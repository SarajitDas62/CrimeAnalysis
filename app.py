"""
FRONTEND.PY (APP.PY) - Premium Crime Analytics Dashboard
Interactive dark-themed dashboard for crime data analysis and prediction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from backend import CrimeDataProcessor, HotspotDetector, CrimeRiskPredictor
from ui_components import set_page_configuration
import warnings
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIGURATION ====================
set_page_configuration()

# ==================== INITIALIZE SESSION STATE ====================
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None
if 'hotspot_model' not in st.session_state:
    st.session_state.hotspot_model = None
if 'risk_predictor' not in st.session_state:
    st.session_state.risk_predictor = None

# ==================== HEADER SECTION ====================
st.markdown("""
<div class="header-container">
    <h1>🚓 Crime Analytics Dashboard</h1>
    <p class="subtitle">Real-time Crime Insights & Hotspot Detection</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR - DATA LOADING & FILTERS ====================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    data_source = st.radio("📁 Data Source", ["Use Default Dataset", "Upload CSV"])

    if data_source == "Use Default Dataset":
        sample_size = st.slider("Sample Size", 10000, 100000, 50000, step=10000)

        if st.button("📥 Load Dataset", use_container_width=True):
            with st.spinner("Loading and processing data..."):
                import os
                csv_path = "c:/Users/saraj/Desktop/Csv file DS/Crime_Data_from_2020_to_Present.csv"
                if os.path.exists(csv_path):
                    processor = CrimeDataProcessor(csv_path)
                    processor.load_data(sample=True, n_rows=sample_size)
                    processor.clean_data()
                    processor.extract_features()
                    st.session_state.df = processor.df
                    st.session_state.filtered_df = processor.df.copy()
                    st.success(f"✅ Loaded {len(processor.df):,} records")
                else:
                    st.error("❌ CSV file not found")
    else:
        uploaded_file = st.file_uploader("📤 Upload CSV", type="csv")
        if uploaded_file is not None:
            with st.spinner("Processing..."):
                processor = CrimeDataProcessor("")
                processor.df = pd.read_csv(uploaded_file)
                processor.clean_data()
                processor.extract_features()
                st.session_state.df = processor.df
                st.session_state.filtered_df = processor.df.copy()
                st.success(f"✅ Loaded {len(processor.df):,} records")

    # Filters
    if st.session_state.df is not None:
        st.markdown("---")
        st.markdown("## 🔍 Filters")

        # Crime Type Filter
        all_crimes = sorted(st.session_state.df['crm_cd_desc'].unique())
        selected_crime = st.selectbox(
            "Crime Type",
            ["All Crimes"] + all_crimes
        )

        # Hour Filter
        selected_hour = st.slider("Hour (0-23)", 0, 23, (0, 23))

        # Apply Filters
        filtered_df = st.session_state.df.copy()

        if selected_crime != "All Crimes":
            filtered_df = filtered_df[filtered_df['crm_cd_desc'] == selected_crime]

        filtered_df = filtered_df[
            (filtered_df['hour'] >= selected_hour[0]) &
            (filtered_df['hour'] <= selected_hour[1])
        ]

        st.session_state.filtered_df = filtered_df

