import sys
import arrow
import logging
import os

from pydub import AudioSegment
from pathlib import Path
from typing import List

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO
)

dry_run = "--dry-run" in sys.argv


class AudioFile:
    supported_types = {"wav", "mp3", "m4a"}

    def __init__(self, path: str, dest_dir: str, artist="Isaac Thiessen"):
        modified_time = arrow.get(os.path.getctime(path))

        self.name = Path(path).name
        # [1:] removes leading period
        self.extension = os.path.splitext(path)[1][1:]

        self.year = str(modified_time.year)
        self.month = modified_time.format("MMMM")

        self.tags = {
            "title": Path(path).stem,
            "album": f"{self.year}-{self.month}",
            "artist": artist,
            "year": self.year,
            "month": self.month,
        }

        self.src = path
        self.dest_directory = os.path.join(dest_dir, self.year, self.month)
        self.dest = os.path.join(self.dest_directory, self.tags["title"] + ".mp3")

        self.supported = self.extension in self.supported_types
        self.already_exists = os.path.exists(self.dest)


def find_audio_files(src: str, dest: str) -> "List[AudioFile]":
    audio_files = []

    for root, _, files in os.walk(src):
        for file_name in files:
            file = AudioFile(os.path.join(root, file_name), dest)

            if file.supported and not file.already_exists:
                logging.info(f"Found new file: {file.src}")
                audio_files.append(file)

            elif file.already_exists:
                logging.debug(f"Skipping existing file: {file.src}")

    return audio_files


def ensure_path(file: AudioFile):
    if dry_run:
        return

    try:
        os.makedirs(file.dest_directory)
        logging.info(f'Created path "{file.dest_directory}"')
    except FileExistsError:
        pass


def copy_file(file: AudioFile) -> None:
    ensure_path(file)

    logging.info(
        f'{"DRY_RUN -- " if dry_run else ""}Converting: "{file.src}" to "{file.dest}"'
    )
    if not dry_run:
        sound = AudioSegment.from_file(file.src, format=file.extension)
        sound.export(file.dest, format="mp3", tags=file.tags)


def main(src: str, dest: str) -> None:
    audio_files = find_audio_files(src, dest)

    for file in audio_files:
        if os.path.exists(file.dest):
            logging.info(f"Skipping {file.dest}")
            continue

        copy_file(file)


if __name__ == "__main__":
    src = sys.argv[1]
    dest = sys.argv[2]
    main(src, dest)
