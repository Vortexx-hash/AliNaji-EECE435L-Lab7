"""Lab 7 graded activity: test the actual Lab 5 database and Flask API.

Every test starts the app in a temporary working directory. This exercises its
real startup code and SQLite functions without touching the project database.
Sample rows are inserted with SQL so read tests do not depend on insert_user.
"""

from contextlib import closing
from pathlib import Path
import runpy
import sqlite3

import pytest

import database

APP_PATH = Path(__file__).resolve().with_name("app.py")
FIELDS = ("name", "email", "phone", "address", "country")


@pytest.fixture
def database_path(tmp_path, monkeypatch):
    """Redirect Lab 5's relative database.db path to an empty directory."""
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "database.db"
    assert not path.exists()
    return path


@pytest.fixture
def flask_app(database_path):
    """Execute actual app initialization for every test, without a server."""
    app = runpy.run_path(str(APP_PATH), run_name="lab7_test_app")["app"]
    app.config.update(TESTING=True)
    return app


@pytest.fixture
def initialized_db(flask_app, database_path):
    return database_path


@pytest.fixture
def client(flask_app):
    with flask_app.test_client() as test_client:
        yield test_client


@pytest.fixture
def sample_users():
    """Explicit test data based on the Lab 5 John/Jane Doe examples."""
    return [
        {
            "name": "John Doe",
            "email": "johndoe@gmail.com",
            "phone": "067765434567",
            "address": "John Doe Street, Innsbruck",
            "country": "Austria",
        },
        {
            "name": "Jane Doe",
            "email": "janedoe@gmail.com",
            "phone": "03123456",
            "address": "Hamra, Beirut",
            "country": "Lebanon",
        },
    ]


@pytest.fixture
def seeded_users(initialized_db, sample_users):
    """Populate each test independently of the CRUD functions under test."""
    users = []
    with closing(sqlite3.connect(initialized_db)) as conn, conn:
        for user in sample_users:
            cursor = conn.execute(
                "INSERT INTO users (name, email, phone, address, country) "
                "VALUES (?, ?, ?, ?, ?)",
                tuple(user[field] for field in FIELDS),
            )
            users.append({"user_id": cursor.lastrowid, **user})
    return users


def stored_users(path):
    """Read persisted state directly, independently of Lab 5's read helpers."""
    with closing(sqlite3.connect(path)) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute("SELECT * FROM users ORDER BY user_id")]


# Requirement 1: first-run creation and the specified sample users.
def test_database_created_on_first_app_run(initialized_db):
    assert initialized_db.is_file()
    with closing(sqlite3.connect(initialized_db)) as conn:
        columns = conn.execute("PRAGMA table_info(users)").fetchall()
    assert [(c[1], c[2], c[3], c[5]) for c in columns] == [
        ("user_id", "INTEGER", 1, 1),
        *((field, "TEXT", 1, 0) for field in FIELDS),
    ]
    # Lab 5 creates the table, but does not automatically insert seed users.
    assert stored_users(initialized_db) == []


def test_app_startup_preserves_specified_users(initialized_db, seeded_users):
    # A subsequent startup must retain every field of the specified users.
    restarted_app = runpy.run_path(str(APP_PATH), run_name="lab7_restart_app")["app"]
    restarted_app.config.update(TESTING=True)
    response = restarted_app.test_client().get("/api/users")
    assert response.status_code == 200
    assert sorted(response.get_json(), key=lambda user: user["user_id"]) == seeded_users
    assert stored_users(initialized_db) == seeded_users


# Requirements 2-6: database CRUD, verified against independently read SQL rows.
def test_insert_user(initialized_db, sample_users):
    user = sample_users[0]
    inserted = database.insert_user(user)
    assert type(inserted["user_id"]) is int
    assert inserted["user_id"] > 0
    assert inserted == {"user_id": inserted["user_id"], **user}
    assert stored_users(initialized_db) == [inserted]


def test_get_users(initialized_db, seeded_users):
    assert sorted(database.get_users(), key=lambda user: user["user_id"]) == seeded_users


def test_get_users_when_empty(initialized_db):
    assert database.get_users() == []


def test_get_user_by_id(initialized_db, seeded_users):
    for expected in seeded_users:
        assert database.get_user_by_id(expected["user_id"]) == expected


def test_get_user_by_id_when_missing(initialized_db):
    assert database.get_user_by_id(99999) == {}


