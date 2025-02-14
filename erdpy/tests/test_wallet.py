import logging
from pathlib import Path
from typing import Any

import nacl.encoding
import nacl.signing
from erdpy.accounts import Account, Address
from erdpy.tests.utils import MyTestCase
from erdpy.transactions import Transaction
from erdpy.wallet import (bip39seed_to_private_key, generate_pair,
                          mnemonic_to_bip39seed, pem)

logging.basicConfig(level=logging.INFO)


class WalletTestCase(MyTestCase):
    def setUp(self):
        super().setUp()
        self.alice = Account(pem_file=str(self.devnet_wallets.joinpath("users", "alice.pem")))

    def test_nacl_playground_signing(self):
        private_key_hex = "b8211b08edc8aca591bedf1b9aba47e4077e54ac7d4ceb2f1bc9e10c064d3e6c7a5679a427f6df7adf2310ddf5e570fd51e47e6b1511124d6b250b989b017588"
        private_key_bytes = bytes.fromhex(private_key_hex)
        private_key_seed_bytes = private_key_bytes[:32]
        signing_key: Any = nacl.signing.SigningKey(private_key_seed_bytes)
        signed = signing_key.sign(b"test")
        signature = signed.signature
        signed_bytes_hex = signature.hex()

        self.assertEqual("a4918458d874ca58893a1f92dac33e7b10e3bf46048ad5de5bc260487ca84e8e07603297120fdc018242f63bd8e87b13efd108f8ffa095f536b6eda03805590c", signed_bytes_hex)
        self.assertEqual(64, len(signature))

    def test_pem_get_pubkey(self):
        pem_file = self.devnet_wallets.joinpath("users", "alice.pem")
        address = pem.get_pubkey(pem_file)

        self.assertEqual("0139472eff6886771a982f3083da5d421f24c29181e63888228dc81ca60d69e1", address.hex())

    def test_pem_parse_multiple(self):
        pem_file = self.testdata.joinpath("walletKey.pem")

        seed, address = pem.parse(pem_file, index=0)
        self.assertEqual("1f4dd8b7d18b5d0785c9d0802ec14d553dba356812b85c7e3414373388472010", seed.hex())
        self.assertEqual(Address("erd1sjsk3n2d0krq3pyxxtgf0q7j3t56sgusqaujj4n82l39t9h7jers6gslr4").hex(), address.hex())

        seed, address = pem.parse(pem_file, index=1)
        self.assertEqual("2565dbbdb62301e4c7b12b8a41cd3b2fbd7ae687c8d9741937aa48cf246aeb25", seed.hex())
        self.assertEqual(Address("erd10536tc3s886yqxtln74u6mztuwl5gy9k9gp8fttxda0klgxg979srtg5wt").hex(), address.hex())

        seed, address = pem.parse(pem_file, index=2)
        self.assertEqual("08de69d398f4a5ffdce0f1a8569704dbc8b58aaf7ba3e726134e32f1e8bf04ad", seed.hex())
        self.assertEqual(Address("erd1n230jlgfepdvf28vqt3zeawexg2jhvxqxjuqdfsss0xc62xcqcps9k54ag").hex(), address.hex())

        seed, address = pem.parse(pem_file, index=3)
        self.assertEqual("4d9dcc1c09a6d00c4c9a389e662d9fe26e0bf4c859776d4d338b5a9c41fc12d4", seed.hex())
        self.assertEqual(Address("erd143907zxv0ujxr9q4mda7rmczn2xwhmqn7p9lfz666z8hd2lcks2szt5yql").hex(), address.hex())

    def test_pem_parse(self):
        pem_file = self.devnet_wallets.joinpath("users", "alice.pem")
        seed, address = pem.parse(pem_file)

        self.assertEqual("413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9", seed.hex())
        self.assertEqual("0139472eff6886771a982f3083da5d421f24c29181e63888228dc81ca60d69e1", address.hex())

    def test_sign_transaction(self):
        # With data
        transaction = Transaction()
        transaction.nonce = 0
        transaction.value = "0"
        transaction.sender = "erd1l453hd0gt5gzdp7czpuall8ggt2dcv5zwmfdf3sd3lguxseux2fsmsgldz"
        transaction.receiver = "erd188nydpkagtpwvfklkl2tn0w6g40zdxkwfgwpjqc2a2m2n7ne9g8q2t22sr"
        transaction.gasPrice = 200000000000000
        transaction.gasLimit = 500000000
        transaction.data = "foo"
        transaction.chainID = "chainID"
        transaction.version = 1
        transaction.sign(self.alice)

        self.assertEqual("0e69f27e24aba2f3b7a8842dc7e7c085a0bfb5b29112b258318eed73de9c8809889756f8afaa74c7b3c7ce20a028b68ba90466a249aaf999a1a78dcf7f4eb40c", transaction.signature)

        # Without data
        transaction = Transaction()
        transaction.nonce = 0
        transaction.value = "0"
        transaction.sender = "erd1l453hd0gt5gzdp7czpuall8ggt2dcv5zwmfdf3sd3lguxseux2fsmsgldz"
        transaction.receiver = "erd188nydpkagtpwvfklkl2tn0w6g40zdxkwfgwpjqc2a2m2n7ne9g8q2t22sr"
        transaction.gasPrice = 200000000000000
        transaction.gasLimit = 500000000
        transaction.data = ""
        transaction.chainID = "chainID"
        transaction.version = 1
        transaction.sign(self.alice)

        self.assertEqual("83efd1bc35790ecc220b0ed6ddd1fcb44af6653dd74e37b3a49dcc1f002a1b98b6f79779192cca68bdfefd037bc81f4fa606628b751023122191f8c062362805", transaction.signature)    

    def test_generate_pair_pem(self):
        seed, pubkey = generate_pair()
        pem_file = Path(self.testdata_out, "foo.pem")
        pem.write(pem_file, seed, pubkey)
        parsed_seed, parsed_pubkey = pem.parse(pem_file)

        self.assertEqual(seed, parsed_seed)
        self.assertEqual(pubkey, parsed_pubkey)

    def test_derive_private_key(self):
        # password = "Password1!"
        # keystore_file = "erd1zzhmdm2uwv9l7d2ak72c4cv6gek5c797s7qdkfc3jthvrvnxc2jqdsnp9y.json"
        mnemonic = "emotion spare multiply lecture rude machine raise radio ability doll depend equip pass ghost cabin delay birth opera shoe force any slow fluid old"
        mnemonic_seed = "2c3afb9202816c0ad8cfffbfe60b086c3b0600e7e96eddb589ca6bfcb2826a073c823b1c73200f152bd768c47754d7bc1daa82f860024c9916f2eab04ac50da9"
        private_key = "4d6fbfd1fa028afee050068f08c46b95754fd27a06f429b308ba326fff094349"
        public_key = "10afb6ed5c730bff355db7958ae19a466d4c78be8780db271192eec1b266c2a4"
        # address = "erd1zzhmdm2uwv9l7d2ak72c4cv6gek5c797s7qdkfc3jthvrvnxc2jqdsnp9y"

        actual_mnemonic_seed = mnemonic_to_bip39seed(mnemonic)
        actual_private_key = bip39seed_to_private_key(actual_mnemonic_seed)
        signing_key = nacl.signing.SigningKey(actual_private_key)
        actual_public_key = bytes(signing_key.verify_key)

        self.assertEqual(mnemonic_seed, actual_mnemonic_seed.hex())
        self.assertEqual(private_key, actual_private_key.hex())
        self.assertEqual(public_key, actual_public_key.hex())

        # password = "Password1!"
        # keystore_file = "erd1l4qsjlxuq33dld8ujmqlq3qs45f5qlspy2gvwwamshv2jmfg4g3q77yr0p.json"
        mnemonic = "real reveal sausage puppy artefact chapter original enough cinnamon run pledge awake fall double antenna admit keep melody celery since hood hurry achieve fee"
        mnemonic_seed = "9a8a5cfe7e4e7cfea54431aa80b9179985bfbf0af29ce75aff9bc4f5766ec2f5fb308486bb702e7465467a94792d16fd66f9307a95c1912526d08b21b6cc41b8"
        private_key = "33306aa0bf13a02057ece15e07dc8e9cfff2b77147d5a007d205d782fc90e362"
        public_key = "fd41097cdc0462dfb4fc96c1f04410ad13407e012290c73bbb85d8a96d28aa22"
        # address = "erd1l4qsjlxuq33dld8ujmqlq3qs45f5qlspy2gvwwamshv2jmfg4g3q77yr0p"

        actual_mnemonic_seed = mnemonic_to_bip39seed(mnemonic)
        actual_private_key = bip39seed_to_private_key(actual_mnemonic_seed)
        signing_key: Any = nacl.signing.SigningKey(actual_private_key)
        actual_public_key = bytes(signing_key.verify_key)

        self.assertEqual(mnemonic_seed, actual_mnemonic_seed.hex())
        self.assertEqual(private_key, actual_private_key.hex())
        self.assertEqual(public_key, actual_public_key.hex())
