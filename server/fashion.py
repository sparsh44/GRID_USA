import pickle
import numpy as np
from numpy.linalg import norm
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input
from sklearn.neighbors import NearestNeighbors
from IPython.display import display, Image
import os
import tensorflow as tf



feature_list = np.array(pickle.load(open('embeddings.pkl','rb')))
filenames = pickle.load(open('filenames.pkl','rb'))

model = tf.keras.models.load_model("../nn_model/reNet.keras")

def preprocessImage(img):
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)

    neighbors = NearestNeighbors(n_neighbors=6,algorithm='brute',metric='euclidean')
    neighbors.fit(feature_list)

    distances,indices = neighbors.kneighbors([normalized_result])
    return indices

def getRec(img):
    indices = preprocessImage(img)
    for file in indices[0][1:6]:
        display(Image(filename=file_paths[file]))
