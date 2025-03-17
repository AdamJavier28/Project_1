import pandas as pd
import matplotlib as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_hourly_rentals_df(df):
    hourly_rentals_df = hour_df.groupby("hr").agg({
        "cnt": "sum"
    }).reset_index()
    hourly_rentals_df.rename(columns={
        "hr": "hour",
        "cnt": "total_rentals"
    }, inplace=True)

    return hourly_rentals_df

def create_monthly_trend_df(df):
    monthly_trend_df = day_df.resample(rule='M', on='dteday').agg({
        "cnt": "sum"
    })
    monthly_trend_df.index = monthly_trend_df.index.strftime('%Y-%m')
    monthly_trend_df = monthly_trend_df.reset_index()
    monthly_trend_df.rename(columns={
        "dteday": "year_month",
        "cnt": "total_rentals"
    }, inplace=True)
    return monthly_trend_df

day_df = pd.read_csv("day_df.csv")
hour_df = pd.read_csv("hour_df.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = [(day_df["dteday"] >= str(start_date)) &
           (day_df["dteday"] <= str(end_date))]



monthly_trend_df = create_monthly_trend_df(main_df)
hourly_trend_df = create_hourly_rentals_df(main_df)

st.subheader('Tren Penyewaan Sepeda per Bulan')

max_month = monthly_trend_df.loc[monthly_trend_df["total_rentals"].idxmax()]
st.metric("Tren teritinggi pada Bulan", value=str(max_month["year_month"]))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_trend_df["year_month"], monthly_trend_df["total_rentals"], marker="o", linestyle="-", color="#72BCD4")
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
ax.tick_params(axis='x', rotation=45) 
st.pyplot(fig)

st.subheader("Tren Penyewaan Sepeda Berdasarkan Jam")
max_hour = hourly_trend_df.loc[hourly_trend_df["total_rentals"].idxmax()]
st.metric("Waktu dengan Penyewaan Tertinggi", value=max_hour)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_trend_df["hour"], hourly_trend_df["total_rentals"], 
        marker="o", linestyle="-", color="#72BCD4")
ax.set_xticks(range(0, 24)) 

st.pyplot(fig)

