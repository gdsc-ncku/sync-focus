use std::sync::atomic::AtomicUsize;
use std::sync::Arc;

use crate::constant::{BUFFER_MAX_TIME, RABBITMQ_QUEUE, RABBITMQ_URL, SQL_URL};
use crate::process::*;
use lapin::{options, types, Channel, Connection, ConnectionProperties};
use sea_orm::{Database, DatabaseConnection};
use std::sync::atomic::Ordering;
use tokio::time;
use tokio_stream::StreamExt;
use tracing::*;

const SERIAL: AtomicUsize = AtomicUsize::new(0);

macro_rules! slient_err {
    ($e:expr) => {
        match $e {
            Ok(x) => x,
            Err(err) => {
                tracing::error!("Error processing request: {:?}", err);
                return;
            }
        }
    };
}
pub struct Server {
    channel: Channel,
    pub db: Arc<DatabaseConnection>,
    pub beatbuffer: BeatBuffers,
}

impl Server {
    pub async fn new() -> Result<Self, Error> {
        let conn = Connection::connect(&RABBITMQ_URL, ConnectionProperties::default()).await?;

        let channel = conn.create_channel().await?;
        let db = Arc::new(Database::connect(&*SQL_URL).await?);

        Ok(Server {
            channel,
            db,
            beatbuffer: BeatBuffers::default(),
        })
    }
    async fn heartbeat(self: Arc<Self>) -> Result<(), Error> {
        let serial = SERIAL.fetch_add(1, Ordering::AcqRel);
        let mut consumer = self
            .channel
            .basic_consume(
                &*RABBITMQ_QUEUE,
                format!("consumer-{}", serial).as_str(),
                options::BasicConsumeOptions::default(),
                types::FieldTable::default(),
            )
            .await?;

        while let Some(x) = consumer.next().await {
            let deliver = x?;

            let self_ = self.clone();
            tokio::spawn(async move {
                let span = info_span!("heartbeat", id = %deliver.delivery_tag);
                slient_err!(
                    deliver
                        .ack(options::BasicAckOptions::default())
                        .instrument(span.clone())
                        .await
                );
                // FIXME: compute busy_ns for JSON parsing
                let request = slient_err!(deliver.try_into());
                // FIXME: Propagation
                // https://docs.rs/opentelemetry_sdk/0.22.1/opentelemetry_sdk/propagation/struct.TraceContextPropagator.html
                slient_err!(self_.process_heartbeats(request).instrument(span).await);
            });
        }

        Ok(())
    }
    pub async fn process_heartbeats(self: Arc<Self>, heartbeats: Heartbeats) -> Result<(), Error> {
        let user_id = heartbeats.user_id;
        if let Some(buffer) = self.beatbuffer.add(heartbeats).await {
            buffer.upload(self.db.clone()).await?;
        }

        tokio::spawn(async move {
            time::sleep(BUFFER_MAX_TIME.to_std().unwrap()).await;
            if let Some(buffer) = self.beatbuffer.get_full(user_id).await {
                if let Err(err) = buffer.upload(self.db.clone()).await {
                    tracing::warn!("Error uploading buffer: {:?}", err);
                }
            }
        });

        Ok(())
    }
    pub async fn attach(self) -> Result<(), Error> {
        let self_ = Arc::new(self);
        tokio::spawn(async move { slient_err!(self_.heartbeat().await) });
        Ok(())
    }
}
