import sys
import os.path

key = None

my_path = os.path.abspath(__file__)
src_path = os.path.dirname(os.path.dirname(my_path))
keyfile_path = os.path.join(src_path, "key.txt")
with open(keyfile_path, "r") as f:
    key = f.readline().strip()

destination_path = os.path.join(
    src_path,
    "register_printer",
    "license",
    "key.py")

with open(destination_path, "w") as f:
    f.write("key = \"" + key + "\"\n")
