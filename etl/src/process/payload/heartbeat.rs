use std::collections::{btree_map::IntoIter, BTreeMap};

use lapin::message::Delivery;
use lockable::{AsyncLimit, LockableHashMap};
use sea_orm::DatabaseConnection;
use serde::{Deserialize, Serialize};
use tokio_stream::StreamExt;
use uuid::Uuid;

use crate::{constant::*, error::Error};

/// Heartbeat is a struct that contains the pathline and time of a heartbeat
///
/// It's part of API spec
#[derive(Deserialize, Serialize)]
pub struct Heartbeat {
    pathline: String,
    time: Time,
}

/// Heartbeat is a struct that contains the pathline and time of a heartbeat
///
/// It's part of API spec
#[derive(Deserialize, Serialize)]
pub struct Heartbeats {
    pub trace_id: u64,
    user_id: Uuid,
    user_agent: String,
    list: Vec<Heartbeat>,
}

impl TryFrom<Delivery> for Heartbeats {
    type Error = Error;

    fn try_from(value: Delivery) -> Result<Self, Self::Error> {
        serde_json::from_slice(&value.data).map_err(Error::RequestParseError)
    }
}

/// Beatbuffer realises logic of batching heartbeats and uploading them to the database
#[derive(Default)]
pub struct Beatbuffer(BTreeMap<Time, String>);

impl From<Heartbeats> for Beatbuffer {
    fn from(value: Heartbeats) -> Self {
        Self(
            value
                .list
                .into_iter()
                .map(|x| (x.time, x.pathline))
                .collect(),
        )
    }
}

impl IntoIterator for Beatbuffer {
    type Item = Heartbeat;

    type IntoIter = std::iter::Map<IntoIter<Time, String>, fn((Time, String)) -> Heartbeat>;

    fn into_iter(self) -> Self::IntoIter {
        self.0
            .into_iter()
            .map(|(time, pathline)| Heartbeat { pathline, time })
    }
}

impl Beatbuffer {
    pub fn add(&mut self, beats: Heartbeats) {
        self.0
            .extend(beats.list.into_iter().map(|x| (x.time, x.pathline)));
    }
    pub fn is_full(&self) -> bool {
        match self.0.is_empty() {
            true => false,
            false => {
                let start = self.0.last_key_value().unwrap().0.clone();
                let end = self.0.first_key_value().unwrap().0.clone();
                (self.0.len() >= BUFFER_MAX_LENGTH) || (end - start >= BUFFER_MAX_TIME)
            }
        }
    }
    pub async fn upload(self, db: impl AsRef<DatabaseConnection> + Send + 'static) {
        todo!()
    }
}

/// BeatBuffers is a struct that enable batching heartbeats and uploading them to the database
#[derive(Default)]
pub struct BeatBuffers(LockableHashMap<Uuid, Beatbuffer>);

impl BeatBuffers {
    pub fn new() -> Self {
        Self(LockableHashMap::new())
    }
    /// partially lock the hashmap, insert the beatbuffer if the user_id is not present
    ///
    /// return the beatbuffer if it should be flushed
    pub async fn add(&self, beats: Heartbeats) -> Option<Beatbuffer> {
        let mut entry = self
            .0
            .async_lock(beats.user_id, AsyncLimit::no_limit())
            .await
            .unwrap();
        match entry.value_mut() {
            Some(x) => x.add(beats),
            None => {
                entry.insert(Beatbuffer::from(beats));
            }
        };
        match entry.value().unwrap().is_full() {
            true => Some(entry.remove().unwrap()),
            false => None,
        }
    }
    /// force flush all the beatbuffer in the hashmap
    pub async fn flush(&self, db: impl AsRef<DatabaseConnection> + Send + Clone + 'static) {
        let mut join_set = tokio::task::JoinSet::new();

        let mut iter = self.0.lock_all_entries().await;
        while let Some(mut entry) = iter.next().await {
            let beats = entry.remove().unwrap();
            join_set.spawn(beats.upload(db.clone()));
        }

        while join_set.join_next().await.is_some() {}
    }
}
