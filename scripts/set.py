import yaml
from sqlalchemy import Table, create_engine, update, MetaData, insert
from config import Config

# NOTE: This script fills an existing database with data from a YAML file. Please sure the database is already created.
if __name__ == "__main__":
    obj = {}
    cfg = Config()
    engine = create_engine(cfg.SQLALCHEMY_DATABASE_URI)

    # Load data from YAML file
    with open('scripts/db_objects.yaml', 'r') as file:
        data = yaml.safe_load(file)

    metadata = MetaData()
    metadata.reflect(bind=engine)
    with engine.connect() as conn:
        transaction = conn.begin()

        for table_name, rows in data.items():
            if table_name in metadata.tables:
                table = metadata.tables[table_name]
            else:
                print(f"Creating table {table_name}")
                table = Table(table_name, metadata)

            primary_key = list(table.primary_key.columns)[0].name

            for row in rows:
                # check if exists in table
                if conn.execute(table.select().where(table.c.get(primary_key) == row[primary_key])).fetchone():
                    print(f"Updating {table_name} with {row}")
                    conn.execute(update(table).where(table.c.get(primary_key) == row[primary_key]).values(**row))
                else:
                    print(f"Inserting {table_name} with {row}")
                    conn.execute(insert(table).values(**row))

        # Commit the changes
        transaction.commit()
