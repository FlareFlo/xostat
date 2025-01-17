### Installing Rust

Rust requires Visual Studio 2013 or greater C++ tools, instructions on how to do so are below:

https://rust-lang.github.io/rustup/installation/windows-msvc.html

After run rustup-init from the following site:

https://rustup.rs/

### Install target

```bash
rustup target add x86_64-unknown-linux-musl
```

### Creating new services or libraries

Creating a service.

```bash
cd ./services
cargo new hello_world
```

Creating a library.

```bash
cd ./lib
cargo new my_library --lib
```

Build with

```bash
cargo build --release --target x86_64-unknown-linux-musl
```

Add to serverless.yml

```bash
functions:
  hello:
    handler: hello_world
    package:
      artifact: ./target/x86_64-unknown-linux-musl/release/bootstrap.zip
```
