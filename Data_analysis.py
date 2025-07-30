import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel("Data_Smaksh's_version.xlsx")

# Slider for year range
year_range = st.slider("Choose year range", 1976, 2017, (1976, 2017), step=5)

# Multi-select countries
selected_countries = st.multiselect("Choose countries", df['A'].unique(), default=[df['A'].unique()[0]])

# Dropdown for y-axis variables
y_axis_options = {
    'Level of Democracy': 'polity2',
    'Loans by IMF in millions': 'totalarrangementsdr',
    'Population': 'population'
}

display_labels = list(y_axis_options.keys())
selected_labels = st.multiselect("Choose variables for y-axis", display_labels, default=[display_labels[0]])

# Filter data
df_filtered = df[df['A'].isin(selected_countries) & df['year'].between(*year_range)]
df_filtered['Level of Democracy'] = df_filtered['polity2']
df_filtered['Loans by IMF in millions'] = df_filtered['totalarrangementsdr']
df_filtered['Population'] = df_filtered['population']

if len(selected_labels) == 1:
    # If only one variable selected, plot with color grouping by country
    col_name = y_axis_options[selected_labels[0]]
    fig = px.line(
        df_filtered,
        x='year',
        y=col_name,
        color_discrete_sequence=px.colors.qualitative.Dark24,
        color='A',  
            # color by country
        markers=True,
        title=f"Comparison of {selected_labels[0]} Over Time"
    )
else:

    # If multiple variables selected, plot separate subplots for clarity
    fig = px.line(
        df_filtered.melt(id_vars=['year', 'A'], value_vars=[y_axis_options[label] for label in selected_labels],
                         var_name='Variable', value_name='Value'),
        x='year',
        y='Value',
        color_discrete_sequence=px.colors.qualitative.Dark24,
        color='A',  # color by country
        line_dash='Variable',   # differentiate variables by dash style
        markers=True,
        facet_row='Variable',
        title="Comparison Over Time"
    )
    fig.update_layout(height=300 * len(selected_labels))  # adjust height for subplots

# Update layout with axis titles and legend
fig.update_layout(
    xaxis_title="Year",
    yaxis_title=", ".join(selected_labels),
    legend_title="Country",
    title_x=0.5
)

st.plotly_chart(fig)
