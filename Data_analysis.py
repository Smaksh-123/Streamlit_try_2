import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("Data_Smaksh's_version.xlsx")

# ------------------- Variable Options & Descriptions -------------------
y_axis_options = {
    'Level of Democracy': {
        'col': 'polity2',
        'desc': 'Measures the level of democracy, higher values mean more democratic.'
    },
    'Loans by IMF in millions': {
        'col': 'totalarrangementsdr',
        'desc': 'Amount of IMF loans in millions USD.'
    },
    'Population': {
        'col': 'population',
        'desc': 'Total population of the country.'
    },
    "GDP Per Capita": {
        'col': "gdp_percapita",
        'desc': "Gross Domestic Product per capita in USD."
    },
    "Sentiment Scores (EB4)": {
        'col': "eb4",
        'desc': "Sentiment score measuring executive board discontent."
    }
}

# ------------------- Sidebar Controls -------------------
st.sidebar.header("Controls")

# Year range selection
min_year = int(df["year"].min())
max_year = int(df["year"].max())
selected_year_range = st.sidebar.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, min_year + 5),  # default 5-year span
    step=1
)

# Country selection
selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=sorted(df['A'].unique()),
    default=sorted(df['A'].unique())[:3]
)

# Variable selection
selected_labels = st.sidebar.multiselect(
    "Select variables to plot",
    options=list(y_axis_options.keys()),
    default=[list(y_axis_options.keys())[0]]
)

# ------------------- Filter Data -------------------
df_filtered = df[
    (df['year'] >= selected_year_range[0]) &
    (df['year'] <= selected_year_range[1]) &
    (df['A'].isin(selected_countries))
].copy()

# ------------------- Variable Descriptions -------------------
st.title("📈 Country Comparisons Over Time")

st.markdown("### Variable Descriptions")
for var in selected_labels:
    st.markdown(f"**{var}:** {y_axis_options[var]['desc']}")

# ------------------- Plotting -------------------
if df_filtered.empty:
    st.warning("No data available for selected filters.")
else:
    if len(selected_labels) == 1:
        col_name = y_axis_options[selected_labels[0]]['col']
        fig = px.line(
            df_filtered,
            x='year',
            y=col_name,
            color='A',
            markers=True,
            title=f"{selected_labels[0]} ({selected_year_range[0]} - {selected_year_range[1]})",
            labels={'A': 'Country', 'year': 'Year', col_name: selected_labels[0]}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Melt the DataFrame to long format
        melted = df_filtered.melt(
            id_vars=['year', 'A'],
            value_vars=[y_axis_options[label]['col'] for label in selected_labels],
            var_name='Variable',
            value_name='Value'
        )
        fig = px.line(
            melted,
            x='year',
            y='Value',
            color='A',
            line_dash='Variable',
            facet_row='Variable',
            markers=True,
            title=f"Comparison of Selected Variables ({selected_year_range[0]} - {selected_year_range[1]})",
            labels={'A': 'Country', 'year': 'Year', 'Value': 'Value'}
        )
        fig.update_layout(height=300 * len(selected_labels))
        st.plotly_chart(fig, use_container_width=True)