# ==================== MAIN CONTENT ====================
if st.session_state.df is not None:
    df = st.session_state.df
    filtered_df = st.session_state.filtered_df

    # ==================== KPI SECTION ====================
    st.markdown("## 📊 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Crimes",
            f"{len(filtered_df):,}",
            f"{len(filtered_df) - len(df)}" if len(filtered_df) < len(df) else "Unfiltered"
        )

    with col2:
        most_common = filtered_df['crm_cd_desc'].value_counts().index[0] if len(filtered_df) > 0 else "N/A"
        count = filtered_df['crm_cd_desc'].value_counts().values[0] if len(filtered_df) > 0 else 0
        st.metric("Most Common Crime", most_common, count)

    with col3:
        peak_hour = filtered_df['hour'].value_counts().index[0] if len(filtered_df) > 0 else "N/A"
        st.metric("Peak Crime Hour", f"{peak_hour}:00", "24-hour format")

    st.markdown("---")

    # ==================== TABS ====================
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🔥 Hotspots", "🤖 Prediction"])

    # ==================== TAB 1: ANALYSIS ====================
    with tab1:
        st.markdown("### 📈 Crime Analysis Charts")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Crime by Hour")
            crime_by_hour = filtered_df.groupby('hour').size()
            fig_hour = go.Figure(
                data=[go.Bar(
                    x=crime_by_hour.index,
                    y=crime_by_hour.values,
                    marker=dict(color='#1f6feb', line=dict(color='#58A6FF', width=2)),
                    hovertemplate='<b>Hour:</b> %{x}:00<br><b>Crimes:</b> %{y}<extra></extra>'
                )]
            )
            fig_hour.update_layout(
                template="plotly_dark",
                showlegend=False,
                hovermode='x unified',
                xaxis_title="Hour of Day",
                yaxis_title="Number of Crimes",
                height=400
            )
            st.plotly_chart(fig_hour, use_container_width=True)

        with col2:
            st.subheader("Top 10 Crime Types")
            top_crimes = filtered_df['crm_cd_desc'].value_counts().head(10)
            fig_crime = px.bar(
                x=top_crimes.values,
                y=top_crimes.index,
                orientation='h',
                title="Top 10 Crime Types",
                labels={'x': 'Count', 'y': 'Crime Type'}
            )
            fig_crime.update_traces(marker=dict(color='#238636', line=dict(color='#2ea043', width=2)))
            fig_crime.update_layout(
                template="plotly_dark",
                showlegend=False,
                height=400,
                hovermode='y unified'
            )
            st.plotly_chart(fig_crime, use_container_width=True)

        # Crime by Day of Week
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Crime by Day of Week")
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            crime_by_day = filtered_df['day_of_week'].value_counts().reindex(day_order)
            fig_day = go.Figure(
                data=[go.Bar(
                    x=crime_by_day.index,
                    y=crime_by_day.values,
                    marker=dict(color='#d1883d', line=dict(color='#f08d57', width=2)),
                    hovertemplate='<b>%{x}</b><br>Crimes: %{y}<extra></extra>'
                )]
            )
            fig_day.update_layout(
                template="plotly_dark",
                showlegend=False,
                height=400,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_day, use_container_width=True)

        with col2:
            st.subheader("Crime by Area")
            area_crimes = filtered_df['area_name'].value_counts().head(10)
            fig_area = px.bar(
                x=area_crimes.values,
                y=area_crimes.index,
                orientation='h'
            )
            fig_area.update_traces(marker=dict(color='#6e40c9', line=dict(color='#9966ff', width=2)))
            fig_area.update_layout(
                template="plotly_dark",
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig_area, use_container_width=True)

    # ==================== TAB 2: HOTSPOTS ====================
    with tab2:
        st.markdown("### 🗺️ Crime Hotspot Detection")

        col1, col2 = st.columns([1, 2])

        with col1:
            n_clusters = st.slider("Number of Hotspots", 3, 15, 8)
            if st.button("🔍 Detect Hotspots", use_container_width=True):
                with st.spinner("Detecting hotspots..."):
                    detector = HotspotDetector(n_clusters=n_clusters)
                    clusters, centers = detector.detect_hotspots(filtered_df)
                    st.session_state.hotspot_model = detector

                    # Display hotspot table
                    hotspot_data = pd.DataFrame({
                        'Hotspot ID': range(len(centers)),
                        'Latitude': centers[:, 0].round(4),
                        'Longitude': centers[:, 1].round(4),
                        'Crime Count': [sum(clusters == i) for i in range(len(centers))]
                    }).sort_values('Crime Count', ascending=False)

                    st.markdown("#### Hotspot Information")
                    st.dataframe(hotspot_data, use_container_width=True, hide_index=True)

        with col2:
            if st.session_state.hotspot_model is not None:
                detector = st.session_state.hotspot_model
                clusters, centers = detector.detect_hotspots(filtered_df)

                # Create scatter plot
                fig_hotspots = go.Figure()

                # Add crime data points
                fig_hotspots.add_trace(go.Scattergeo(
                    lon=filtered_df['lon'],
                    lat=filtered_df['lat'],
                    mode='markers',
                    marker=dict(
                        size=4,
                        color=clusters,
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Cluster")
                    ),
                    text=filtered_df['crm_cd_desc'],
                    hovertemplate='<b>Crime:</b> %{text}<br><b>Lat:</b> %{lat:.4f}<br><b>Lon:</b> %{lon:.4f}<extra></extra>'
                ))

                # Add cluster centers
                fig_hotspots.add_trace(go.Scattergeo(
                    lon=centers[:, 1],
                    lat=centers[:, 0],
                    mode='markers',
                    marker=dict(size=15, color='red', symbol='star', line=dict(width=2, color='white')),
                    text=[f'Hotspot {i}' for i in range(len(centers))],
                    hovertemplate='<b>%{text}</b><extra></extra>'
                ))

                fig_hotspots.update_layout(
                    template="plotly_dark",
                    geo=dict(projection_type='mercator'),
                    height=500,
                    showlegend=False
                )
                st.plotly_chart(fig_hotspots, use_container_width=True)
            else:
                st.info("👈 Select hotspot count and click 'Detect Hotspots' to visualize")

    # ==================== TAB 3: PREDICTION ====================
    with tab3:
        st.markdown("### 🤖 Crime Risk Prediction")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Make Prediction")

            pred_hour = st.slider("Select Hour", 0, 23, 12, key="pred_hour_slider")

            areas = sorted(filtered_df['area_name'].unique())
            pred_area = st.selectbox("Select Area", areas, key="pred_area_select")

            if st.button("🔮 Predict Crime Type", use_container_width=True):
                with st.spinner("Training model..."):
                    predictor = CrimeRiskPredictor()
                    predictor.train(filtered_df)
                    st.session_state.risk_predictor = predictor

                    # Get area coordinates
                    area_data = filtered_df[filtered_df['area_name'] == pred_area]
                    pred_lat = area_data['lat'].mean()
                    pred_lon = area_data['lon'].mean()

                    # Make prediction
                    prediction = predictor.predict_crime_type(pred_hour, pred_area, pred_lat, pred_lon)

                    # Display result
                    st.markdown(f"""
                    <div class="premium-card">
                        <h3 style="color: #58A6FF;">Prediction Result</h3>
                        <p><b>Hour:</b> {pred_hour}:00</p>
                        <p><b>Area:</b> {pred_area}</p>
                        <p style="font-size: 1.3em; color: #79C0FF;"><b>Predicted Crime Type:</b></p>
                        <p style="font-size: 1.5em; color: #1f6feb;"><b>{prediction}</b></p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Show feature importance
                    importance = predictor.get_feature_importance()
                    if importance:
                        fig_importance = px.bar(
                            x=list(importance.values()),
                            y=list(importance.keys()),
                            orientation='h',
                            title="Model Feature Importance"
                        )
                        fig_importance.update_traces(marker=dict(color='#238636'))
                        fig_importance.update_layout(template="plotly_dark", height=300)
                        st.plotly_chart(fig_importance, use_container_width=True)

        with col2:
            st.markdown("#### Model Statistics")

            if st.session_state.risk_predictor is not None:
                pred_stats = {
                    "Model": "Random Forest",
                    "Trees": "100",
                    "Max Depth": "15",
                    "Training Samples": f"{len(filtered_df):,}",
                    "Crime Types": f"{filtered_df['crm_cd_desc'].nunique()}",
                    "Locations": f"{filtered_df['area_name'].nunique()}"
                }

                stats_html = "<div class='premium-card'>"
                for key, value in pred_stats.items():
                    stats_html += f"<p><b>{key}:</b> {value}</p>"
                stats_html += "</div>"

                st.markdown(stats_html, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Make a prediction to see model statistics")

else:
    st.markdown("""
    <div class="premium-card">
        <h3 style="color: #58A6FF;">👋 Welcome to Crime Analytics Dashboard</h3>
        <p>Please load a dataset from the sidebar to get started.</p>
        <p><b>Steps:</b></p>
        <ul>
            <li>Select a data source (Default or Upload)</li>
            <li>Click "Load Dataset" button</li>
            <li>Use filters to refine data</li>
            <li>Explore Analysis, Hotspots, and Predictions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
