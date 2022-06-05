import os
import re

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .custom_types import FileStructure

supported_types = [
    re.compile(r".*\.wav"),
    re.compile(r".*\.mp3"),
    re.compile(r".*\.m4a"),
]


def is_supported(file_name: str) -> bool:
    for supported_type in supported_types:
        if supported_type.match(file_name):
            return True

    return False


def find_files(src: str) -> "FileStructure":
    audio_files = []
    for root, _, files in os.walk(src):
        for file in files
            if is_supported(file)


    pass
