from app import (
    app
)
from alembic import config, script, command
from alembic.runtime import migration
from sqlalchemy import engine


def check_current_head(alembic_cfg, connectable):
    """

    """
    # import pdb; pdb.set_trace()
    # type: (config.Config, engine.Engine) -> bool
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())


# import pdb; pdb.set_trace()

# Get database URL
db_connection = app.config["SQLALCHEMY_DATABASE_URI"]

# Validate database URL
if db_connection is None:
    raise TypeError("`db_connection` cannot be `None`.")
elif not isinstance(db_connection, str):
    raise TypeError("`db_connection` must be a string.")

# Establish database connection
eng = engine.create_engine(
    db_connection,
    echo=True
)

# Configure
cfg = config.Config("alembic.ini")

print('check_current_head() ==', check_current_head(cfg, eng))
