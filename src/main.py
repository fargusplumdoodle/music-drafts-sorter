import sys
from pathlib import Path
import arrow
import shutil
import logging

import os
import re

from typing import TYPE_CHECKING, List, Optional

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.DEBUG
)

dry_run = "--dry-run" in sys.argv


class AudioFile:
    supported_types = {"wav", "mp3", "m4a"}

    def __init__(self, path: str, dest_dir: str, artist="Isaac Thiessen"):
        modified_time = arrow.get(os.path.getmtime(path))
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

        # [1:] removes leading period
        self.supported = self.extension[1:] in self.supported_types


def find_audio_files(src: str, dest: str) -> "List[AudioFile]":
    audio_files = []

    for root, _, files in os.walk(src):
        for file_name in files:
            audio_files.append(AudioFile(os.path.join(root, file_name), dest))

    return [file for file in audio_files if file.supported]


def ensure_path(file: AudioFile):
    if dry_run:
        return

    try:
        os.makedirs(file.dest_directory)
        logging.info(f'Created path "{file.dest_directory}"')
    except FileExistsError:
        pass


def move_file(file: AudioFile) -> None:
    ensure_path(file)

    logging.info(
        f'{"DRY_RUN -- " if dry_run else ""}Moving: "{file.src}" to "{file.dest}"'
    )
    if not dry_run:
        shutil.move(file.src, file.dest)


def main(src: str, dest: str) -> None:
    audio_files = find_audio_files(src, dest)

    for file in audio_files:
        move_file(file)


if __name__ == "__main__":
    src = sys.argv[1]
    dest = sys.argv[2]
    main(src, dest)
