pub mod summary;
pub mod summary_item;

use uuid::Uuid;

use sea_orm::{
    entity::prelude::*, EntityTrait, PrimaryKeyTrait, 
};

// https://www.sea-ql.org/SeaORM/docs/generate-entity/entity-structure/#column-name
// All column names are assumed to be in snake-case. You can override the column name by specifying the `column_name` attribute.