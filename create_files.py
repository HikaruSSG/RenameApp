import os

def create_files(directory, num_files):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(1, num_files + 1):
        filename = os.path.join(directory, f"file {i}.txt")
        with open(filename, "w") as f:
            f.write(f"This is file {i}.")

if __name__ == "__main__":
    create_files("sample files", 24)
