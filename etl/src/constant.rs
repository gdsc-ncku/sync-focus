use chrono::TimeDelta;
use std::env::var;

// postgres://postgres:admin@localhost:5432/postgres
lazy_static::lazy_static! {
    pub static ref SQL_URL: String = var("SQL_URL").unwrap_or("postgres://postgres:postgres@localhost:5432/postgres".to_string());
    pub static ref RABBITMQ_URL: String = var("RABBITMQ_URL").unwrap_or("amqp://guest:guest@localhost:5672/%2f".to_string());
    pub static ref RABBITMQ_QUEUE: String = var("RABBITMQ_QUEUE").unwrap_or("focus_summary_IN".to_string());
}

pub static BUFFER_MAX_LENGTH: usize = 1000;
pub static BUFFER_MAX_TIME: TimeDelta = TimeDelta::minutes(10);

pub type Time = chrono::DateTime<chrono::FixedOffset>;
