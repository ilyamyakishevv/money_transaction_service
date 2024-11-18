import os
import sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from pathlib import Path
import importlib

from configs.config import db_settings
from models.base import Base

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

services = ['auth_service', 'transaction_service']
for service in services:
    models_folder = Path(__file__).resolve().parent.parent / service / "models"
    for model_file in models_folder.glob("*.py"):
        module_name = f"{service}.models.{model_file.stem}"
        importlib.import_module(module_name)

target_metadata = Base.metadata


def get_url() -> str:
    postgres_server = db_settings.POSTGRES_HOST
    postgres_user = db_settings.POSTGRES_USER
    postgres_password = db_settings.POSTGRES_PASSWORD
    postgres_db = db_settings.POSTGRES_DB
    postgres_port = db_settings.POSTGRES_PORT

    return (
        f"postgresql+asyncpg://{postgres_user}:{postgres_password}"
        f"@{postgres_server}:{postgres_port}/{postgres_db}"
    )


def run_migrations_offline() -> None:
    # url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()



if context.is_offline_mode():
    run_migrations_offline()

