import os.path
from tempfile import TemporaryDirectory
from unittest import TestCase

DATASET_ROOT_PATH = os.path.join(
    os.path.dirname(__file__),
    "dataset"
)


class TestRegisterPrinter(TestCase):

    DATASET_PATH = os.path.join(DATASET_ROOT_PATH, "dataset1")

    def test_c_generator(self):
        with TemporaryDirectory() as tmp_dir:
            self.assertTrue(os.path.exists(tmp_dir), "Tmp directory does not exist")

