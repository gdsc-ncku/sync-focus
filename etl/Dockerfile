FROM rust:1.77.1-slim-buster AS builder

WORKDIR /complier

RUN apt update -y
RUN apt install musl-tools protobuf-compiler pkg-config make -y

RUN cargo install just

RUN --mount=type=cache,target=~/.cargo/bin/
RUN --mount=type=cache,target=~/.cargo/registry/index/
RUN --mount=type=cache,target=~/.cargo/registry/cache/
RUN --mount=type=cache,target=~/.cargo/git/db/

WORKDIR /complier

COPY . .
RUN --mount=type=cache,target=target

ARG ARCH

RUN rustup target add ${ARCH}-unknown-linux-musl
RUN cargo install --no-default-features --features release --target ${ARCH}-unknown-linux-musl

FROM scratch
# WORKDIR are used instead of mkdir
WORKDIR /database
WORKDIR /config
WORKDIR /
COPY --from=builder /usr/local/cargo/bin/etl /

CMD ["/etl"]