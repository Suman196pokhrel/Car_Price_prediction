from types import MethodDescriptorType
from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


# Initializing the Flask app
app = Flask(__name__)


# Initiating the ML models
model_linearReg = pickle.load(open(r"linear_regression_model.pkl",'rb'))
model_randomForReg = pickle.load(open(r'random_forest_regression_model.pkl', 'rb'))

# creating routs for App


@app.route('/')   # Note : default method is GET
def Home():
    return render_template('index_1.html')


sandard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():
     
     Fuel_Type_Diesel = 0
     if request.method == 'POST':
          print("JUST GOT A POST REQUEST")
          Year = int(request.form['Year'])
          Present_Price = float(request.form['Present_Price'])
          Kms_Driven = int(request.form['Kms_Driven'])
          Kms_Driven2 = np.log(Kms_Driven)
          Owner = int(request.form['Owner'])
          Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
          if(Fuel_Type_Petrol == 'Petrol'):
               Fuel_Type_Petrol = 1
               Fuel_Type_Diesel = 0
          else:
               Fuel_Type_Petrol = 0
               Fuel_Type_Diesel = 1
          Year = 2020-Year
          Seller_Type_Individual = request.form['Seller_Type_Individual']
          if(Seller_Type_Individual == 'Individual'):
               Seller_Type_Individual = 1
          else:
               Seller_Type_Individual = 0
          Transmission_Mannual = request.form['Transmission_Mannual']
          if(Transmission_Mannual == 'Mannual'):
               Transmission_Mannual = 1
          else:
               Transmission_Mannual = 0

          selected_model = request.form['Model_Type']

          # COnditioning For Machine Learning Models 


          # For Random Regressor 
          if selected_model=='Random Forest Regressor':
               print("INside the RANDOMREGRESSOR")
               prediction = model_randomForReg.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel,Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])
               output = round(prediction[0], 2)
               

               if output < 0:
                    return render_template('index_1.html', prediction_text="Sorry you cannot sell this car")
               else:
                    return render_template('index_1.html', prediction_text="you Can Sell The Car at {}".format(output))
          
          # For Linear Regressor
          
          elif selected_model == 'Linear Regression':
               print("INside the LINEARREGRESSOR")
               params = [[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel,Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]]
               print("PARAMS ARE ::==>> ", params)
               prediction = model_linearReg.predict(params).tolist()
               output = round(prediction[0][0], 2)

               
               if output < 0:
                    return render_template('index_1.html', prediction_text="Sorry you cannot sell this car")
               else:
                    return render_template('index_1.html', prediction_text="you Can Sell The Car at {}".format(output))
     
     else:
          return render_template('index_1.html')

          


if __name__ == '__main__':
    app.run(debug=True)
