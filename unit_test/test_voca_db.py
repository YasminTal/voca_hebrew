import unittest
import os
import json
import sys

import io
from contextlib import redirect_stdout

sys.path.append(os.path.abspath(".."))

import voca_db
from constants import TEST_FILE_PATH_CONST as TEST_FILE


class TestVocaDB(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            "unit_1": [
                {"word": "apple", "meaning": "תפוח"},
                {"word": "banana", "meaning": "בננה"}
            ]
        }
        with open(TEST_FILE, "w", encoding="utf-8") as f:
            json.dump(self.sample_data, f, ensure_ascii=False, indent=4)

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_file_exists_pass(self):
        voca_db.file_exists(TEST_FILE)  # should not raise

    def test_file_exists_fail(self):
        with self.assertRaises(FileNotFoundError):
            voca_db.file_exists("non_existing_file.json")

    def test_load_data(self):
        data = voca_db.load_data(TEST_FILE)
        self.assertEqual(data, self.sample_data)

    def test_save_data(self):
        new_data = {"unit_2": [{"word": "cherry", "meaning": "דובדבן"}]}
        voca_db.save_data(TEST_FILE, new_data)
        with open(TEST_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        self.assertEqual(loaded, new_data)

    def test_append_word(self):
        voca_db.append_word(self.sample_data, "unit_1", "kiwi", "קיווי")
        self.assertIn({"word": "kiwi", "meaning": "קיווי"}, self.sample_data["unit_1"])

    def test_update_word_in_unit_success(self):
        result = voca_db.update_word_in_unit(self.sample_data, "unit_1", "apple", "תפוח ירוק")
        self.assertTrue(result)
        self.assertEqual(self.sample_data["unit_1"][0]["meaning"], "תפוח ירוק")

    def test_update_word_in_unit_fail(self):
        result = voca_db.update_word_in_unit(self.sample_data, "unit_1", "kiwi", "קיווי")
        self.assertFalse(result)

    def test_delete_word_success(self):
        result = voca_db.delete_word(self.sample_data, "unit_1", "apple")
        self.assertTrue(result)
        words = [entry["word"] for entry in self.sample_data["unit_1"]]
        self.assertNotIn("apple", words)

    def test_delete_word_fail(self):
        original_len = len(self.sample_data["unit_1"])
        result = voca_db.delete_word(self.sample_data, "unit_1", "kiwi")
        self.assertFalse(result)
        self.assertEqual(len(self.sample_data["unit_1"]), original_len)

def test_print_list_output(self):
    expected_output = (
        "\n📘 Words in unit_1:\n"
        "  - apple : תפוח\n"
        "  - banana : בננה\n\n"
    )
    f = io.StringIO()
    with redirect_stdout(f):
        voca_db.print_list("unit_1", self.sample_data)
    output = f.getvalue()
    self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
