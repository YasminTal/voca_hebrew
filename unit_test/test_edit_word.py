import unittest
import json
import os
import sys
from unittest.mock import patch

sys.path.append(os.path.abspath(".."))

import voca_edit
import voca_utils
from constants import TEST_FILE_PATH_CONST as TEST_FILE
from voca_utils import WordExistsError, UnitNotFoundError, WordNotFoundError


class TestVocaEdit(unittest.TestCase):

    def setUp(self):
        # Point voca_edit to use the test file instead of the main one
        if hasattr(voca_edit, "set_file_path"):
            voca_edit.set_file_path(TEST_FILE)

        # Prepare test data
        self.test_data = {
            "unit_1": [
                {"word": "apple", "meaning": "תפוח"}
            ]
        }
        with open(TEST_FILE, "w", encoding="utf-8") as f:
            json.dump(self.test_data, f, ensure_ascii=False, indent=4)

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def load_data(self):
        with open(TEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_add_new_word_success(self):
        voca_edit.add_word(1, "banana", "בננה")
        data = self.load_data()
        self.assertIn({"word": "banana", "meaning": "בננה"}, data["unit_1"])

    def test_add_duplicate_word_fails(self):
        with patch("builtins.print") as mock_print:
            voca_edit.add_word(1, "apple", "תפוח")
            self.assertTrue(any("already exists" in str(call) for call in mock_print.call_args_list))

    def test_update_word_success(self):
        voca_edit.update_word(1, "apple", "תפוח ירוק")
        data = self.load_data()
        updated = next((w for w in data["unit_1"] if w["word"] == "apple"), None)
        self.assertIsNotNone(updated)
        self.assertEqual(updated["meaning"], "תפוח ירוק")

    def test_update_word_not_exists(self):
        with patch("builtins.print") as mock_print:
            voca_edit.update_word(1, "kiwi", "קיווי")
            self.assertTrue(any("does not exist" in str(call) for call in mock_print.call_args_list))

    def test_delete_word_success(self):
        with patch("builtins.input", return_value="y"):
            voca_edit.delete_word(1, "apple")
        data = self.load_data()
        words = [entry["word"] for entry in data["unit_1"]]
        self.assertNotIn("apple", words)

    def test_delete_word_not_found(self):
        with patch("builtins.print") as mock_print, patch("builtins.input", return_value="y"):
            voca_edit.delete_word(1, "kiwi")
            self.assertTrue(any("does not exist" in str(call) for call in mock_print.call_args_list))

    def test_delete_word_cancelled(self):
        with patch("builtins.input", return_value="n"):
            voca_edit.delete_word(1, "apple")
        data = self.load_data()
        words = [entry["word"] for entry in data["unit_1"]]
        self.assertIn("apple", words)


if __name__ == "__main__":
    unittest.main(verbosity=2)
