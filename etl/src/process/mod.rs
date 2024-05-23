mod entity;
mod payload;
mod trie;
mod upload;

pub use payload::BeatBuffers;
pub use payload::Heartbeats;

#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("`{0}`")]
    RabbitMQError(#[from] lapin::Error),
    #[error("`{0}`")]
    DbError(#[from] sea_orm::DbErr),
    #[error("Error parsing request `{0}`")]
    RequestParseError(serde_json::Error),
    #[error("Unreachable")]
    Unreachable,
}
