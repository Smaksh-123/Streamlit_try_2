# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 13:06:26 2025
@author: Smaksh Mahajan
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit layout
st.set_page_config(layout="wide")
st.title("🌍 Global Sentiment Map Over Time")

# Load data
df = pd.read_excel("Data_Smaksh's_version.xlsx")

# Available sentiment variables
sentiment_options = ["eb1", "eb2", "eb4"]

# Define both short and long labels
sentiment_label_map = {
    "eb1": {
        "short": "Executive Board Discontent (Overall)",
        "long": "Measured as the sum of all sentence sentiments (sum of -1, 0, and 1 divided by total number of sentences)."
    },
    "eb2": {
        "short": "Executive Board Discontent (Negative / Total)",
        "long": "Measured as the sum of all negative sentence sentiments (sum of -1 divided by total number of sentences)."
    },
    "eb3": {
        "short": "Executive Board Discontent (Negative and Positive / Total)",
        "long": "Measured as sum of all negative and positive sentence sentiments (sum of all -1 divided by total number of -1 and 1 sentences)."
    },
    "eb4": {
        "short": "Executive Board Discontent (Negatives Sentances)",
        "long": "Measured as the total number of negative sentence sentiments (-1 sentences only)."
    }
}

# Dropdown for sentiment selection
selected_sentiment = st.selectbox("Select Sentiment Metric:", sentiment_options, index=0)
sentiment_short_label = sentiment_label_map[selected_sentiment]["short"]
sentiment_long_description = sentiment_label_map[selected_sentiment]["long"]

# Show long description as readable text in Streamlit
st.markdown(f"**Description:** {sentiment_long_description}")

# Filter and prepare data
if not df.empty:
    df_clean = df.dropna(subset=[selected_sentiment]).copy()
    df_clean["SentimentMagnitude"] = df_clean[selected_sentiment].abs()

    # Create animated map
    fig = px.scatter_geo(
        df_clean,
        locations="A",
        locationmode="country names",
        color=selected_sentiment,
        size="SentimentMagnitude",
        hover_name="A",
        animation_frame="year",
        color_continuous_scale="RdYlGn",
        projection="natural earth",
        title=f"{sentiment_short_label} Over Time",
        custom_data=[selected_sentiment, "year", "A"]
    )

    # Hover template
    hover_template = (
        "<b>🌍 Country:</b> %{customdata[2]}<br>"
        f"<b>📊 {sentiment_short_label}:</b> " + "%{customdata[0]:.2f}<br>"
        "<b>📅 Year:</b> %{customdata[1]}<extra></extra>"
    )

    fig.update_traces(
        hovertemplate=hover_template,
        marker=dict(
            line=dict(width=1, color="white"),
            opacity=0.7,
            sizemode='area',
            sizeref=2.*df_clean["SentimentMagnitude"].max()/(40.**2),
            sizemin=4
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_color="black"
        )
    )

    if fig.frames:
        for frame in fig.frames:
            for trace in frame.data:
                trace.hovertemplate = hover_template

    # Update layout and styles
    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor="white",
            showcountries=True,
            countrycolor="black",
            bgcolor="black",
            showocean=True,
            oceancolor="lightblue",
            projection_type="orthographic"
        ),
        paper_bgcolor='black',
    plot_bgcolor='black',
    title=dict(
        text=f"🌐 {sentiment_short_label} Over Time",
        x=0.5,
        xanchor="center",
        font=dict(size=22, color="white")
    ),
    coloraxis_colorbar=dict(
        title="Sentiment Score",
        ticks="outside"
    )
)

# Set a consistent diverging color scale and optionally clamp min/max values
    fig.update_coloraxes(
        colorscale="RdYlGn",
        cmin=df_clean[selected_sentiment].min(),
        cmax=df_clean[selected_sentiment].max()
    )


    fig.update_coloraxes(colorscale="Inferno")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No data available. Please check your Excel file.")
