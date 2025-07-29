# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 12:38:38 2025

@author: Smaksh Mahajan
"""

import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_excel("Data_Smaksh's_version.xlsx")

# Slider for year range
year_range = st.slider("Choose year range", 1976, 2017, (1976, 2017), step=5)

# Dropdown to select country
country = st.selectbox("Choose a country", df['A'].unique())

# Dropdown (or selectbox) to choose y-axis variable
y_axis_options = {
    'Level of Democracy': 'polity2',
    'Loans by IMF in millions': 'totalarrangementsdr',
    'Population': 'population'
    
}

# Let user select which variables to plot
display_labels = list(y_axis_options.keys())
selected_labels = st.multiselect("Choose variables for y-axis", display_labels, default=[display_labels[0]])

# Filter the data
df_filtered = df[(df['A'] == country) & (df['year'].between(*year_range))]

# Plot multiple y-axis variables
fig = px.scatter(title=f"{country} Data Over Time")

for label in selected_labels:
    col_name = y_axis_options[label]
    fig.add_scatter(x=df_filtered['year'], y=df_filtered[col_name], mode='markers+lines', name=label)

st.plotly_chart(fig)


