use super::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq)]
#[sea_orm(table_name = "summary_items")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: Uuid,
    pub summary_id: Uuid,
    #[sea_orm(column_name = "type")]
    pub type_: i32,
    pub total: i64,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(
        belongs_to = "super::summary::Entity",
        from = "Column::SummaryId",
        to = "super::summary::Column::Id",
        on_update = "NoAction",
        on_delete = "NoAction"
    )]
    Summary
}

impl Related<super::summary::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::Summary.def()
    }
}

impl ActiveModelBehavior for ActiveModel {}