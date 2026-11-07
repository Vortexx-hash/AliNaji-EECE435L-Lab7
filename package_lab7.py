"""Build the Moodle submission ZIP without environments or Git internals."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
PROJECT_NAME = "Lab7-Ali-Naji"
PROJECT_FILES = (
    "app.py",
    "database.py",
    "database.db",
    "capitalize.py",
    "wallet.py",
    "hello_add.py",
    "test_user_Ali_Naji.py",
    "test_capitalize.py",
    "test_wallet.py",
    "test_hello_add.py",
    "requirements.txt",
    "requirements-dev.txt",
    "README.md",
    "SUBMISSION.md",
    "package_lab7.py",
    ".gitignore",
    "screenshots/.gitkeep",
)


def main():
    files = [ROOT / name for name in PROJECT_FILES]
    files.extend(sorted((ROOT / "postman").glob("*.json")))
    screenshots = sorted(
        path for path in (ROOT / "screenshots").glob("*")
        if path.suffix.lower() in {".png", ".jpg", ".jpeg"} and path.is_file()
    )
    files.extend(screenshots)
    # Fail before opening the output ZIP if a required file is missing.
    for path in files:
        if not path.is_file():
            raise FileNotFoundError(f"Missing project file: {path}")

    output = ROOT / "dist" / f"{PROJECT_NAME}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, str(Path(PROJECT_NAME) / path.relative_to(ROOT)))
    print(f"Created: {output}")
    print(f"Included {len(files)} files under {PROJECT_NAME}/")
    if not screenshots:
        print("Screenshot still needed: save it in screenshots/, then rerun this script.")


if __name__ == "__main__":
    main()
