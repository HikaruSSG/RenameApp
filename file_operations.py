import os
from pathlib import Path
import re

class FileOperations:
    def __init__(self):
        self.folder_path = None

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
                os.rename(src, dst)

    def natural_sort_key(self, s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(r'(\d+)', s)]
