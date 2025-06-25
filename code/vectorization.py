from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input 
from tensorflow.keras.models import Model, load_model
import os

from PIL import Image
import pickle
import numpy as np
import matplotlib.pyplot as plt


class feature_extract:
    def __init__(self):
        pass
    
    def get_model_extract(self): # make a model to extract features use pretrain of VGG16
        vgg16_model = VGG16(weights = 'imagenet') 
        model_extract = Model(inputs = vgg16_model.input, outputs = vgg16_model.get_layer("fc1").output)
        return model_extract
    
    def img_preprocess(self, img): # image preprocessing convert to tensor
        img = img.resize((224,224)) 
        img = img.convert('RGB') 
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis = 0) # add batch_size axis
        x = preprocess_input(x) # image normalized
        return x
    
    def vector_normalized(self, model, img_path): # extract vector and normalized
        print('processing...............................................', img_path)
        img = Image.open(img_path)
        img_tensor = self.img_preprocess(img)

        vector = model.predict(img_tensor)[0] # get vector from 2D to 1D
        vector = vector / np.linalg.norm(vector) # vector normalized 
        print('processed !!!', img_path)
        return vector
    
    def store_vector(self, model, data_path):  # new method to store vectors
        vectors = []
        paths = []

        for img_path in os.listdir(data_path):
            img_path_full = os.path.join(data_path, img_path)
            img_vector = self.vector_normalized(model, img_path_full)

            vectors.append(img_vector)
            paths.append(img_path_full)

        print("Saving............................................")
        with open('vectors.pkl', 'wb') as f:
            pickle.dump(vectors, f)
        with open('paths.pkl', 'wb') as f:
            pickle.dump(paths, f)

        print("Vectors and paths saved.")

    def save_model(self, model, save_path):
        model.save(save_path)
        print("Model saved to", save_path)

    def load_model(self, load_path):
        model = load_model(load_path)
        print("Model loaded from", load_path)
        return model
        



