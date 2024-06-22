import json
import os
from sqlalchemy import Connection, create_engine, inspect, insert, select

from config import Config
from borkum.website.database.models import (
    Contact,
    Flat,
    FlatImage,
    House,
    HouseImage,
    Tag,
    Category,
    flat_tag_association,
)
import uuid
from PIL import Image
def uuid4():
    return str(uuid.uuid4())

CONTACT = {
    "name": "Ferienwohnungen Scheibe",
    "street": "Rüschenweg 46",
    "city": "26188 Edewecht",
    "phone": "04486 / 920167",
    "email": "vermietung.scheibe@gmail.com",
    "url_name": "traum-ferienwohnungen.de",
    "url": "https://www.traum-ferienwohnungen.de/objektuebersicht/scheibe/",
}

DB_OBJECTS = json.load(open("./scripts/db_objects.json"))

cfg = Config()


def seed_contact(conn: Connection):
    if (
        not inspect(engine).has_table(Contact.__tablename__)
        or conn.execute(
            select(Contact).where(Contact.name == CONTACT["name"])
        ).fetchone()
        is None
    ):
        Contact.__table__.create(bind=engine, checkfirst=True)

        conn.execute(insert(Contact).values(id=uuid4(), **CONTACT))

        conn.commit()
    else:
        print(f"Contact {CONTACT['name']} already exists")


def seed_categories(conn: Connection):
    categories: set[str] = {t["category"] for t in DB_OBJECTS["tag_names"]}

    for c in categories:
        if (
            not inspect(engine).has_table(Category.__tablename__)
            or conn.execute(select(Category).where(Category.name == c)).fetchone()
            is None
        ):
            Category.__table__.create(bind=engine, checkfirst=True)

            conn.execute(insert(Category).values(id =uuid4(),name=c))

        else:
            print(f"Category {c} already exists")
    conn.commit()


def seed_tags(conn: Connection):
    for t in DB_OBJECTS["tag_names"]:
        if (
            not inspect(engine).has_table(Tag.__tablename__)
            or conn.execute(select(Tag).where(Tag.name == t["name"])).fetchone() is None
        ):
            Tag.__table__.create(bind=engine, checkfirst=True)

            category = conn.execute(
                Category.__table__.select().where(Category.name == t["category"])
            ).fetchone()
            conn.execute(insert(Tag).values(id =uuid4(),name=t["name"], category_id=category.id))

        else:
            print(f"Tag {t['name']} already exists")
    conn.commit()


def seed_houses(conn: Connection):
    for h in DB_OBJECTS["houses"]:
        if (
            not inspect(engine).has_table(House.__tablename__)
            or conn.execute(select(House).where(House.name == h["name"])).fetchone()
            is None
        ):
            House.__table__.create(bind=engine, checkfirst=True)

            conn.execute(insert(House).values(id =uuid4(),**h))

        else:
            print(f"House {h['name']} already exists")
    conn.commit()


def seed_flats(conn: Connection):
    for f in DB_OBJECTS["flats"]:
        if (
            not inspect(engine).has_table(Flat.__tablename__)
            or conn.execute(select(Flat).where(Flat.name == f["name"])).fetchone()
            is None
        ):
            Flat.__table__.create(bind=engine, checkfirst=True)

            house = conn.execute(
                House.__table__.select().where(House.name == f["house"])
            ).fetchone()
            data = {**f}
            del data["house"]
            del data["tag_names"]

            conn.execute(insert(Flat).values(id =uuid4(),**data, house_id=house.id))

            conn.commit()
        else:
            print(f"Flat {f['name']} already exists")
    conn.commit()


def seed_flat_tag_association(conn: Connection):
    for f in DB_OBJECTS["flats"]:
        for t in f["tag_names"]:
            flat_tag_association.create(bind=engine, checkfirst=True)

            flat = conn.execute(
                Flat.__table__.select().where(Flat.name == f["name"])
            ).fetchone()
            tag = conn.execute(Tag.__table__.select().where(Tag.name == t)).fetchone()

            if (
                not inspect(engine).has_table(flat_tag_association.name)
                or conn.execute(
                    flat_tag_association.select().where(
                        flat_tag_association.c.flat_id == flat.id
                        and flat_tag_association.c.tag_id == tag.id
                    )
                ).fetchone()
                is None
            ):
                conn.execute(
                    flat_tag_association.insert().values(flat_id=flat.id, tag_id=tag.id)
                )

            else:
                print(f"Flat {f['name']} already has tag {t}")

    conn.commit()

def seed_flat_images(conn: Connection):

    source_path = "Bilder/flats"
    static_path = "borkum/website/static/images/objects"


    for flat in conn.execute(Flat.__table__.select()).fetchall():
        if not os.path.exists(f"{static_path}/{flat.id}"):
            folder_name = f"{flat.name.lower().replace(' ', '-')}"
            FlatImage.__table__.create(bind=engine, checkfirst=True)

            # get all images from file system    
            imgs = os.listdir(f"{source_path}/{folder_name}/rooms")

            for img in imgs:
                title = img.split(".")[0].split("-")[-1]
                title = str(title[0].upper() + title[1:])

                img_id = uuid4()
                conn.execute(
                    insert(FlatImage).values(id = img_id,flat_id=flat.id, title=title)
                )
                # convert image to webp and save in static folder
                image = Image.open(f"{source_path}/{folder_name}/rooms/{img}")
                image = image.convert('RGB')
                os.system(f"mkdir -p {static_path}/{flat.id}")
                image.save(f"{static_path}/{flat.id}/{img_id}.webp", 'webp')
        else:
            print(f"Flat {flat.name} already has images")
    conn.commit()

def seed_house_images(conn: Connection):

    source_path = "Bilder/houses"
    static_path = "borkum/website/static/images/objects"

    for house in conn.execute(House.__table__.select()).fetchall():
        if not os.path.exists(f"{static_path}/{house.id}"):
            folder_name = f"{house.name.lower().replace(' ', '-')}"
            HouseImage.__table__.create(bind=engine, checkfirst=True)

            # get all images from file system    
            if os.path.exists(f"{source_path}/{folder_name}"):
                imgs = os.listdir(f"{source_path}/{folder_name}")

                for img in imgs:
                    title = img.split(".")[0].split("-")[-1]
                    title = str(title[0].upper() + title[1:])

                    img_id = uuid4()
                    conn.execute(
                        insert(HouseImage).values(id = img_id,house_id=house.id, title=title)
                    )
                    # convert image to webp and save in static folder
                    image = Image.open(f"{source_path}/{folder_name}/{img}")
                    image = image.convert('RGB')
                    os.system(f"mkdir -p {static_path}/{house.id}")
                    image.save(f"{static_path}/{house.id}/{img_id}.webp", 'webp')
        else:
            print(f"House {house.name} already has images")
    conn.commit()

if __name__ == "__main__":
    engine = create_engine(cfg.SQLALCHEMY_DATABASE_URI)

    with engine.connect() as conn:
        seed_contact(conn)
        seed_categories(conn)
        seed_tags(conn)
        seed_houses(conn)
        seed_flats(conn)
        seed_flat_tag_association(conn)
        seed_flat_images(conn)
        seed_house_images(conn)
        conn.close()
