from apps.users.service import create_usr, delete_usr, get_by_id, get_by_email, get_all
from tests.connect import db
from apps.users.schema import UserCreate, UserUpdate

def test_create_user(db):
    user_data = {
        "name": "Billy Jean",
        "first_name": "Billy",
        "last_name": "Jean",
        "email": "billy.jean@example.com",
        "age": 30,
        "address": "Calle Siempre Viva"
    }
    user_data_set = UserCreate(**user_data)
    db_user = create_usr(db, user_data_set)
    assert db_user.id is not None
    assert db_user.email == "billy.jean@example.com"


def test_get_by_id(db):
    user_data = {
        "name": "Michael Smith",
        "first_name": "Michael",
        "last_name": "Smith",
        "email": "michael.smith@example.com",
        "age": 28,
        "address": "Calle Siempre Viva"
    }
    user_data_set = UserCreate(**user_data)
    db_user = create_usr(db, user_data_set)
    current_user = get_by_id(db, db_user.id)
    assert current_user.id == db_user.id
    assert current_user.email == "michael.smith@example.com"

def test_get_by_email(db):
    user_data = {
        "name": "Jake Johnson",
        "first_name": "Jake",
        "last_name": "Johnson",
        "email": "jake.johnson@example.com",
        "age": 35,
        "address": "Calle Siempre Viva"
    }
    user_data_set = UserCreate(**user_data)
    db_user = create_usr(db, user_data_set)
    fetched_user = get_by_email(db, "jake.johnson@example.com")
    assert fetched_user.id == db_user.id
    assert fetched_user.email == "jake.johnson@example.com"

def test_get_all(db):
    user_data_1 = {
        "name": "Lucas Brown",
        "first_name": "Lucas",
        "last_name": "Brown",
        "email": "lucas.brown@example.com",
        "age": 30,
        "address": "123 Main St"
    }
    user_data_2 = {
        "name": "Hilary Davis",
        "first_name": "Hilary",
        "last_name": "Davis",
        "email": "hilary.davis@example.com",
        "age": 28,
        "address": "456 Main St"
    }
    user_data_set1 = UserCreate(**user_data_1)
    user_data_set1 = UserCreate(**user_data_2)
    create_usr(db, user_data_set1)
    create_usr(db, user_data_set1)
    users = get_all(db)
    assert len(users) >= 2

def test_delete_user(db):
    user_data = {
        "name": "Jill Miller",
        "first_name": "Jill",
        "last_name": "Miller",
        "email": "jill.miller@example.com",
        "age": 25,
        "address": "654 Main St"
    }
    user_data_set = UserCreate(**user_data)
    db_user = create_usr(db, user_data_set)
    delete_usr(db, db_user.id)
    assert get_by_id(db, db_user.id) is None
