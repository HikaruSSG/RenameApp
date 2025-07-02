import os
from pathlib import Path
import re
import errno

class FileNameTooLongError(Exception):
    """Custom exception for when a filename is too long."""
    pass

class FileOperations:
    def __init__(self):
        self.folder_path = None
        self.previous_names = {}

    def set_folder_path(self, folder_path):
        self.folder_path = folder_path

    def list_files(self):
        if not self.folder_path:
            return []

        files = []
        for item in os.listdir(self.folder_path):
            item_path = os.path.join(self.folder_path, item)
            if os.path.isfile(item_path):
                name = item
                file_type = Path(item_path).suffix
                size = os.path.getsize(item_path)
                files.append((name, file_type, size))
        return files

    def rename_files(self, base_name, ordered_files):
        if not self.folder_path:
            return

        for i, file_name in enumerate(ordered_files):
            src = os.path.join(self.folder_path, file_name)
            if os.path.isfile(src):
                file_ext = Path(file_name).suffix
                new_name = base_name + str(i+1) + file_ext
                dst = os.path.join(self.folder_path, new_name)
                self.previous_names[dst] = src
                try:
                    os.rename(src, dst)
                except OSError as e:
                    if e.errno == errno.ENAMETOOLONG:
                        raise FileNameTooLongError(f"The new file name '{new_name}' is too long.")
                    else:
                        raise # Re-raise other OS errors

    def undo_rename(self):
        if not self.folder_path:
            return

        for dst, src in self.previous_names.items():
            if os.path.isfile(dst):
                os.rename(dst, src)
        self.previous_names = {}

    def natural_sort_key(self, s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(r'(\d+)', s)]
