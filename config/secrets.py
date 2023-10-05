import os
from dotenv import load_dotenv
load_dotenv()
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE", None)
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", None)
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", None)
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME", None)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
)
