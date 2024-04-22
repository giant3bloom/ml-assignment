from rest_framework import viewsets, status
from rest_framework.response import Response
import pandas as pd
import numpy as np 
from sklearn.linear_model import LinearRegression

lm = None

def train():
    global lm
    data = pd.read_csv('myproject/myapp/CAR DETAILS FROM CAR DEKHO.csv')
    data.infer_objects(copy=False)
    pd.set_option('future.no_silent_downcasting', True)
    data.drop('name', axis=1, inplace=True)
    data.replace({'Individual':0, 'Dealer':1, 'Trustmark Dealer':2}, inplace=True)
    data.replace({'First Owner': 1, 'Second Owner':2, 'Third Owner':3, 'Test Drive Car':4}, inplace=True)
    data = pd.get_dummies(data)
    y = data['selling_price']
    x = data.drop('selling_price', axis=1)
    
    lm = LinearRegression()
    lm.fit(x, y)
train()
class UserInputViewSet(viewsets.ViewSet):
    def create(self, request):
        # Extract data from the request
        data = request.data
        year = int(data.get('feature1'))
        km_driven = int(data.get('feature2'))
        seler_type = data.get('feature3')
        fuel_type = data.get('feature4')
        transmission_type = data.get('feature5')
        owner = data.get('feature6')

        # Define a function to calculate prediction
        def calculate_price(year, km_driven, seler_type, fuel_type, transmission_type, owner):
            global lm 
            # Prepare data for prediction
            data = []
            #	year	km_driven	seller_type	fuel_CNG	fuel_Diesel	fuel_Electric	fuel_LPG	fuel_Petrol	transmission_Automatic	transmission_Manual	owner_1	owner_2	owner_3	owner_4	owner_Fourth & Above Owner
            data.append(year)
            data.append(km_driven)
            # Convert categorical features to numerical
            if seler_type == 'Individual':
                data.append(0)
            elif seler_type == 'Dealer':
                data.append(1)
            elif seler_type == 'Trustmark Dealer':
                data.append(2)

            if fuel_type == 'CNG':
                data.extend([1, 0, 0, 0, 0])
            elif fuel_type == 'Diesel':
                data.extend([0, 1, 0, 0, 0])
            elif fuel_type == 'Electric':
                data.extend([0, 0, 1, 0, 0])
            elif fuel_type == 'LPG':
                data.extend([0, 0, 0, 1, 0])
            elif fuel_type == 'Petrol':
                data.extend([0, 0, 0, 0, 1])

            if transmission_type == 'Automatic':
                data.append(1)
                data.append(0)
            elif transmission_type == 'Manual':
                data.append(0)
                data.append(1)

            if owner == 'First Owner':
                data.extend([1, 0, 0, 0, 0])
            elif owner == 'Second Owner':
                data.extend([0, 1, 0, 0, 0])
            elif owner == 'Third Owner':
                data.extend([0, 0, 1, 0, 0])
            elif owner == 'Test Drive Car':
                data.extend([0, 0, 0, 1, 0])
            elif owner == 'Fourth & Above Owner':
                data.extend([0, 0, 0, 0, 1])

            # Predict price
            predicted_price = lm.predict([data])[0]
            return predicted_price

        # Calculate the prediction
        predicted_price = calculate_price(year, km_driven, seler_type, fuel_type, transmission_type, owner)

        predicted_price = float("{:.4f}".format(predicted_price))

        # Return the prediction to the frontend
        return Response({'price': abs(predicted_price)}, status=status.HTTP_200_OK)
