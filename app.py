"""
FRONTEND.PY (APP.PY) - Streamlit Web Application
Interactive dashboard for crime data analysis and prediction
"""

import streamlit as st
import pandas as pd
import numpy as np
from backend import CrimeDataProcessor, HotspotDetector, CrimeRiskPredictor
from ui_components import (
    set_page_configuration, configure_chart_style,
    create_data_source_selector, display_metrics_4col, display_dataset_info,
    create_bar_chart, create_pie_chart, create_line_chart, create_scatter_plot,
    create_histogram, display_hotspot_table, create_prediction_inputs,
    show_loading_spinner, show_success_message, show_info_message
)
import warnings
warnings.filterwarnings('ignore')

# Configure page
set_page_configuration()
configure_chart_style()

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'hotspot_model' not in st.session_state:
    st.session_state.hotspot_model = None
if 'risk_predictor' not in st.session_state:
    st.session_state.risk_predictor = None

# ==================== MAIN LAYOUT ====================
st.markdown("# 🚨 Crime Data Analysis & Prediction Dashboard")
st.markdown("---")

# Sidebar - Data Loading
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    data_source, sample_size, uploaded_file = create_data_source_selector()

    if data_source == "Use Default Dataset":
        if st.button("Load Default Dataset", key="load_btn"):
            with st.spinner("Loading and processing data..."):
                csv_path = "c:/Users/saraj/Desktop/Csv file DS/Crime_Data_from_2020_to_Present.csv"
                processor = CrimeDataProcessor(csv_path)
                processor.load_data(sample=True, n_rows=sample_size)
                processor.clean_data()
                processor.extract_features()
                st.session_state.df = processor.df
                show_success_message(f"Loaded {len(processor.df):,} records")

    else:
        if uploaded_file is not None:
            with st.spinner("Loading and processing data..."):
                processor = CrimeDataProcessor("")
                processor.df = pd.read_csv(uploaded_file)
                processor.clean_data()
                processor.extract_features()
                st.session_state.df = processor.df
                show_success_message(f"Loaded {len(processor.df):,} records")

