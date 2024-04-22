import streamlit as st
import pandas as pd
import numpy as np 

#load pickle model
import pickle as pk
pk_path = 'pk_file.sav'
with open(pk_path, 'rb') as pk_f:
  lm = pk.load(pk_f)

# pred()
def calculate(feature):
    return abs(lm.predict(feature)[0])

#create df
def get_input():
    year = st.text_input("year :")
    km_driven = st.text_input("km driven :")
    seler_type = st.text_input("seler type [ Indcividual | Dealer | Trustmark Dealer ] :")
    fuel_type = st.text_input("fuel type [ Petrol | Diesel ] :")
    transmission_type = st.text_input("transmission type [ Manual | Automatic ] :")
    owner = st.text_input("owner [ First Owner | Second Owner | Fourth & Above Owner | Third Owner | Test Drive Car ] :")
    data = [0]*15
    data[0] = year
    data[1] = km_driven
    if seler_type == 'Individual':
        data[2] = 0
    elif seler_type == 'Dealer':
        data[2] = 1
    elif seler_type == 'Trustmark Dealer':
        data[2] = 2
    if fuel_type == 'CNG':
        data[3] = 1
    elif fuel_type == 'Diesel':
        data[4] = 1
    elif fuel_type == 'Electric':
        data[5] = 1
    elif fuel_type == 'LPG':
        data[6] = 1
    elif fuel_type == 'Petrol':
        data[7] = 1
    if transmission_type == 'Automatic':
        data[8] = 1
    elif transmission_type == 'Manual':
        data[9] = 1
    if owner == 'First Owner':
        data[10] = 1
    elif owner == 'Second Owner':
        data[11] = 1
    elif owner == 'Third Owner':
        data[12] = 1
    elif owner == 'Test Drive Car':
        data[13] = 1
    elif owner == 'Fourth & Above Owner':
        data[14] = 1
    data = np.array(data)
    return pd.DataFrame(data.reshape(1, 15))

# Streamlit app
def main():
    st.title("car price")
    st.write("enter data, we will predict its price!")

    df = get_input()

    # pred button
    if st.button("calculate"):
        price = calculate(df)
        st.write(f"price : {price}")

if __name__ == "__main__":
    main()

