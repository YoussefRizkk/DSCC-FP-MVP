import streamlit as st
from DSCC_FP_MVP_Storage import MySQLDatabase as db
import DSCC_FP_MVP_Timeseries_Forecasting as forecast
import plotly.express as px
import pandas as pd


# Create a connection with the database
connection = db.create_connection(
    'root', 'password', 'localhost', 'new_stock_db')

# Execute a sql query to fetch all the tables from the database
result_from_query = db.execute_sql_query('SHOW TABLES')
# Convert the result obtained into a list which contains the table names
sql_table_name_list = [i[0] for i in result_from_query]


# Side bar filters
year = st.sidebar.selectbox('Select the stock to display',
                            options=sql_table_name_list)

quarter = st.sidebar.selectbox('Select the Column',
                               options=['Open', 'Close', 'Low', 'High'])


# Set the main header title of the web page
st.title('Stock Analysis & Forecasting')


def load_data():
    """Loads the data from the MySQL server. 
    """
    df_fetch_from_sql = pd.read_sql_table(
        sql_table_name_list[0],
        connection)
    print(df_fetch_from_sql)
    return df_fetch_from_sql


df = load_data()


st.subheader(f'Stock Price Variation')
line_chart = px.line(df, 'Date', 'Open')
st.plotly_chart(line_chart, use_container_width=True)
# st.plotly_chart(fig_total_count_by_year, use_container_width=True)

st.subheader(f'50 Days Forecast')
st.pyplot(forecast.fig)
# st.plotly_chart(fig_data_year_qtr, use_container_width=True)
