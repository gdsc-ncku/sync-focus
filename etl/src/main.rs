use server::Server;

mod constant;
mod logger;
mod process;
mod server;

#[tokio::main]
async fn main() {
    logger::init();
    tracing::info!("Starting server...");
    Server::new().await.unwrap().attach().await.unwrap();
    tracing::info!("Exit");
    // 1970-01-01 00:00:00 +00:00
}
