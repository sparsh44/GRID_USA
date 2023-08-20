from flask import Flask, request, jsonify, json
from flask_cors import CORS,cross_origin
import pandas as pd
import numpy as np

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

df6 = pd.read_csv("./dataset/df6.csv")
df8 = pd.read_csv("./dataset/df8.csv")
similar_user = pd.read_csv("./dataset/similar_user.csv")
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
            if [prodName, imgLink] not in recommendations:
                recommendations.append([prodName, imgLink])
            if category not in categories:
                categories.append(category)
            
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

@app.route('/')
def main():
    return allRecommendations(100)

@app.route('/get_predictions', methods = ['POST'])
def get_class():
    print("IN GET CLASS")
    print(allRecommendations(6183))

if __name__=='__main__':  
    print(allRecommendations(100))
    app.run(debug=True, port ='5000')