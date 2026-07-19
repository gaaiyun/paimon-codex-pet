import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "tools" / "validate_atlas.py"
SPEC = importlib.util.spec_from_file_location("validate_atlas", MODULE_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateAtlasTests(unittest.TestCase):
    def test_default_spritesheet_path_follows_pet_manifest(self):
        expected = REPO_ROOT / "pet" / "paimon" / "spritesheet.webp"
        self.assertEqual(VALIDATOR.default_spritesheet_path(), expected)

    def test_validate_accepts_manifest_webp(self):
        self.assertTrue(VALIDATOR.validate(VALIDATOR.default_spritesheet_path()))


if __name__ == "__main__":
    unittest.main()
