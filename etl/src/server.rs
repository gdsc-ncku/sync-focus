use std::sync::atomic::AtomicUsize;
use std::sync::Arc;

use crate::constant::{RABBITMQ_QUEUE, RABBITMQ_URL, SQL_URL};
use crate::error::Error;
use crate::process::request;
use lapin::{options, types, Channel, Connection, ConnectionProperties};
use sea_orm::{Database, DatabaseConnection};
use std::sync::atomic::Ordering;
use tokio_stream::StreamExt;

const SERIAL: AtomicUsize = AtomicUsize::new(0);

pub struct Server {
    channel: Channel,
    db: Arc<DatabaseConnection>,
}

impl Server {
    pub async fn new() -> Result<Self, Error> {
        let conn = Connection::connect(&RABBITMQ_URL, ConnectionProperties::default()).await?;

        let channel = conn.create_channel().await?;
        let db = Arc::new(Database::connect(SQL_URL).await?);

        Ok(Server { channel, db })
    }
    async fn attach(&self) -> Result<(), Error> {
        let serial = SERIAL.fetch_add(1, Ordering::AcqRel);
        let mut consumer = self
            .channel
            .basic_consume(
                RABBITMQ_QUEUE,
                format!("consumer-{}", serial).as_str(),
                options::BasicConsumeOptions::default(),
                types::FieldTable::default(),
            )
            .await
            .unwrap();
        while let Some(deliver) = consumer.next().await {
            let deliver = deliver?;
            deliver.ack(options::BasicAckOptions::default()).await?;
        }

        while let Some(x) = consumer.next().await {
            let deliver = x?;
            let request:request::Request = deliver.try_into()?;
            
            let db=self.db.clone();
            tokio::spawn(async {
                if let Err(err)=request.process(db).await.unwrap(){
                    tracing::error!("Error processing request: {:?}", err);
                }
            });
        }

        Ok(())
    }
}
