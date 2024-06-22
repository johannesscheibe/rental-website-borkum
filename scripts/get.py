from sqlalchemy import create_engine, inspect, select, MetaData, quoted_name
import yaml
from config import Config

if __name__ == "__main__":
    obj = {}
    cfg = Config()
    engine = create_engine(cfg.SQLALCHEMY_DATABASE_URI)
    metadata = MetaData()

    
    metadata.reflect(bind=engine)

    insp = inspect(engine)
    for table_name in insp.get_table_names():
        table = metadata.tables[table_name]
        
        cols: list[str] = list(map(str, table.columns.keys()))

        obj[table_name] = []
        with engine.connect() as con:
            result = con.execute(select(table))
            # iterate over the result and add it to the object
            for row in result:
                obj[table_name].append(dict(zip(cols, row)))

    with open("scripts/db_objects.yaml", "w+") as f:
        yaml.safe_dump(obj, f)