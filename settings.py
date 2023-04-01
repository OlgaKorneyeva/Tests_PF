import os

from dotenv import load_dotenv

load_dotenv()

invalid_email = os.getenv('invalid_email')
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
invalid_password = os.getenv('invalid_password')
unregistered_email = os.getenv('unregistered_email')
unregistered_password = os.getenv('unregistered_password')
invalid_auth_key = os.getenv('invalid_auth_key')
