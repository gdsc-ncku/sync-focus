use super::entity::*;
use crate::error::Error;
use core::str;
use lapin::message::Delivery;
use sea_orm::{ColumnTrait, DatabaseConnection, EntityTrait, QueryFilter, TransactionTrait};
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;
use std::ops::Bound::Included;
use std::sync::atomic::AtomicUsize;
use std::sync::Arc;
use tokio::task::JoinHandle;
use tokio_stream::StreamExt;
use uuid::Uuid;

static RUNNING_BACKGROUND_TASKS: AtomicUsize = AtomicUsize::new(0);

#[derive(Deserialize, Serialize)]
struct Domain {
    domain: String,
    path: String,
}

#[derive(Deserialize, Serialize)]
pub struct Request {
    target_user: Uuid,
    start_time: chrono::NaiveDateTime,
    end_time: chrono::NaiveDateTime,
    domains: Vec<Domain>,
}

impl TryFrom<Delivery> for Request {
    type Error = Error;

    fn try_from(value: Delivery) -> Result<Self, Self::Error> {
        serde_json::from_slice(&value.data).map_err(Error::RequestParseError)
    }
}

impl Request {
    pub fn process(
        self,
        db: impl AsRef<DatabaseConnection> + Send + 'static,
    ) -> JoinHandle<Result<(), Error>> {
        tokio::spawn(async move {
            let filter = &{
                let mut filter = BTreeSet::new();
                for domain in self.domains {
                    filter.insert([domain.domain, domain.path].concat());
                }
                filter
            };

            let txn = Arc::new(db.as_ref().begin().await?);

            let stream = heartbeat::Entity::find()
                .filter(heartbeat::Column::UserId.eq(self.target_user))
                .filter(heartbeat::Column::Time.gt(self.start_time))
                .filter(heartbeat::Column::Time.lt(self.end_time))
                .stream_partial_model::<_, heartbeat::PartialModel>(&*txn)
                .await?;

            let mut stream: Vec<_> = stream
                .filter_map(|item| match item {
                    Ok(item) => {
                        let mut url = item.domain.clone();
                        url.push_str(&item.path);
                        Some(url)
                    }
                    Err(err) => {
                        tracing::warn!("Error: {:?}", err);
                        None
                    }
                })
                .map(|x| {
                    let bound = Included(x);
                    filter.range((bound.clone(), bound)).next().is_some()
                })
                .collect()
                .await;

            Ok(())
        })
    }
}
