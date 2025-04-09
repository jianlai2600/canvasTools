# run once to create .well-known/jwks.json
import json
from cryptography.hazmat.primitives import serialization
from jwcrypto import jwk

key_file = "keys/private.key"
with open(key_file, "rb") as f:
    private_key = f.read()

key = jwk.JWK.from_pem(private_key)
jwk_dict = json.loads(key.export_public())
with open(".well-known/jwks.json", "w") as f:
    json.dump({"keys": [jwk_dict]}, f, indent=2)