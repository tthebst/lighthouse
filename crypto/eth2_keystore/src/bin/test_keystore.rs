use eth2_keystore::Keystore;
use std::env;

fn main() {
    let keystore = Keystore::from_json_file("keystore.json")
        .expect("please place keystore.json in eth2_keystore directory");
    let password = env::var("PASSWORD").expect("please define PASSWORD environment variable");

    keystore
        .decrypt_keypair(password.as_bytes())
        .expect("found the bug!");
    println!("this commit is OK");
}
