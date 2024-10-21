from keras import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, LSTM, Dropout, add, Activation
from keras.regularizers import l2
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
import sys
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


class ModelStructure:
    def __init__(self):
        self.model = None
    
    def model_build(self, input_shape, n_vocab):
        try:
            model = Sequential()
            model.add(LSTM(256, input_shape=input_shape,return_sequences=True))
            model.add(LSTM(512, return_sequences=True))
            model.add(LSTM(256, return_sequences=False))
            model.add(Dense(256, activation='relu'))
            model.add(Dense(n_vocab))
            model.add(Activation('softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics = ['accuracy'])
            
            return model
        
        except Exception as e:
            raise CustomException(e, sys)

class ModelTrainer:
    def __init__(self, X_train, y_train, X_test, y_test, n_vocab):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.n_vocab = n_vocab
    
    def train_model(self, epochs=50, batch_size=64):
        try:
            model_obj = ModelStructure()
            model = model_obj.model_build(
                (self.X_train.shape[1], self.X_train.shape[2]),
                self.n_vocab
            )
            
            logging.info("Model Architecture build.")
            
            early_stopping = EarlyStopping(monitor='loss', patience=10)
            reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5)

            
            history = model.fit(self.X_train, self.y_train, 
                                epochs=epochs, batch_size=batch_size, 
                                callbacks=[early_stopping, reduce_lr])
            
            logging.info("Model Trained Successfully.")
            
            # Load the weights to each node
            model.save('../artifacts/weights.h5')
            
            
            loss, accuracy = model.evaluate(self.X_test, self.y_test)
            return loss, accuracy
        
        except Exception as e:
            raise CustomException(e, sys)