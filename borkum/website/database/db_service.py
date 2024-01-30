from .models import House, Flat, FlatImage, HouseImage, Tag, Category
from . import db
from loguru import logger


### House CRUD Functions ###
def create_house(name, address, description=None) -> House:
    new_house = House(name=name, address=address, description=description)
    add_and_commit_to_db(new_house)
    return new_house


def get_all_houses() -> list[House]:
    houses = db.session.query(House).all()
    logger.debug(f"Retrieved all houses: {houses}")
    return houses


def filter_houses(**kwargs) -> list[House]:
    filtered_houses = db.session.query(House).filter_by(**kwargs).all()
    logger.debug(f"Filtered houses with parameters {kwargs}: {filtered_houses}")
    return filtered_houses


def get_house_by_id(house_id) -> House | None:
    house = db.session.query(House).get(house_id)
    if house:
        logger.debug(f"Retrieved house by ID {house_id}: {house}")
    else:
        logger.warning(f"No house found with ID {house_id}")
    return house


def get_house_by_name(name) -> House | None:
    house = db.session.query(House).filter_by(name=name).first()
    if house:
        logger.debug(f"Retrieved house by name '{name}': {house}")
    else:
        logger.warning(f"No house found with name '{name}'")
    return house


def update_house(house_id, **kwargs) -> House | None:
    house = get_house_by_id(house_id)
    if house is not None:
        update_and_commit_to_db(house, **kwargs)
        return house
    else:
        logger.warning(f"No house found with ID {house_id} for update")
    return None


def delete_house(house_id) -> bool:
    house = get_house_by_id(house_id)
    if house:
        delete_and_commit_to_db(house)
        return True
    else:
        logger.warning(f"No house found with ID {house_id} for deletion")
    return False


### Flat CRUD Functions ###
def create_flat(
    name,
    description=None,
    house_id=None,
    tags=[],
    tag_names=[],
) -> Flat:
    new_flat = Flat(name=name, description=description, house_id=house_id, tags=tags)

    # Add tags to the flat
    for tag_name in tag_names:
        tag = db.session.query(Tag).filter_by(name=tag_name).first()
        if tag:
            new_flat.tags.append(tag)
        else:
            logger.warning(f"Could not find a tag with name {tag_name}. Skipping that.")

    add_and_commit_to_db(new_flat)
    return new_flat


def get_all_flats() -> list[Flat]:
    flats = db.session.query(Flat).all()
    logger.debug(f"Retrieved all flats: {flats}")
    return flats


def filter_flats(**kwargs) -> list[Flat]:
    filtered_flats = db.session.query(Flat).filter_by(**kwargs).all()
    logger.debug(f"Filtered flats with parameters {kwargs}: {filtered_flats}")
    return filtered_flats


def get_flat_by_id(flat_id) -> Flat | None:
    flat = db.session.query(Flat).get(flat_id)
    if flat:
        logger.debug(f"Retrieved flat by ID {flat_id}: {flat}")
    else:
        logger.warning(f"No flat found with ID {flat_id}")
    return flat


def get_flat_by_name(name) -> Flat | None:
    flat = db.session.query(Flat).filter_by(name=name).first()
    if flat:
        logger.debug(f"Retrieved flat by name '{name}': {flat}")
    else:
        logger.warning(f"No flat found with name '{name}'")
    return flat


def update_flat(flat_id, **kwargs) -> Flat | None:
    flat = get_flat_by_id(flat_id)
    if flat is not None:
        update_and_commit_to_db(flat, **kwargs)
        return flat
    else:
        logger.warning(f"No flat found with ID {flat_id} for update")
    return None


def delete_flat(flat_id) -> bool:
    flat = get_flat_by_id(flat_id)
    if flat:
        delete_and_commit_to_db(flat)
        return True
    else:
        logger.warning(f"No flat found with ID {flat_id} for deletion")
    return False


### FlatImage CRUD Functions ###
def create_flat_image(
    image_url, title=None, description=None, flat_id=None, house_id=None
):
    new_image = FlatImage(
        image_url=image_url,
        title=title,
        description=description,
        flat_id=flat_id,
    )

    add_and_commit_to_db(new_image)
    return new_image


def get_all_flat_images() -> list[FlatImage]:
    logger.debug("Querying all images...")
    return db.session.query(FlatImage).all()


def get_flat_image_by_id(image_id) -> FlatImage | None:
    logger.debug(f"Querying image with id {image_id}...")
    return db.session.query(FlatImage).get(image_id)


