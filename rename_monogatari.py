from argparse import ArgumentParser
from pathlib import Path
from typing import List

from my_utils.my_logger import get_logger

logger = get_logger(__name__)


def main():
    parser = ArgumentParser(description="Renaming And Sorting Monogatari Series")

    parser.add_argument(
        "show_dir",
        type=str,
        help="The folder of the show",
    )

    args = parser.parse_args()
    folder: str = args.show_dir
    scan_files(Path(folder))


def scan_files(folder: Path):
    file_types = ".mp4 .mkv .ass".split(" ")
    files = [f for f in folder.iterdir() if f.is_file() and f.suffix in file_types]

    rename_files(files)


def rename_files(files: List[Path]):
    from my_utils.my_ai import deepseek_client

    response = deepseek_client.chat(
        Path("prompts/monogatari_sort_prompt.txt").read_text(),
        "\n".join(f.name for f in files),
    ).collect()
    new_files = response.split("\n")

    if len(new_files) != len(files):
        logger.error("The number of files don't match!")
        return

    for file, new_file in zip(files, new_files):
        file.rename(file.parent / new_file)
        logger.info(f"{file.name} => {file.parent / new_file}")


if __name__ == "__main__":
    main()
