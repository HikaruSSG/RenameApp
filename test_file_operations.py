import unittest
import os
import shutil
from file_operations import FileOperations
from pathlib import Path

class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.file1 = os.path.join(self.test_dir, "test1.txt")
        self.file2 = os.path.join(self.test_dir, "test2.txt")
        self.file3 = os.path.join(self.test_dir, "test3.pdf")
        # Create test files
        with open(self.file1, "w") as f:
            f.write("test1")
        with open(self.file2, "w") as f:
            f.write("test2")
        with open(self.file3, "w") as f:
            f.write("test3")

        self.file_operations = FileOperations()
        self.file_operations.set_folder_path(self.test_dir)

    def tearDown(self):
        # Clean up renamed files
        renamed_files = ["new_name1.txt", "new_name2.txt", "new_name3.pdf",
                         "reordered1.pdf", "reordered2.txt", "reordered3.txt"]
        for file in renamed_files:
            file_path = os.path.join(self.test_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
        shutil.rmtree(self.test_dir)

    def test_list_files(self):
        files = self.file_operations.list_files()
        self.assertEqual(len(files), 3)
        file_names = [f[0] for f in files]
        self.assertIn("test1.txt", file_names)
        self.assertIn("test2.txt", file_names)
        self.assertIn("test3.pdf", file_names)

    def test_rename_files(self):
        self.file_operations.rename_files("new_name", ["test1.txt", "test2.txt", "test3.pdf"])
        files = os.listdir(self.test_dir)
        self.assertIn("new_name1.txt", files)
        self.assertIn("new_name2.txt", files)
        self.assertIn("new_name3.pdf", files)
        self.assertFalse(os.path.exists(self.file1))
        self.assertFalse(os.path.exists(self.file2))
        self.assertFalse(os.path.exists(self.file3))

    def test_rename_files_reordered(self):
        self.file_operations.rename_files("reordered", ["test3.pdf", "test1.txt", "test2.txt"])
        files = os.listdir(self.test_dir)
        self.assertEqual(sorted(files), sorted(["reordered1.pdf", "reordered2.txt", "reordered3.txt"]))
        self.assertFalse(os.path.exists(self.file1))
        self.assertFalse(os.path.exists(self.file2))
        self.assertFalse(os.path.exists(self.file3))

    def test_rename_files_manual_order(self):
        self.file_operations.rename_files("manual", ["test2.txt", "test3.pdf", "test1.txt"])
        files = os.listdir(self.test_dir)
        self.assertEqual(sorted(files), sorted(["manual1.txt", "manual2.pdf", "manual3.txt"]))
        self.assertFalse(os.path.exists(self.file1))
        self.assertFalse(os.path.exists(self.file2))
        self.assertFalse(os.path.exists(self.file3))

if __name__ == "__main__":
    unittest.main()
