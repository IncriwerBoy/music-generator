from src.logger import logging
from src.exception import CustomException
import pickle
import sys

def save_object(file_path, object):
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(object, file)
            logging.info('Object Dumped')
        
    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, 'rb') as file:
            logging.info('Object Loaded')
            return pickle.load(file)
    
    except Exception as e:
        raise CustomException(e, sys)


def note_to_int(pitchnames):
    noted_int = dict((note, num) for num, note in enumerate(pitchnames))
    return noted_int

def int_to_note(pitchnames):
    int_noted = dict((number, note) for number, note in enumerate(pitchnames))
    return int_noted