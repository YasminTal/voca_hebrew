import unittest
import sys
import os
sys.path.append(os.path.abspath(".."))

import voca_utils
class TestVocaUtils(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            "unit_1": [
                {"word": "apple", "meaning": "תפוח"},
                {"word": "banana", "meaning": "בננה"}
            ]
        }

     # --- to_lower
    def test_to_lower(self):
     result = voca_utils.to_lower("HeLLo", "WorLD")

     self.assertEqual(result, ["hello", "world"])

 # --- unit_key
    def test_unit_key(self):
        self.assertEqual(voca_utils.unit_key(1), "unit_1")

    # --- is_valid_word_and_meaning
    def test_valid_word_and_meaning_pass(self):
        voca_utils.is_valid_word_and_meaning("apple", "fruit")  # should not raise

    def test_valid_word_and_meaning_fail(self):
        with self.assertRaises(voca_utils.EmptyFieldError):
                voca_utils.is_valid_word_and_meaning("", "meaning")

    # --- unit_exists
    def test_unit_exists_pass(self):
        voca_utils.unit_exists(self.sample_data, "unit_1")

    def test_unit_exists_fail(self):
        with self.assertRaises(voca_utils.UnitNotFoundError):
                voca_utils.unit_exists(self.sample_data, "unit_5")

    # --- word_exists_check
    def test_word_exists_check_true(self):
        result = voca_utils.word_exists_check(self.sample_data, "unit_1", "apple")
        self.assertTrue(result)

    def test_word_exists_check_false(self):
        result = voca_utils.word_exists_check(self.sample_data, "unit_1", "grape")
        self.assertFalse(result)

    # --- word_exists (validator)
    def test_word_exists_pass(self):
        voca_utils.word_exists(self.sample_data, "unit_1", "banana")

    def test_word_exists_fail(self):
        with self.assertRaises(voca_utils.WordNotFoundError):
            voca_utils.word_exists(self.sample_data, "unit_1", "grape")

    # --- word_not_exists (validator)
    def test_word_not_exists_pass(self):
        voca_utils.word_not_exists(self.sample_data, "unit_1", "grape")

    def test_word_not_exists_fail(self):
        with self.assertRaises(voca_utils.WordExistsError):
            voca_utils.word_not_exists(self.sample_data, "unit_1", "banana")


if __name__ == "__main__":
     unittest.main(verbosity=2)