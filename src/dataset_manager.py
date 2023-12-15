"""
DatasetManager class is responsible for managing dataset.
That includes operations like sanitizing song titles and
music bands names, store them in proper directory tree,
counting songs, creating samples
"""

import os
import shutil
import posixpath
import re

class DatasetManager:
    """
    Class representing a renamer for data files and directories.
    Output format for songs is snake_case for author and song name
    separated by dash: author-song_name
    Output format for album names is also snake case: album_name
    """

    def __init__(self, path: str):
        self._path = path
        self._artists = dict()
        self._songs_to_take_per_artist = -1


    def set_path(self, path: str):
        """
        Set new path
        """

        self._path = path


    def get_artists(self) -> dict:
        """
        Get dictionary containing artists names and their songs count
        """
        return self._artists


    def create_dataset(self):
        """
        Method which starts creating a dataset from directory containing song albums
        It it responsible for sanitizng music bands names, albums names and song titles - 
        removing whitespaces, numbers that starts names, converting to snake_case etc.
        Output format is snake_case for author and song name separated
        by dash: author-song_name
        """
        self._sanitaze_names()
        self._move()
        self._remove_directory(self._path)
        self._count_songs_per_artist()
        self._minimum_songs_per_artists()


    def _sanitaze_names(self):
        self._sanitize(self._path)


    def _sanitize(self, path: str):
        item_path = self._convert_backslashes_to_forward_slashes(path)
        items = os.listdir(item_path)
        for item in items:
            item_path = posixpath.join(path, item)
            if os.path.isdir(item_path):
                self._sanitize(item_path)
                self._sanitize_directory(item_path)
            else:
                self._sanitize_filename(item, item_path)


    def _convert_backslashes_to_forward_slashes(self, path: str) -> str:
        return path.replace('\\', '/')


    def _get_name(self, path: str) -> str:
        return path.split('/')[-1]


    def _sanitize_directory(self, path: str):
        directory_name = self._get_name(path)
        updated_directory_name, new_path = self._remove_album_year(directory_name, path)
        self._to_snake_case(updated_directory_name, new_path, False)


    def _sanitize_filename(self, filename: str, path: str):
        new_filename = filename
        new_filename = self._remove_order_number(new_filename)
        new_filename = self._remove_non_alphanumeric_at_begin(new_filename)
        self._to_snake_case(new_filename, path, True)


    def _remove_album_year(self, name: str, path: str) -> str | str:
        new_path = path
        new_name = name
        new_name = re.sub(r'[\(\[].*?[\)\]] ', '', new_name)
        if new_name == name:
            new_name = re.sub(r'[\(\[].*?[\)\]]', '', new_name)

        if new_name != name:
            new_path = self._rename_directory(new_name, path)

        return new_name, new_path


    def _to_snake_case(self, name: str, path: str, is_file: bool):
        new_name = name
        new_name = self._remove_whitespaces_around_dash(new_name)
        new_name = self._replace_whitespaces_with_underscores(new_name)
        new_name = self._to_lowercase(new_name)
        if is_file:
            self._rename_file(new_name, path)
        else:
            self._rename_directory(new_name, path)


    def _remove_whitespaces_around_dash(self, name: str) -> str:
        new_name = name
        new_name = new_name.replace(" - ", "-")
        return new_name


    def _replace_whitespaces_with_underscores(self, name: str) -> str:
        new_name = name
        new_name = new_name.replace(" ", "_")
        return new_name


    def _to_lowercase(self, name: str) -> str:
        new_name = name
        new_name = new_name.lower()
        return new_name


    def _remove_order_number(self, filename: str) -> str:
        new_filename = filename
        while self._check_if_filename_starts_with_number(new_filename):
            new_filename = new_filename[1:]
        return new_filename


    def _remove_non_alphanumeric_at_begin(self, filename) -> str:
        new_filename = filename
        while not self._check_if_filename_starts_with_alphanumeric(new_filename):
            new_filename = new_filename[1:]
        return new_filename


    def _check_if_filename_starts_with_number(self, filename: str) -> bool:
        return filename[0].isdigit()


    def _check_if_filename_starts_with_alphanumeric(self, filename: str) -> bool:
        return filename[0].isalpha()


    def _rename_directory(self, new_name: str, path: str) -> str:
        old_name = self._get_name(path)
        new_path = new_name.join(path.rsplit(old_name, 1))
        try:
            os.rename(path, new_path)
            return new_path
        except FileNotFoundError as exc:
            print(f"Can't rename the {old_name} directory")
            raise exc


    def _rename_file(self, new_name: str, path: str):
        old_name = self._get_name(path)
        new_path = path.replace(old_name, new_name)
        try:
            os.rename(path, new_path)
        except FileNotFoundError as exc:
            print(f"Can't rename the {old_name} file")
            raise exc


    def _move(self):
        sanitized_path = self._convert_backslashes_to_forward_slashes(self._path)
        for root, _, files in os.walk(sanitized_path):
            root = self._convert_backslashes_to_forward_slashes(root)
            for file in files:
                item_path = root + "/" + file
                if self._check_if_mp3(item_path):
                    directory_name = self._get_name(root)
                    destination_path = "".join(root.rsplit(directory_name, 1))
                    self._move_file(item_path, destination_path)


    def _check_if_mp3(self, path: str) -> bool:
        if path.lower().endswith(".mp3"):
            return True
        else:
            return False


    def _move_file(self, old_path: str, destination_path: str):
        if destination_path != self._path:
            try:
                shutil.move(old_path, destination_path)
            except shutil.Error:
                print(f"Problems with copying {old_path} to {destination_path}. Removing file")
                os.remove(old_path)


    def _remove_directory(self, path: str):
        item_path = self._convert_backslashes_to_forward_slashes(path)
        items = os.listdir(item_path)
        for item in items:
            item_path = posixpath.join(path, item)
            if os.path.isdir(item_path):
                self._remove_directory(item_path)
                content = os.listdir(item_path)
                if not self._check_if_mp3_in_directory(content):
                    shutil.rmtree(item_path)


    def _check_if_mp3_in_directory(self, directory_content: list) -> bool:
        is_mp3_in_directory_content = False
        for item in directory_content:
            if self._check_if_mp3(item):
                is_mp3_in_directory_content = True
                break

        return is_mp3_in_directory_content


    def _count_songs_per_artist(self):
        sanitized_path = self._convert_backslashes_to_forward_slashes(self._path)
        for root, _, files in os.walk(sanitized_path):
            root = self._convert_backslashes_to_forward_slashes(root)
            directory_name = self._get_name(root)
            if len(directory_name) != 0:
                self._artists[directory_name] = len(files)


    def _minimum_songs_per_artists(self):
        self._songs_to_take_per_artist = min(self._artists.values())
        print(self._songs_to_take_per_artist)