def update_flat_image(image_id, **kwargs):
    image = get_flat_image_by_id(image_id)
    if image:
        update_and_commit_to_db(image, **kwargs)
        return image
    return None


def delete_flat_image(image_id) -> bool:
    image = get_flat_image_by_id(image_id)
    if image:
        delete_and_commit_to_db(image)
        return True
    else:
        logger.warning(f"No image found with ID {image_id} for deletion")
    return False


### HouseImage CRUD Functions ###
def create_house_image(image_url, title=None, description=None, house_id=None):
    new_image = HouseImage(
        image_url=image_url,
        title=title,
        description=description,
        house_id=house_id,
    )

    add_and_commit_to_db(new_image)
    return new_image


def get_all_house_images() -> list[HouseImage]:
    logger.debug("Querying all images...")
    return db.session.query(HouseImage).all()


def get_house_image_by_id(image_id) -> HouseImage | None:
    logger.debug(f"Querying image with id {image_id}...")
    return db.session.query(HouseImage).get(image_id)


def update_house_image(image_id, **kwargs):
    image = get_house_image_by_id(image_id)
    if image:
        update_and_commit_to_db(image, **kwargs)
        return image
    return None


def delete_house_image(image_id) -> bool:
    image = get_house_image_by_id(image_id)
    if image:
        delete_and_commit_to_db(image)
        return True
    else:
        logger.warning(f"No image found with ID {image_id} for deletion")
    return False


### Tag CRUD Functions ###
def create_tag(name, category_id) -> Tag:
    existing_tag = db.session.query(Tag).filter_by(name=name).first()
    if existing_tag:
        # TODO maybe overwrite?
        logger.warning(f"Tag with name {name} already exists. Ignoring that.")
        return existing_tag

    new_tag = Tag(name=name, category_id=category_id)
    add_and_commit_to_db(new_tag)
    return new_tag


def get_all_tags() -> list[Tag]:
    logger.debug("Querying all tags...")
    return db.session.query(Tag).all()


def get_tag_by_id(tag_id) -> Tag | None:
    return db.session.query(Tag).get(tag_id)


def update_tag(tag_id, **kwargs) -> Tag | None:
    tag = get_tag_by_id(tag_id)
    if tag:
        update_and_commit_to_db(tag, **kwargs)
        return tag
    else:
        logger.warning(f"No tag found with ID {tag_id} for update")
    return None


def delete_tag(tag_id) -> bool:
    tag = get_tag_by_id(tag_id)
    if tag:
        delete_and_commit_to_db(tag)
        return True
    else:
        logger.warning(f"No tag found with ID {tag_id} for deletion")
    return False


### Category CRUD Functions ###
def create_category(name) -> Category:
    existing_category = db.session.query(Category).filter_by(name=name).first()
    if existing_category:
        logger.warning(f"Category with name {name} already exists. Ignoring that.")
        return existing_category

    new_category = Category(name=name)
    add_and_commit_to_db(new_category)
    return new_category


def get_all_categories() -> list[Category]:
    return db.session.query(Category).all()


def get_category_by_id(category_id) -> Category | None:
    return db.session.query(Category).get(category_id)


def update_category(category_id, **kwargs) -> Category | None:
    category = get_category_by_id(category_id)
    if category:
        update_and_commit_to_db(category, **kwargs)
        return category
    else:
        logger.warning(f"No category found with ID {category_id} for update")
    return None


def delete_category(category_id) -> bool:
    category = get_category_by_id(category_id)
    if category:
        delete_and_commit_to_db(category)
        return True
    else:
        logger.warning(f"No category found with ID {category_id} for deletion")
    return False


# Helper Functions
def add_and_commit_to_db(obj):
    try:
        db.session.add(obj)
        db.session.commit()
        logger.info(f"Created new database object: {obj}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to create database object {obj}. Error: {e}")
        raise


def update_and_commit_to_db(obj, **kwargs):
    print(obj)
    print(kwargs)
    try:
        for key, value in kwargs.items():
            print(key, getattr(obj, key))
            print(value)
            setattr(obj, key, value)

        db.session.commit()
        logger.info(f"Updated database object: {obj}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to update database object {obj}. Error: {e}")
        raise


def delete_and_commit_to_db(obj):
    try:
        db.session.delete(obj)
        db.session.commit()
        logger.info(f"Deleted database object: {obj}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to delete database object {obj}. Error: {e}")
        raise
