def test_get_public_key(cmd, button, model):
    pub_key, address = cmd.get_public_key(
        bip32_path="44'/5741565'/0'/0'/1'",
        network_byte='V',
        display=True,
        button=button,
        model=model
    )  # type: bytes, bytes

    assert len(pub_key) == 32
    assert len(address) == 35

