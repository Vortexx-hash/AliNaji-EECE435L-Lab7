# Lab7-Ali-Naji submission guide

The graded activity on pages 8-9 of `Lab 7-Python testing.pdf` requires the
personalized pytest file, a zipped project, and a screenshot of successful tests.
The examples on pages 1-8 are also implemented in this project.

## 1. Install and run

Open this folder in VS Code, then choose **Terminal > New Terminal** with
PowerShell. Run:

```powershell
Set-Location 'C:\Users\AliNaji\Desktop\EECE435L\Lab7'
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\venv\Scripts\python.exe -m pytest -v
```

The existing `venv` is ready on this computer. On another computer, run
`python -m venv venv` before installing dependencies. Python 3.10 or newer is
required by the pinned pytest version. Activation is optional.

There is no need to start `app.py` or open Postman to run these tests. The API
tests execute the Lab 5 app with Flask's test client. Each graded test gets a
fresh temporary SQLite database; `database.db` in the project is preserved.

## 2. Capture the required screenshot

The handout requires a successful pytest terminal screenshot like page 9.
Capture your actual run, with the project identity and passing summary visible.

1. Expand the terminal panel so that its output is readable.
2. Run these commands for the **graded activity**:

   ```powershell
   Clear-Host
   Write-Host 'Lab7-Ali-Naji - graded user database and API tests'
   .\venv\Scripts\python.exe -m pytest test_user_Ali_Naji.py --color=yes
   ```

3. Wait for the green passing summary and the PowerShell prompt to return.
   Include the command, `test_user_Ali_Naji.py`, `[100%]`, and the final
   `24 passed` line in the screenshot. No failures or errors should appear.
4. Press **Win + Shift + S**, select the terminal area, open the capture,
   and save it as `screenshots/Lab7-Ali-Naji-pytest.png`.
5. Optionally capture all exercises too:

   ```powershell
   Clear-Host
   Write-Host 'Lab7-Ali-Naji - all Lab 7 exercises'
   .\venv\Scripts\python.exe -m pytest --color=yes
   ```

   Save this second image as `screenshots/Lab7-Ali-Naji-all-tests.png`.
   It should show all four test filenames and `33 passed`.

The first screenshot is sufficient for the stated graded activity. Postman and
browser screenshots are not requested for Lab 7. If you want more detailed
evidence, use `-v` and take multiple captures showing the test names and summary.

## 3. Build the Moodle ZIP

After saving your screenshot, run:

```powershell
.\venv\Scripts\python.exe package_lab7.py
```

This creates `dist/Lab7-Ali-Naji.zip`, containing a top-level folder named
`Lab7-Ali-Naji` with all project code, requirements, the Lab 5 database and
Postman exports, documentation, and any PNG/JPG screenshots in `screenshots/`.
It excludes `venv`, `.git`, caches, temporary files, and old lab handouts.
The ZIP is a generated submission file and is ignored by Git.

Upload to Moodle:

1. `dist/Lab7-Ali-Naji.zip`.
2. `screenshots/Lab7-Ali-Naji-pytest.png` as the separately requested snapshot.

You can generate the ZIP before taking screenshots, but rerun the packager
after saving them so the archive also includes the evidence.

## 4. Commit and push to GitHub

This checkout's existing remote is:
`https://github.com/Vortexx-hash/AliNaji-EECE435L-Lab5.git`.
Use a Lab 7 branch to keep this work easy to identify in that repository.
The lab handout asks for Moodle uploads; pushing GitHub is your additional
requested workflow. No commit or push has been made automatically.

Run from this project folder, after saving the screenshot:

```powershell
git switch -c lab7-python-testing
git add .gitignore README.md requirements-dev.txt SUBMISSION.md package_lab7.py
git add capitalize.py test_capitalize.py wallet.py test_wallet.py
git add hello_add.py test_hello_add.py test_user_Ali_Naji.py screenshots
git diff --cached --stat
git diff --cached
git commit -m "Complete Lab 7 pytest exercises and user API tests"
git push -u origin lab7-python-testing
```

If that branch already exists, use `git switch lab7-python-testing` instead of
creating it. The `app.py`, `database.py`, `database.db`, `requirements.txt`, and
Postman exports are already tracked from Lab 5 and are reused unchanged.

Do not use `git add .`: the folder also contains the untracked Lab 7 handout and
an old Lab 5 repository-link text file, neither of which is needed for this
commit. Do not commit the virtual environment, caches, or `dist/` archive.

After pushing, open GitHub, select branch `lab7-python-testing`, and verify that
`test_user_Ali_Naji.py`, `requirements-dev.txt`, and your screenshot are visible.
If your instructor expects this on `main`, open a pull request from the Lab 7
branch to `main`, review it, and merge it.
