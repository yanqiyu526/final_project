import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import datetime as dt
import geopy.distance

plt.style.use("seaborn")
st.title("Uber Fares Datasets by Jiayu Cui & Yanqi Yu")
df = pd.read_csv("uber.csv")
df = df.tail(5000)  # Here we select the last 5000 rows
df["latitude"] = df["pickup_latitude"]
df["longitude"] = df["pickup_longitude"]
df.pickup_datetime = pd.to_datetime(df.pickup_datetime)
df["year"] = df.pickup_datetime.dt.year
df["month"] = df.pickup_datetime.dt.month
df["weekday"] = df.pickup_datetime.dt.weekday
df["hour"] = df.pickup_datetime.dt.hour
df["Distance"] = [
    round(
        geopy.distance.distance(
            (df.pickup_latitude[i], df.pickup_longitude[i]),
            (df.dropoff_latitude[i], df.dropoff_longitude[i]),
        ).km,
        2,
    )
    for i in df.index
]


# Get the uber data from US only
df = df[
    (-130 < df["pickup_longitude"])
    & (df["pickup_longitude"] < -70)
    & (-130 < df["dropoff_longitude"])
    & (df["dropoff_longitude"] < -70)
    & (25 < df["pickup_latitude"])
    & (df["pickup_latitude"] < 50)
    & (25 < df["dropoff_latitude"])
    & (df["dropoff_latitude"] < 50)
    & (df["passenger_count"] < 50)
    & (df["passenger_count"] > 0)
    & (df["Distance"] < 50)
]


fare_amount_filter = st.slider("Minimal Fare Amount:", 2.5, 230.0, 12.0)
st.subheader("Distribution of Uber trips with the chosen Minimal Fare Amount :")
df1 = df[df.fare_amount >= fare_amount_filter]
st.map(df1)


passenger_count_filter = st.sidebar.radio(
    label="Choose passenger number",
    options=("Single", "Double", "More", "All"),
)


if passenger_count_filter == "Single":
    df = df[df.passenger_count == 1]
    st.subheader("Distribution of fare of trip for one passenger")
    fig, ax3 = plt.subplots()
    df.fare_amount.hist(bins=50)
    plt.xlabel("Fare_amount")
    plt.ylabel("Amount")
    st.pyplot(fig)


elif passenger_count_filter == "Double":
    df = df[df.passenger_count == 2]
    st.subheader("Distribution of fare of trip for two passengers")
    fig, ax4 = plt.subplots()
    df.fare_amount.hist(bins=50)
    plt.xlabel("Fare_amount")
    plt.ylabel("Amount")
    st.pyplot(fig)

elif passenger_count_filter == "More":
    df = df[df.passenger_count > 2]
    st.subheader("Distribution of fare of trip for over 2 passengers")
    fig, ax5 = plt.subplots()
    df.fare_amount.hist(bins=50)
    plt.xlabel("Fare_amount")
    plt.ylabel("Amount")
    st.pyplot(fig)

elif passenger_count_filter == "All":
    st.subheader("Distribution of fare of trip")
    fig, ax6 = plt.subplots()
    df.fare_amount.hist(bins=50)
    plt.xlabel("Fare_amount")
    plt.ylabel("Amount")
    st.pyplot(fig)


# Q1: Change of Total Fare from 2009 to 2015
st.subheader("Change of Total Fare from 2009 to 2015:")
a = df.groupby("year")["fare_amount"].sum()
b = pd.Series(a, a.index)
fig, ax = plt.subplots()
plt.style.use("seaborn")
b.plot(ax=ax, linestyle="solid", marker="o")
ax.set_ylabel("Total Fare")
ax.set_title("Change of Total Fare from 2009 to 2015")
st.pyplot(fig)


# Q2: Distribution of Average Fare in a week
st.subheader("Distribution of Average Fare in a week:")
c = df.groupby("weekday")["fare_amount"].mean()
daily_fare = []
for i in c:
    daily_fare.append(i)

day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
d = pd.Series(daily_fare, day)
fig, ax1 = plt.subplots()
d.plot.bar(ax=ax1)
ax1.set_ylabel("Average   Fare")
ax1.set_title("Average Fare in a Week")
plt.xticks(rotation=0)
st.pyplot(fig)

# Q3: Distribution of distance of each trip
st.subheader("Distribution of Distance in each trip")
fig, ax2 = plt.subplots()
df.Distance.hist(bins=50)
plt.xlabel("Distance(km)")
plt.ylabel("Amount")
st.pyplot(fig)
