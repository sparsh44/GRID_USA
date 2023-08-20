from flask import Flask, request, jsonify, json
from flask_cors import CORS,cross_origin
import pandas as pd
import numpy as np
import pickle
from numpy.linalg import norm
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.neighbors import NearestNeighbors
from io import BytesIO
from PIL import Image
import os
import tensorflow as tf

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

df6 = pd.read_csv("../dataset/df6.csv")
df8 = pd.read_csv("../dataset/df8.csv")
similar_user = pd.read_csv("../dataset/similar_user.csv")
similar_user = similar_user.to_numpy()

user_product = df6.groupby('userID')['product_id'].agg(list)
def getRecommendations(userId):
    arr = similar_user[userId]
    nums = []
    for i in range(len(arr)):
        if arr[i] > 0:
            nums.append([arr[i], i])
    nums.sort(reverse = True)
    #now i will see products bought by similar users
    recommendations = []
    categories = []
    myProd = user_product[userId]
    for i in range(len(nums)):
        uId = nums[i][1]
        if uId not in user_product:
            continue
        prod = user_product[uId]
        for p in prod:
            #if given product is already bought by user then dont recommend
            prodName = df6[df6['product_id'] == p]['product_name'].unique()[0]
            category = df6[df6['product_id'] == p]['category'].unique()[0]
            imgLink = df6[df6['product_id'] == p]['img_link'].unique()[0]
            if category not in categories:
                categories.append(category)
            if [prodName, imgLink] not in recommendations:
                if p in myProd:
                    continue
                recommendations.append([prodName, imgLink])
            
    return recommendations,categories

def getTopProd(category):
    temp = df8[df8['category'] == category][['product_name', 'img_link']][:10]
    temp = np.array(temp)
    return temp

def allRecommendations(userId):
    rec, cat = getRecommendations(userId)   
    for val in cat:
        arr = getTopProd(val)
        for i in arr:
            rec.append(list(i))
    return rec

feature_list = np.array(pickle.load(open('../nn_model/embeddings.pkl','rb')))
filenames = pickle.load(open('../nn_model/filenames.pkl','rb'))

model = tf.keras.models.load_model("../nn_model/resNet.keras")

to_remove = '/kaggle/input/fashion-product-images-small'
new_filenames = [filename.replace(to_remove, '') for filename in filenames]
file_paths = ['../fashionImages'+filename for filename in new_filenames]


def preprocessImage(img):
    # img = input(shape=(None, 224, 224, 3))
    # img = img.resize((None, 224, 224, 3))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)

    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)

    neighbors = NearestNeighbors(n_neighbors=6,algorithm='brute',metric='euclidean')
    neighbors.fit(feature_list)

    distances,indices = neighbors.kneighbors([normalized_result])
    return (indices)

def getRec(img):
    print(len(filenames))
    indices = preprocessImage(img)
    response = []
    for file in indices[0][1:11]:
        name = file_paths[file]
        response.append(name)
    return response

def getMyProd(userId):
    myProd = user_product[userId]
    purchaseHistory = []
    for p in myProd:
        #if given product is already bought by user then dont recommend
        prodName = df6[df6['product_id'] == p]['product_name'].unique()[0]
        imgLink = df6[df6['product_id'] == p]['img_link'].unique()[0]
        purchaseHistory.append([prodName, imgLink])
    return purchaseHistory

@app.route('/',  methods = ['GET', 'POST'])
def main():
    userId = request.json['data']
    print(userId)
    rec = allRecommendations(int(userId))
    print(rec)
    history = getMyProd(int(userId))
    return [rec, history]

@app.route('/getFashion', methods = ['POST'])
def getFashion():
    file = request.files['file']
    img = Image.open(file)
    desired_shape=(224, 224)
    resized_img=img.resize(desired_shape, Image.ANTIALIAS)
    filesPath = getRec(resized_img)
    return filesPath


if __name__=='__main__':  
    app.run(debug=True, port ='5000')