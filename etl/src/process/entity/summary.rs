use super::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq)]
#[sea_orm(table_name = "summaries")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: Uuid,
    pub user_id: Uuid,
    pub from_time: chrono::NaiveDateTime,
    pub to_time: chrono::NaiveDateTime,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(has_many = "super::summary_item::Entity")]
    SummaryItem,
}

impl Related<super::summary_item::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::SummaryItem.def()
    }
}

impl ActiveModelBehavior for ActiveModel {}
