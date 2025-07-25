import streamlit as st
import numpy as np
import pandas as pd
import pickle

# Load saved model and transformer
from joblib import load
model = load('final_model.joblib')
pt = load('transformer.joblib')

with open('transformer.pkl', 'rb') as file:
    pt = pickle.load(file)

# Prediction function
def prediction(input_list):
    # Convert lead time and price to float before transformation
    lead_time = float(input_list[0])
    price = float(input_list[3])

    tran_data = pt.transform([[lead_time, price]])
    input_list[0] = tran_data[0][0]
    input_list[3] = tran_data[0][1]

    input_array = np.array(input_list, dtype=object)
    pred = model.predict_proba([input_array])[:, 1][0]

    if pred > 0.5:
        return f'⚠️ This booking is more likely to get canceled: {round(pred * 100, 2)}% chance'
    else:
        return f'✅ This booking is less likely to get canceled: {round(pred * 100, 2)}% chance'

# Streamlit app
def main():
    st.title('🏨 INN HOTEL GROUP - Cancellation Predictor')

    lt = st.text_input('Enter the lead time (in days)', value="0")
    mst = 1 if st.selectbox('Enter the type of booking', ['online', 'offline']) == 'online' else 0
    spcl = st.selectbox('Number of special requests made', [0, 1, 2, 3, 4])
    price = st.text_input('Enter the price of the room', value="0")
    adult = st.selectbox('Number of adults in booking', [0, 1, 2, 3, 4])
    wkd = st.text_input('Enter the number of **weekend nights**', value="0")
    wk = st.text_input('Enter the number of **week nights**', value="0")
    park = 1 if st.selectbox('Is parking included?', ['Yes', 'No']) == 'Yes' else 0
    month = st.slider('Month of arrival', min_value=1, max_value=12, step=1)
    day = st.slider('Day of arrival', min_value=1, max_value=31, step=1)
    
    wkday_map = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
    wkday = wkday_map[st.selectbox('Weekday of arrival', list(wkday_map.keys()))]

    try:
        inp_list = [
            float(lt), mst, spcl, float(price), adult,
            int(wkd), park, int(wk), month, day, wkday
        ]

        if st.button('Predict'):
            response = prediction(inp_list)
            st.success(response)
    except ValueError:
        st.error("❌ Please enter valid numeric values for Lead Time, Price, Weekend Nights, and Week Nights.")

if __name__ == '__main__':
    main()
