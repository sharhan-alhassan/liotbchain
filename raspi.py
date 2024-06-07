from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import json
import time
import requests

# Generate a new RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

def save_keys(private_key, public_key, device_id):
    with open(f"{device_id}_private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    with open(f"{device_id}_public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

def load_private_key(device_id):
    with open(f"{device_id}_private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    return private_key

def sign_data(private_key, data):
    message = json.dumps(data).encode()
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature

# Example data from IoT device
device_id = "RaspberryPi1"
data = {"device": device_id, "distance": 120, "timestamp": time.time()}

# Generate keys and save them (done once)
save_keys(private_key, public_key, device_id)

# Load private key and sign data
private_key = load_private_key(device_id)
signature = sign_data(private_key, data)

# Send data and signature to server
payload = {"data": data, "signature": signature.hex()}
response = requests.post('http://<server-ip>:5000/add_block', json=payload)

print(response.json())
