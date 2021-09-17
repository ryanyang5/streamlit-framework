# app.py

"""
A streamlit app that produces a trend of a specified stock's closing price (default: GOOG)

"""

import pandas as pd
import streamlit as st
import os
import requests
from bokeh.io import output_file, show
from bokeh.plotting import figure
import numpy as np
from dotenv import load_dotenv
import plotly.express as px


st.title('Stock Closing Price Trend')
st.sidebar.write("Please enter a ticker and select a date range:")

st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 400px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)

ticker = str(st.sidebar.text_input('Ticker:', 'TSLA'))


load_dotenv()
API_KEY = os.getenv("API_KEY")

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, API_KEY)

try:
	def load_data():
		r = requests.get(url)
		r = r.json()
		df = pd.DataFrame(r['Time Series (Daily)']).transpose()
		return df

	df = load_data()
	df.columns = ["open", "high", "low", "close", "adjusted close",
	" volume", "divident amount", "split coefficient"]

	df = df.applymap(float)
	df = df.reindex(index=df.index[::-1])
	start_date, end_date = st.sidebar.select_slider('Date Range:',
	options=list(df.index),
	value=(df.index[0], df.index[99]))

	df = df[start_date:end_date]

	fig = px.line(df, x=df.index, y="close")
	fig.update_layout(title=str(ticker.upper()), xaxis_title='Date',yaxis_title='Closing Price')
	st.plotly_chart(fig, use_container_width=True)

except KeyError:
	st.write("The ticker you entered is not valid. Please enter a valid ticker (e.g. GOOG, AAPL, TSLA)")

else:
	pass
