use sea_orm::FromQueryResult;

use super::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq)]
#[sea_orm(table_name = "heartbeat")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: Uuid,
    pub user_id: Uuid,
    pub entity: String,
    #[sea_orm(column_name = "type")]
    pub kind: String,
    pub category: String,
    pub browser: String,
    pub domain: String,
    pub path: String,
    pub user_agent: String,
    pub time: Time,
    pub hash: String,
    pub created_at: Time,
}

#[derive(DerivePartialModel, FromQueryResult)]
#[sea_orm(entity = "Entity")]
pub struct PartialModel {
    #[sea_orm(primary_key)]
    pub id: Uuid,
    pub user_id: Uuid,
    pub domain: String,
    pub path: String,
    pub time: chrono::NaiveDateTime,
    pub hash: String,
    pub created_at: chrono::NaiveDateTime,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
