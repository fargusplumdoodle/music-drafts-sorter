import sys
from pathlib import Path
import arrow
import shutil
import logging

import os
import re

from typing import TYPE_CHECKING, List, Optional

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO
)


class AudioFile:
    supported_types = {"wav", "mp3", "m4a"}

    def __init__(self, path: str, dest_dir: str, artist="Isaac Thiessen"):
        modified_time = arrow.get(os.path.getctime(path))
        self.name = Path(path).name
        self.extension = os.path.splitext(path)[1]

        self.year = str(modified_time.year)
        self.month = modified_time.format("MMMM")

        self.title = Path(path).stem
        self.album = f"{self.year}-{self.month}"
        self.artist = artist

        self.src = path
        self.dest_directory = os.path.join(dest_dir, self.year, self.month)
        self.dest = os.path.join(self.dest_directory, self.name)

        self.supported = self.extension in self.supported_types


def find_audio_files(src: str, dest: str) -> "List[AudioFile]":
    audio_files = []

    for root, _, files in os.walk(src):
        for file_name in files:
            audio_files.append(AudioFile(os.path.join(root, file_name), dest))

    return [file for file in audio_files if file.supported]


def ensure_path(file: AudioFile):
    try:
        os.makedirs(file.dest_directory)
    except FileExistsError:
        pass


def move_file(file: AudioFile, dry_run: bool) -> None:
    logging.info(
        f'{"DRY_RUN -- " if dry_run else ""}Moving: "{file.src}" to "{file.dest})"'
    )

    if not dry_run:
        shutil.move(file.src, file.dest)


def main(src: str, dest: str, dry_run: bool) -> None:
    audio_files = find_audio_files(src, dest)

    for file in audio_files:
        move_file(file, dry_run)


if __name__ == "__main__":
    src = sys.argv[1]
    dest = sys.argv[2]
    dry_run = "--dry-run" in sys.argv
    main(src, dest, dry_run)
