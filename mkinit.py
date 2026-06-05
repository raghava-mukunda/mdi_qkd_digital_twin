from pathlib import Path

PROJECT_ROOT = Path(".")

folders = [
    "config",
    "source",
    "modulators",
    "channel",
    "synchronization",
    "interference",
    "detectors",
    "bsm",
    "statistics",
    "skr",
    "validation",
    "visualization",
    "tests"
]

for folder in folders:

    folder_path = PROJECT_ROOT / folder

    if folder_path.exists():

        init_file = folder_path / "__init__.py"

        init_file.touch(exist_ok=True)

        print(f"Created: {init_file}")

    else:

        print(f"Folder not found: {folder}")

print("\nDone.")
