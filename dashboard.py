import pandas as pd
import matplotlib.pyplot as plt
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
    df["dteday"] = pd.to_datetime(df["dteday"])
    monthly_trend_df.index = monthly_trend_df.index.strftime('%Y-%m')
    monthly_trend_df = monthly_trend_df.reset_index()
    monthly_trend_df.rename(columns={
        "dteday": "year_month",
        "cnt": "total_rentals"
    }, inplace=True)
    return monthly_trend_df

all_df = pd.read_csv("all_df.csv")

selected_option = st.sidebar.radio(
    "Pilih Tren yang Ingin Ditampilkan:",
    ("Tren Penyewaan per Bulan", "Tren Penyewaan Jam")
)


if selected_option == "Tren Penyewaan per Bulan":

    monthly_trend_df = create_monthly_trend_df(all_df)
    st.subheader('Tren Penyewaan Sepeda per Bulan')

    max_month = monthly_trend_df.loc[monthly_trend_df["total_rentals"].idxmax()]
    st.metric("Tren teritinggi pada Bulan", value=str(max_month["year_month"]))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_trend_df["year_month"], monthly_trend_df["total_rentals"], marker="o", linestyle="-", color="#72BCD4")
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
    ax.tick_params(axis='x', rotation=45) 
    st.pyplot(fig)

if selected_option == "Tren Penyewaan Jam":
    hourly_trend_df = create_hourly_rentals_df(all_df)
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Jam")
    max_hour = hourly_trend_df.loc[hourly_trend_df["total_rentals"].idxmax()]
    st.metric("Waktu dengan Penyewaan Tertinggi", value=str(max_hour["hour"]))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly_trend_df["hour"], hourly_trend_df["total_rentals"], 
            marker="o", linestyle="-", color="#72BCD4")
    ax.set_xticks(range(0, 24)) 

    st.pyplot(fig)

print(day_df.dtypes) 
