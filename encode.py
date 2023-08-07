from cryptography.fernet import Fernet
import base64
import json



def generate_key():
    return Fernet.generate_key()


def encode(data, secret_key: str):
    cipher_suite = Fernet(secret_key)
    license_str = json.dumps(data)
    encoded_text = cipher_suite.encrypt(license_str.encode('utf-8'))
    return base64.urlsafe_b64encode(encoded_text).decode('utf-8')