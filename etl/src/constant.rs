use chrono::TimeDelta;

pub static SQL_URL: &str = "postgres://postgres:password@localhost:5432/postgres";
pub static RABBITMQ_URL: &str = "amqp://guest:guest@localhost:5672/%2f";

pub static RABBITMQ_QUEUE: &str = "focus_summary_IN";
pub static BUFFER_MAX_LENGTH: usize = 1000;
pub static BUFFER_MAX_TIME: TimeDelta = TimeDelta::minutes(10);

pub type Time = chrono::DateTime<chrono::FixedOffset>;
