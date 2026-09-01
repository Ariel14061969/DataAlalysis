# import libraries


import cairocffi
import pandas as pd
import streamlit as st
from PIL import Image
from io import BytesIO
import cairosvg as svg
import requests
from import_country_data import import_country_data

Import_data = False
if Import_data:
    out_filename = 'country_with_data.csv'
    import_country_data(out_filename)

country_data = pd.read_csv('country_with_data.csv')
country_data.set_index('Country', inplace=True)

# Basic single selection (defaults to the first item)
choice = st.selectbox("Pick a country:", country_data.index)
print(choice)
#user_country = country_data.index.iloc[choice]
#if Verify_user_country(user_country, country_data):
#    Show_country_data(user_country,country_data)
