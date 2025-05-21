
import os 
import json

class VocaError(Exception):
    pass

class EmptyFieldError(VocaError):
    pass

class FileNotFoundError(VocaError):
    pass

class UnitNotFoundError(VocaError):
    pass

class WordExistsError(VocaError):
    pass

class WordNotFoundError(VocaError):
    pass



def unit_exists(data, unit):
     if unit not in data:
        raise UnitNotFoundError(f"Unit '{unit}' does not exist.")
     
def word_exists_check(data, unit, word):
    return any(entry["word"] == word for entry in data[unit])

def word_exists(data, unit, word):
   if not word_exists_check(data, unit, word):
        raise WordNotFoundError(f"The word '{word}' does not exist in unit '{unit}'.")
      
def word_not_exists(data, unit, word):
    if word_exists_check(data, unit, word):
        raise WordExistsError(f"The word '{word}' already exists in unit '{unit}'.")

def to_lower(*args):
    return [arg.lower() for arg in args]

def unit_key(unit_number):
    return f"unit_{unit_number}".lower()

def is_valid_word_and_meaning(word, meaning):
      if not word.strip() or not meaning.strip():
        raise EmptyFieldError("Word and meaning cannot be empty.")