# Main content
if st.session_state.df is not None:
    df = st.session_state.df

    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Overview", "📈 Visualizations", "🎯 Hotspots", "🔮 Prediction", "⚙️ Analytics"]
    )

    # ==================== TAB 1: OVERVIEW ====================
    with tab1:
        st.markdown("### Dataset Overview")
        display_metrics_4col(
            "📋 Total Crimes", len(df),
            "📍 Unique Locations", df['area_name'].nunique(),
            "🏢 Crime Types", df['crm_cd_desc'].nunique(),
            "📅 Years Covered", f"{df['year'].min()}-{df['year'].max()}"
        )

        st.markdown("### Dataset Preview")
        preview_cols = ['date_occ', 'hour', 'area_name', 'crm_cd_desc', 'lat', 'lon']
        st.dataframe(df[preview_cols].head(10), use_container_width=True)

        st.markdown("### Data Information")
        display_dataset_info(df)

    # ==================== TAB 2: VISUALIZATIONS ====================
    with tab2:
        col1, col2 = st.columns(2)

        # Crime by hour
        with col1:
            st.markdown("### Crime Count by Hour")
            crime_by_hour = df.groupby('hour').size()
            fig = create_bar_chart(crime_by_hour, "Distribution of Crimes by Hour",
                                  "Hour of Day", "Crime Count", color='steelblue')
            st.pyplot(fig)

        # Top crime types
        with col2:
            st.markdown("### Top 10 Crime Types")
            top_crimes = df['crm_cd_desc'].value_counts().head(10)
            fig = create_bar_chart(top_crimes, "Top 10 Crime Types",
                                  "Count", "Crime Type", color='coral', kind='barh')
            st.pyplot(fig)

        col1, col2 = st.columns(2)

        # Top areas
        with col1:
            st.markdown("### Top 10 Crime Areas")
            top_areas = df['area_name'].value_counts().head(10)
            fig = create_bar_chart(top_areas, "Top 10 Crime Areas",
                                  "Count", "Area", color='lightgreen', kind='barh')
            st.pyplot(fig)

        # Crime by day of week
        with col2:
            st.markdown("### Crime by Day of Week")
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            crime_by_day = df['day_of_week'].value_counts().reindex(day_order)
            fig = create_bar_chart(crime_by_day, "Distribution by Day",
                                  "Day of Week", "Crime Count", color='skyblue')
            st.pyplot(fig)

    # ==================== TAB 3: HOTSPOTS ====================
    with tab3:
        st.markdown("### Crime Hotspot Detection using KMeans")
        st.write("Identifies geographic clusters of crime concentration")

        n_clusters = st.slider("Number of Hotspots", 3, 15, 8)

        if st.button("🔍 Detect Hotspots", key="hotspot_btn"):
            with st.spinner("Detecting hotspots..."):
                detector = HotspotDetector(n_clusters=n_clusters)
                clusters, centers = detector.detect_hotspots(df)
                st.session_state.hotspot_model = detector

                df_with_clusters = df.copy()
                df_with_clusters['cluster'] = clusters

                st.markdown("#### Hotspot Locations")
                display_hotspot_table(clusters, centers)

                st.markdown("#### Geographic Hotspot Map")
                fig = create_scatter_plot(df_with_clusters, 'lon', 'lat', 'cluster',
                                        f"Crime Hotspots ({n_clusters} clusters)", centers)
                st.pyplot(fig)

        else:
            show_info_message("Click 'Detect Hotspots' button to start analysis")

    # ==================== TAB 4: PREDICTION ====================
    with tab4:
        st.markdown("### Crime Risk Prediction")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### Option 1: By Hour & Area")

            areas = sorted(df['area_name'].unique())
            hours = sorted(df['hour'].unique())

            input_hour = st.selectbox("Select Hour", hours, key="pred_hour")
            input_area = st.selectbox("Select Area", areas, key="pred_area")

            area_data = df[df['area_name'] == input_area]
            avg_lat = area_data['lat'].mean()
            avg_lon = area_data['lon'].mean()

            if st.button("🔮 Predict Crime Type", key="pred_btn1"):
                with st.spinner("Training model..."):
                    predictor = CrimeRiskPredictor()
                    predictor.train(df)
                    st.session_state.risk_predictor = predictor

                    prediction = predictor.predict_crime_type(input_hour, input_area, avg_lat, avg_lon)
                    show_success_message(f"Predicted Crime Type: **{prediction}**")

                    # Feature importance
                    importance = predictor.get_feature_importance()
                    if importance:
                        st.markdown("#### Feature Importance")
                        fig = create_bar_chart(pd.Series(importance), "ML Model Feature Importance",
                                            "Importance", "Feature", color='teal', kind='barh')
                        st.pyplot(fig)

        with col2:
            st.markdown("#### Option 2: Custom Coordinates")

            input_hour_map = st.slider("Hour of Day", 0, 23, 12, key="hour_slider")
            input_area_map = st.selectbox("Select Area", areas, key="area_select")
            input_lat = st.number_input("Latitude", value=34.0522, format="%.4f", key="lat_input")
            input_lon = st.number_input("Longitude", value=-118.2437, format="%.4f", key="lon_input")

            if st.button("🎯 Predict at Location", key="pred_btn2"):
                with st.spinner("Predicting..."):
                    if st.session_state.risk_predictor is None:
                        predictor = CrimeRiskPredictor()
                        predictor.train(df)
                        st.session_state.risk_predictor = predictor
                    else:
                        predictor = st.session_state.risk_predictor

                    prediction = predictor.predict_crime_type(input_hour_map, input_area_map, input_lat, input_lon)
                    show_success_message(f"Predicted Crime Type: **{prediction}**")

    # ==================== TAB 5: ANALYTICS ====================
    with tab5:
        st.markdown("### Advanced Analytics")

        col1, col2 = st.columns(2)

        # Trends over time
        with col1:
            st.markdown("#### Crime Trends Over Time")
            crime_by_month = df.groupby(df['date_occ'].dt.to_period('M')).size()
            fig = create_line_chart(crime_by_month, "Crime Trends",
                                   "Month", "Crime Count")
            st.pyplot(fig)

        # Crime by year
        with col2:
            st.markdown("#### Crime Distribution by Year")
            crime_by_year = df['year'].value_counts().sort_index()
            fig = create_bar_chart(crime_by_year, "Crimes by Year",
                                  "Year", "Crime Count", color='orangered')
            st.pyplot(fig)

        st.markdown("#### Victim Demographics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Victim Sex Distribution**")
            sex_dist = df['vict_sex'].value_counts()
            fig = create_pie_chart(sex_dist, "Victim Sex")
            st.pyplot(fig)

        with col2:
            st.markdown("**Victim Age Distribution**")
            fig = create_histogram(df['vict_age'].dropna(), bins=30,
                                 title="Age Distribution", xlabel="Age")
            st.pyplot(fig)

        with col3:
            st.markdown("**Victim Descent**")
            descent_dist = df['vict_descent'].value_counts().head(8)
            fig = create_bar_chart(descent_dist, "Top Victim Descents",
                                  "Count", "Descent", color='brown', kind='barh')
            st.pyplot(fig)

else:
    show_info_message("👈 Load dataset from sidebar to begin analysis")
