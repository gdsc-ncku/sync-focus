use super::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq)]
#[sea_orm(table_name = "summary_items")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: Uuid,
    pub summary_id: Uuid,
    #[sea_orm(column_name = "type")]
    pub kind: RecordKind,
    pub total: i64,
    #[sea_orm(column_type = "Text")]
    pub key: String,
}

#[derive(Clone, Debug, PartialEq, EnumIter, DeriveActiveEnum, Eq)]
#[sea_orm(rs_type = "i32", db_type = "Integer")]
pub enum RecordKind {
    #[sea_orm(num_value = 0)]
    Domain,
    #[sea_orm(num_value = 1)]
    Path,
    #[sea_orm(num_value = 2)]
    UserAgent,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(
        belongs_to = "super::summary::Entity",
        from = "Column::SummaryId",
        to = "super::summary::Column::Id"
    )]
    Summary,
}

impl Related<super::summary::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::Summary.def()
    }
}

impl ActiveModelBehavior for ActiveModel {}
