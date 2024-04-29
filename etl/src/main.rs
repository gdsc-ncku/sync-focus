use server::Server;

pub mod constant;
pub mod process;
pub mod server;

#[tokio::main]
async fn main() {
    // FIXME: add logger
    Server::new().await.unwrap().attach().await.unwrap();
}
