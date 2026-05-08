import logging
import os
from dotenv import load_dotenv
import shutil
from pathlib import Path


def setup_logging():
    logging.basicConfig(
        filename="septima.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def copy_file(src: Path, dest_dir: Path):

    try:
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_file = dest_dir / src.name

        # Brug copyfile hvis du ikke behøver metadata.
        # copy2 forsøger også at kopiere metadata/timestamps.
        shutil.copy2(src, dest_file)

        logging.info(f"File copied successfully from s{src} to {dest_file}")

    except PermissionError as e:
        logging.error(
            f"Permission denied copying {src} to {dest_dir}. "
            f"Check write access, locked files, or read-only destination. Error: {e}"
        )

    except Exception as e:
        logging.error(f"Error copying file from {src} to {dest_dir}: {e}")


def main():
    load_dotenv()
    setup_logging()
    root_source = Path(os.getenv("ROOT_SOURCE", ""))
    root_destination = Path(os.getenv("ROOT_DESTINATION", ""))
    source_destination = {
        Path(root_source / "Ejendomsadministrationen"): root_destination,
        Path(root_source / "Dagplejen"): root_destination,
    }

    for src_dir, dest_dir in source_destination.items():
        if not src_dir.exists():
            logging.error(f"Source folder does not exist: {src_dir}")
            continue

        for src_file in src_dir.iterdir():
            if not src_file.is_file():
                continue

            # Skip Excel temp/lock files
            if src_file.name.startswith("~$"):
                continue

            if src_file.suffix.lower() not in [".xlsx", ".xls"]:
                continue

            copy_file(src_file, dest_dir)


if __name__ == "__main__":
    main()
