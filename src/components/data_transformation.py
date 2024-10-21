from music21 import converter, instrument, note, chord
import glob
import sys
from components.model_trainer import ModelTrainer
from exception import CustomException
from logger import logging
from utils import save_object, note_to_int, load_object
import numpy as np
from dataclasses import dataclass
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split


@dataclass
class DataTransformationConfig:
    sequence_length = 100

class DataIngestion:
    def __init__(self):
        pass
    
    def initiate_Data_ingestion(self):
        try:
            notes = []
            # cnt = 1
            for file in glob.glob("../music_midi/*.mid"):
                # if cnt % 25 == 0:
                #     print(cnt)
                
                midi = converter.parse(file)
                notes_to_parse = None
                
                parts = instrument.partitionByInstrument(midi)
                
                #file has instruments part
                if parts:
                    notes_to_parse = parts.parts[0].recurse()
                else:
                    notes_to_parse = midi.flat.notes
                    
                
                for element in notes_to_parse:
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        notes.append('.'.join(str(n) for n in element.normalOrder))
                
                # cnt += 1
            
            logging.info("Notes are parsed from the MIDI files.")
            
            #get all pitch names
            pitchnames = sorted(set(pitch for pitch in notes))
            
            save_object(
                file_path='../artifacts/notes_list.pkl',
                object=notes
            )
            
            save_object(
                file_path='../artifacts/pitchnames.pkl',
                object=pitchnames
            )
        
        except Exception as e:
            raise CustomException(e, sys)
        
        return pitchnames, notes


class DataTransformation():
    def __init__(self):
        self.seq_len = DataTransformationConfig().sequence_length
        self.data_ingestion_obj = DataIngestion()
    
    def get_input_transformation(self):
        try:
            net_input = []
            net_output = []
            pitchnames, notes = self.data_ingestion_obj.initiate_Data_ingestion()
            n_vocab = len(pitchnames)
            
            #create a dict to map pitches to integer
            noted_int = note_to_int(pitchnames)

            logging.info("Converting notes into sequence")
            #create input seq and the corresponding outputs
            for i in range(0, len(notes) - self.seq_len):
                seq_in = notes[i : i + self.seq_len]
                seq_out = notes[i + self.seq_len]

                net_input.append([noted_int[char] for char in seq_in])
                net_output.append(noted_int[seq_out])
                
            net_input = np.array(net_input)
            net_output = np.array(net_output)
            
            save_object(
                file_path="../artifacts/net_input.pkl",
                object=net_input
            )
            
            logging.info("Notes converted to sequence pattern successfully")
        
        except Exception as e:
            raise CustomException(e, sys)
        
        return net_input, net_output, n_vocab
    def initiate_data_transformation(self):
        try:
            net_input, net_output, n_vocab = self.get_input_transformation()
            n_patterns = len(net_input)
            n_vocab = n_vocab
            
            logging.info("Initializing data transformation")
            
            # reshape the input into a format compatible with LSTM layers
            net_input = np.reshape(net_input, (n_patterns, self.seq_len, 1))
            # normalize input
            net_input = net_input / float(n_vocab)
            # encode the output
            net_output = to_categorical(net_output, num_classes=n_vocab)
            
            save_object(
                file_path="../artifacts/input_data.pkl",
                object=net_input
            )
            save_object(
                file_path="../artifacts/output_data.pkl",
                object=net_output
            )
            
            X_train, X_test, y_train, y_test = train_test_split(net_input, net_output, test_size=0.2, random_state=352)

        
        except Exception as e:
            raise CustomException(e, sys)
        
        return X_train, y_train, X_test, y_test

if __name__ == '__main__':  
    # data_transformation_obj = DataTransformation()
    # X_train, y_train, X_test, y_test = data_transformation_obj.initiate_data_transformation()
    # print(len(X_train))
    net_input = load_object(
        file_path="../artifacts/input_data.pkl"
    )
    
    net_output = load_object(
        file_path="../artifacts/output_data.pkl"
    )
    
    pitchname = load_object(
        file_path="../artifacts/pitchnames.pkl"
    )
    n_vocab = len(pitchname)
    
    # print(net_output)
    
    X_train, X_test, y_train, y_test = train_test_split(net_input, net_output, test_size=0.2, random_state=352)
    
    print(n_vocab)
    print(X_train.shape)
    print(X_test.shape)
    
    # logging.info("Train Test Split")
    
    # model_obj = ModelTrainer(X_train, y_train, X_test, y_test, n_vocab)
    # loss, accuracy = model_obj.train_model(epochs=50, batch_size=32)
    
    # logging.info("Model trained successfully with loss=%f, accuracy=%f" % (loss, accuracy))    
    # print("loss : ", loss)
    # print("accuracy : ", accuracy)
