# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 13:06:26 2025

@author: Smaksh Mahajan
"""

import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_excel("Data_Smaksh's_version.xlsx")


# Filter just for the selected country or data source if needed
# (or use df directly if it's already ready)
if not df.empty:
    df_clean = df.dropna(subset=["eb1"]).copy()
    df_clean["SentimentMagnitude"] = df_clean["eb1"].abs()
    
    
    
    fig = px.scatter_geo(
        df_clean,
        locations="A",
        locationmode="country names",
        color="eb1",
        size="SentimentMagnitude",
        hover_name="A",
        animation_frame="year",
        color_continuous_scale="RdYlGn",
        projection="natural earth",
        title="Sentiment Map Over Time"
    )
    fig.update_layout(geo=dict(showland=True, landcolor="LightGray"))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available.")
