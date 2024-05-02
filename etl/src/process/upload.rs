use crate::constant::HEARTBEAT_THRESHOLD;

use super::Error;
use itertools::Itertools;
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

            for (mut times, path) in tree.into_iter() {
                let mut total = 0;
                times.sort();
                times.windows(2).for_each(|win| {
                    let delta = (win[1] - win[0]).abs();
                    if delta < HEARTBEAT_THRESHOLD {
                        total += delta.num_seconds() as i64;
                    }
                });

                summary_item::ActiveModel {
                    summary_id: ActiveValue::Set(summary.id),
                    kind: ActiveValue::Set(1 as i32), // FIXME: change it
                    total: ActiveValue::Set(total as i64),
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
