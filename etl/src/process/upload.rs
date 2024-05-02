use super::Error;
use sea_orm::*;

impl super::payload::Beatbuffer {
    pub async fn upload(
        self,
        db: impl AsRef<DatabaseConnection> + Send + 'static,
    ) -> Result<(), Error> {
        use crate::process::entity::*;
        use sea_orm::*;
        for (summary, tree) in self.into_payloads() {
            let summary = summary.insert(db.as_ref()).await?;

            for (occur, path) in tree.iter() {
                summary_item::ActiveModel {
                    summary_id: ActiveValue::Set(summary.id),
                    kind: ActiveValue::Set(1 as i32), // FIXME: change it
                    total: ActiveValue::Set(occur as i64),
                    key: ActiveValue::Set(path),
                    ..Default::default()
                }
                .insert(db.as_ref())
                .await?;
            }
        }
        Ok(())
    }
}
