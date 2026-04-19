from logging.config import fileConfig
from alembic.op import f
from sqlalchemy import engine_from_config, pool
from alembic import context

from core.config import settings
from core.database import DATABASE_URL, Base
import app.models   # ✅ load all models

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Set DB URL dynamically
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# DATABASE_URL = settings.SQLITE
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL
)

# ✅ Metadata
target_metadata = Base.metadata


# ----------------------------
# OFFLINE MODE
# ----------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ----------------------------
# ONLINE MODE
# ----------------------------
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# ----------------------------
# RUN
# ----------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()