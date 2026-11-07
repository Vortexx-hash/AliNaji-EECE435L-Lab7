# Lab7-Ali-Naji Python testing

Lab 7 builds on the Lab 5 Flask user API and SQLite database. The graded test
file is `test_user_Ali_Naji.py`. It tests the existing `app.py` and `database.py`
directly, including real SQLite persistence and complete JSON request/response
data. The handout's capitalization, wallet, and Flask-add exercises are included.

## Setup and testing

Use Python 3.10 or newer. Open PowerShell in the project folder:

```powershell
# Only needed if a virtual environment does not already exist:
python -m venv venv

.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\venv\Scripts\python.exe -m pytest -v
```

Expected result: **33 passed**. No Flask server or Postman session is needed.
To run only the graded activity:

```powershell
.\venv\Scripts\python.exe -m pytest -v test_user_Ali_Naji.py
```

Expected result: **24 passed**. Use `python -m pytest` with the environment's
Python executable so the correct interpreter and local modules are used.

## Graded requirements

| Handout requirement | Tests in `test_user_Ali_Naji.py` |
| --- | --- |
| 1. First-run database and specified users | `test_database_created_on_first_app_run`, `test_app_startup_preserves_specified_users` |
| 2. Insert_user() | `test_insert_user` |
| 3. Get_users() | `test_get_users`, `test_get_users_when_empty` |
| 4. Get_users_by_id() | `test_get_user_by_id`, `test_get_user_by_id_when_missing` |
| 5. Update_user() | `test_update_user` |
| 6. Delete_user() | `test_delete_user` |
| 7. Api_get_user() | `test_api_get_user`, `test_api_get_users` |
| 8. Api_add_user() | `test_api_add_user` |
| 9. Api_update_user() | `test_api_update_user` |
| 10. Api_delete_user() | `test_api_delete_user` |

The handout calls item 4 `Get_users_by_id()`; the actual Lab 5 function is named
`get_user_by_id()`, which is the function tested. Additional cases cover missing
users, each missing required field, an invalid update ID, and a full API CRUD
lifecycle. Successful responses use HTTP 200, matching the existing Lab 5 app.
Every API test checks both the status code and response data. Write-operation
tests also check persisted data independently through SQL, and ensure that
unrelated users remain intact.

### Initial database and sample data

The Lab 5 startup calls `create_db_table()` and creates an **empty** users table
if needed. Neither handout specifies an automatic seed list, and the existing
app does not insert one. Lab 7 keeps that startup behavior.

The first startup test begins with no database file and verifies creation of
the exact users schema. A separate fixture inserts explicit John Doe and Jane
Doe test records, based on the Lab 5 examples. The startup-preservation test
starts the app again and checks that those complete records are retained.

Each graded test runs app initialization in its own pytest `tmp_path` directory.
`monkeypatch` redirects Lab 5's relative `database.db` path and restores the
working directory afterward. Fixtures insert sample rows directly with SQL so
retrieval tests do not depend on the insert function being correct. Assertions
use generated IDs. No tests change the repository's existing `database.db`.

## Handout exercises

| Files | Demonstrated behavior |
| --- | --- |
| `capitalize.py`, `test_capitalize.py` | Capitalization, friendly `TypeError`, acceptance of string subclasses |
| `wallet.py`, `test_wallet.py` | Initial balances, add/spend methods, insufficient balance exception, fixtures |
| `hello_add.py`, `test_hello_add.py` | JSON POST `/add`, HTTP 200, `{"sum": 3}` |

The wallet tests use the final fixture-based form of the handout's five tests.
The tutorial applications follow the behaviors taught in the examples.

## Screenshot and submission

See [SUBMISSION.md](SUBMISSION.md) for step-by-step run instructions, the exact
terminal screenshot to take, Moodle uploads, and Git commit/push commands.

To build the submission ZIP:

```powershell
.\venv\Scripts\python.exe package_lab7.py
```

Output: `dist/Lab7-Ali-Naji.zip`. Save your real passing-test screenshot in
`screenshots/` and rerun the packager to include it. The archive includes all
project code and dependencies lists, with the required project folder name.

## Run the original Lab 5 API manually

This is optional for Lab 7 testing:

```powershell
.\venv\Scripts\python.exe app.py
```

Run from the project root because Lab 5 opens `database.db` relative to the
current directory. The API is available at `http://127.0.0.1:5000`:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/users` | List users |
| GET | `/api/users/<user_id>` | Get one user |
| POST | `/api/users/add` | Add a user |
| PUT | `/api/users/update` | Update a user |
| DELETE | `/api/users/delete/<user_id>` | Delete a user |

POST and PUT require non-empty string fields `name`, `email`, `phone`,
`address`, and `country`. PUT also requires a positive integer `user_id`.
Missing users return 404; invalid fields return 400. The `/` path has no route.

The existing Postman exports are retained in:

- `postman/AliNaji_Flask_User_App_Collection.json`
- `postman/AliNaji_FlaskCollection_environment.json`

The separate addition example can be run with
`.\venv\Scripts\python.exe hello_add.py`; its `/add` endpoint uses port 5001.
