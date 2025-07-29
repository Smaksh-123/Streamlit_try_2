import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("My First Streamlit App!")

# Load sample data
df = px.data.gapminder()

# Drop Down Menu!
country = st.selectbox("Select a country", df['country'].unique())

# Filter data
filtered = df[df['country'] == country]

# Line chart
fig = px.line(filtered, x='year', y='pop', title=f"GDP per Capita: {country}")
st.plotly_chart(fig)

