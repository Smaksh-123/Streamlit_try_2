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
        title="Sentiment Map Over Time",
        custom_data=["eb1","year","A"] 
    )
    
    # Customize hovertemplate
    fig.update_traces(
       hovertemplate="<b>Country Name</b>: %{customdata[2]}<br><b>Sentiment Score</b>: %{customdata[0]}<br><b>Year</b>: %{customdata[1]}<extra></extra>"
       )
    if fig.frames:
        for frame in fig.frames:
            for trace in frame.data:
                trace.hovertemplate = "<b>Country Name</b>: %{customdata[2]}<br><b>Sentiment Score</b>: %{customdata[0]}<br><b>Year</b>: %{customdata[1]}<extra></extra>"

    fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="white",
        showcountries=True,
        countrycolor="black",
        bgcolor="black",
        showocean=True,
        oceancolor="lightblue",
        projection_type="orthographic"  # or your preferred projection
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    coloraxis_colorbar=dict(title="Sentiment Score"),
    title=dict(
        text="Global Sentiment Map Over Time",
        x=0.5,
        xanchor="center",
        font=dict(size=20)
    )
    )
    fig.update_coloraxes(colorscale="plasma")
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("No data available.")
