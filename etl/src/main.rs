use server::Server;

mod constant;
mod logger;
mod process;
mod server;

#[tokio::main]
async fn main() {
    logger::init();
    Server::new().await.unwrap().attach().await.unwrap();
}
