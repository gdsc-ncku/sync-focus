use super::{
    entity::{summary, summary_item},
    Error,
};
use crate::{
    constant::{Time, HEARTBEAT_THRESHOLD},
    process::entity::summary_item::RecordKind,
};
use sea_orm::*;

fn get_time_range(times: impl Iterator<Item = Time>) -> i64 {
    let mut total = 0;
    let mut times = times.collect::<Vec<_>>();
    times.sort();
    times.windows(2).for_each(|win| {
        let delta = (win[1] - win[0]).abs();
        if delta < HEARTBEAT_THRESHOLD {
            total += delta.num_seconds() as i64;
        }
    });
    total
}

struct SummaryWrapper<'a>(summary::Model, &'a DatabaseConnection);

impl<'a> SummaryWrapper<'a> {
    pub async fn insert_item(
        &self,
        kind: RecordKind,
        times: impl Iterator<Item = Time>,
        key: String,
    ) -> Result<summary_item::Model, Error> {
        let model = summary_item::ActiveModel {
            summary_id: ActiveValue::Set(self.0.id),
            kind: ActiveValue::Set(kind),
            total: ActiveValue::Set(get_time_range(times)),
            key: ActiveValue::Set(key),
            ..Default::default()
        }
        .insert(self.1)
        .await?;

        Ok(model)
    }
}

impl super::payload::Beatbuffer {
    pub async fn upload(
        self,
        db: impl AsRef<DatabaseConnection> + Send + 'static,
    ) -> Result<(), Error> {
        let (summary, tree) = self.clone().into_payloads();
        let summary = summary.insert(db.as_ref()).await?;
        let summary = SummaryWrapper(summary, db.as_ref());

        macro_rules! insert {
            ($elements:expr, $kind:ident) => {
                for (path, times) in $elements {
                    summary
                        .insert_item(RecordKind::$kind, times.into_iter(), path)
                        .await?;
                }
            };
        }
        insert!(tree.into_iter(), Path);
        insert!(self.clone().into_domains(), Domain);
        insert!(self.into_agents(), UserAgent);

        Ok(())
    }
}
