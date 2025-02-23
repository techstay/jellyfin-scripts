from argparse import ArgumentParser
from pathlib import Path
from typing import List

from my_utils.my_logger import get_logger

logger = get_logger(__name__)


def main():
    parser = ArgumentParser(description="Renaming And Sorting Subtitles")

    parser.add_argument(
        "show_dir",
        type=str,
        help="The folder of the show",
    )

    args = parser.parse_args()
    folder: str = args.show_dir
    scan_files(Path(folder))


def scan_files(folder: Path):
    video_types = ".mp4 .mkv".split(" ")
    subtitle_types = ".ass .ssa .srt".split(" ")
    videos = [f for f in folder.iterdir() if f.is_file() and f.suffix in video_types]
    subtitles = [
        f for f in folder.iterdir() if f.is_file() and f.suffix in subtitle_types
    ]

    rename_subtitles(videos, subtitles)


def rename_subtitles(videos: List[Path], subtitles: List[Path]):
    from my_utils.my_ai import deepseek_client

    message = (
        "\n".join(f.name for f in videos) + "\n" + "\n".join(f.name for f in subtitles)
    )
    response = deepseek_client.chat(
        Path("prompts/renaming_subtitles_prompt.txt").read_text(), message
    ).collect()

    new_subtitles = response.split("\n")

    if len(new_subtitles) != len(subtitles):
        logger.error("Error: The number of files and new filenames are not equal!")
        logger.error(response)
        return

    for sub, new_sub in zip(subtitles, new_subtitles):
        print(f"{sub.name} => {sub.parent / new_sub}")

    choice = input("Are you sure to rename these files? (y/n)")
    if choice.lower() not in "y yes".split(" "):
        return
    for sub, new_sub in zip(subtitles, new_subtitles):
        sub.rename(sub.parent / new_sub)
        logger.info(f"{sub.name} => {sub.parent / new_sub}")


if __name__ == "__main__":
    main()
