import argparse
import re
from pathlib import Path

from my_utils.my_logger import get_logger

logger = get_logger(__name__)


def main():
    """Rename episodes of a show to comfort jellyfin, format: [show name] SS[season number]E[episode number]"""
    parser = argparse.ArgumentParser(
        description="Rename episodes of a show to comfort jellyfin",
    )

    parser.add_argument(
        "show_dir",
        type=str,
        help="The folder of the show",
    )

    args = parser.parse_args()
    folder: str = args.show_dir
    scan_folder(Path(folder))


def scan_folder(folder: Path):
    reg = re.compile(r"[Ss]eason (\d+)")
    show_name: str = ""
    season: int = 1
    # If current folder is a season folder, then its parent folder is the show name
    if reg.match(folder.name):
        show_name = folder.parent.name
        season = int(reg.match(folder.name).group(1))
        handle_files(folder, show_name, season)
    else:
        sub_folders = [d for d in folder.iterdir() if d.is_dir()]
        show_name = folder.name
        for sub_folder in sub_folders:
            if reg.match(sub_folder.name):
                season = int(reg.match(sub_folder.name).group(1))
                handle_files(sub_folder, show_name, season)

        handle_files(folder, show_name, season)


def handle_files(folder: Path, show_name: str, season: int):

    files = filter_files(folder)

    if len(files) != 0:
        rename_files(files, show_name, season)

    extra_dirs = [
        f
        for f in folder.iterdir()
        if f.is_dir() and f.name.lower() in ["extra", "special"]
    ]

    if len(extra_dirs) > 0:
        for extra_dir in extra_dirs:
            extra_files = filter_files(extra_dir)
            if len(extra_files) > 0:
                rename_files(extra_files, show_name, season)


def filter_files(folder: Path) -> list[Path]:
    file_types = [".mkv", ".mp4", ".ass", ".rmvb", ".ssa", ".srt"]
    return [f for f in folder.iterdir() if f.is_file() and f.suffix in file_types]


def rename_files(file_list: list[Path], show_name: str, season: int):
    """Here length of file_list should be greater than 0"""
    lines = [f"{show_name} 第{season}季"]
    lines.extend(f.name for f in file_list)
    message = "\n".join(lines)

    from my_utils.my_ai import gemini_client as client

    response = (
        client.chat(Path("prompts/renaming_prompt.txt").read_text(), message)
        .collect()
        .strip()
    )

    new_filenames = response.split("\n")
    if len(file_list) != len(new_filenames):
        logger.error("Error: Number of files and new filenames are not equal!")
        return

    for old_file, new_file in zip(file_list, new_filenames):
        old_file.rename(old_file.parent / new_file)
        logger.info(f"{old_file.name} => {new_file}")
    logger.info("Renaming files successfully!")


if __name__ == "__main__":
    main()
