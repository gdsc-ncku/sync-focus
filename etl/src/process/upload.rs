use super::Error;
use sea_orm::*;

impl super::payload::Beatbuffer {
    pub async fn upload(
        self,
        db: impl AsRef<DatabaseConnection> + Send + 'static,
    ) -> Result<(), Error> {
        use crate::process::entity::*;
        use sea_orm::*;
        let (summary, tree) = self.into_payload();

        let summary = summary.insert(db.as_ref()).await?;

        for (occur, path) in tree.iter() {
            summary_item::ActiveModel {
                summary_id: ActiveValue::Set(summary.id),
                kind: ActiveValue::Set(todo!() as i32),
                total: ActiveValue::Set(occur as i64),
                ..Default::default()
            };
        }

        Ok(())
    }
}
