#![no_main]
use libfuzzer_sys::fuzz_target;

use aes::cipher::generic_array::GenericArray;
use aes::cipher::{NewCipher, StreamCipher};
use aes::Aes128Ctr as Aes;

use aes_ctr::cipher::generic_array::GenericArray as GenericArrayCtr;
use aes_ctr::cipher::{NewStreamCipher, SyncStreamCipher};
use aes_ctr::Aes128Ctr as AesCtr;

// Differential fuzz `aes` vs `aes-ctr` crates (note encryption and decryption are the same process)
fuzz_target!(|data: &[u8]| {
    // Take 32 bytes for plain text (to match BLS secret key), 16 bytes for IV and 16 bytes for key (use `cargo fuzz run <target> -- -max_len=64`)
    if data.len() != 64 {
        return;
    }

    // Prepare parameters
    let iv = data[..16].to_vec();
    let key = data[16..32].to_vec();
    let plain_text = data[32..].to_vec();

    // aes
    let mut cipher_text_aes = plain_text.clone();
    let key = GenericArray::from_slice(&key);
    let nonce = GenericArray::from_slice(&iv);
    let mut cipher = Aes::new(key, nonce);
    cipher.apply_keystream(&mut cipher_text_aes);

    // aes-ctr
    let mut cipher_text_aes_ctr = plain_text.clone();
    let key = GenericArrayCtr::from_slice(&key);
    let nonce = GenericArrayCtr::from_slice(&iv);
    let mut cipher = AesCtr::new(key, nonce);
    cipher.apply_keystream(&mut cipher_text_aes_ctr);

    assert_eq!(cipher_text_aes_ctr, cipher_text_aes);
});