def test_update_user(initialized_db, seeded_users):
    updated = {
        "user_id": seeded_users[0]["user_id"],
        "name": "Ali Naji",
        "email": "ali.naji@example.com",
        "phone": "07123456",
        "address": "Bliss Street, Beirut",
        "country": "Lebanon",
    }
    assert database.update_user(updated) == updated
    assert stored_users(initialized_db) == [updated, seeded_users[1]]


def test_delete_user(initialized_db, seeded_users):
    message = database.delete_user(seeded_users[0]["user_id"])
    assert message == {"status": "User deleted successfully"}
    assert stored_users(initialized_db) == [seeded_users[1]]


# Requirements 7-10: HTTP status AND complete uploaded/downloaded user data.
def test_api_get_user(client, seeded_users):
    expected = seeded_users[0]
    response = client.get(f"/api/users/{expected['user_id']}")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == expected


def test_api_get_users(client, seeded_users):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.is_json
    assert sorted(response.get_json(), key=lambda user: user["user_id"]) == seeded_users


def test_api_add_user(client, initialized_db, sample_users):
    uploaded = sample_users[0]
    response = client.post("/api/users/add", json=uploaded)
    assert response.status_code == 200
    assert response.is_json
    downloaded = response.get_json()
    assert type(downloaded["user_id"]) is int
    assert downloaded["user_id"] > 0
    assert downloaded == {"user_id": downloaded["user_id"], **uploaded}
    assert stored_users(initialized_db) == [downloaded]


def test_api_update_user(client, initialized_db, seeded_users, sample_users):
    uploaded = {"user_id": seeded_users[0]["user_id"], **sample_users[1]}
    response = client.put("/api/users/update", json=uploaded)
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == uploaded
    assert stored_users(initialized_db) == [uploaded, seeded_users[1]]
    downloaded = client.get(f"/api/users/{uploaded['user_id']}")
    assert downloaded.status_code == 200
    assert downloaded.get_json() == uploaded


def test_api_delete_user(client, initialized_db, seeded_users):
    user_id = seeded_users[0]["user_id"]
    response = client.delete(f"/api/users/delete/{user_id}")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"status": "User deleted successfully"}
    assert stored_users(initialized_db) == [seeded_users[1]]
    downloaded = client.get(f"/api/users/{user_id}")
    assert downloaded.status_code == 404
    assert downloaded.get_json() == {"error": "User not found"}


# Additional checks of Lab 5's existing error responses and full API workflow.
@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_api_missing_user(client, sample_users, method):
    if method == "put":
        response = client.put(
            "/api/users/update", json={"user_id": 99999, **sample_users[0]}
        )
    else:
        url = "/api/users/99999" if method == "get" else "/api/users/delete/99999"
        response = getattr(client, method)(url)
    assert response.status_code == 404
    assert response.get_json() == {"error": "User not found"}


@pytest.mark.parametrize("field", FIELDS)
def test_api_rejects_missing_user_fields(client, initialized_db, sample_users, field):
    uploaded = dict(sample_users[0])
    del uploaded[field]
    response = client.post("/api/users/add", json=uploaded)
    assert response.status_code == 400
    assert response.get_json() == {"error": f"{field} must be a non-empty string."}
    assert stored_users(initialized_db) == []


def test_api_rejects_invalid_update_id(client, initialized_db, seeded_users, sample_users):
    response = client.put(
        "/api/users/update", json={"user_id": "1", **sample_users[0]}
    )
    assert response.status_code == 400
    assert response.get_json() == {"error": "user_id must be a positive integer."}
    assert stored_users(initialized_db) == seeded_users


def test_api_crud_lifecycle(client, sample_users):
    added = client.post("/api/users/add", json=sample_users[0])
    assert added.status_code == 200
    user = added.get_json()
    assert user == {"user_id": user["user_id"], **sample_users[0]}
    user_id = user["user_id"]

    fetched = client.get(f"/api/users/{user_id}")
    assert fetched.status_code == 200
    assert fetched.get_json() == user

    updated = {"user_id": user_id, **sample_users[1]}
    changed = client.put("/api/users/update", json=updated)
    assert changed.status_code == 200
    assert changed.get_json() == updated
    listed = client.get("/api/users")
    assert listed.status_code == 200
    assert listed.get_json() == [updated]

    deleted = client.delete(f"/api/users/delete/{user_id}")
    assert deleted.status_code == 200
    assert deleted.get_json() == {"status": "User deleted successfully"}
    missing = client.get(f"/api/users/{user_id}")
    assert missing.status_code == 404
    assert missing.get_json() == {"error": "User not found"}
    listed = client.get("/api/users")
    assert listed.status_code == 200
    assert listed.get_json() == []
