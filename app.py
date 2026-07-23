import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px

st.set_page_config(page_title="Bridge Health Monitoring Dashboard", layout="wide")

st.title("🌉 Bridge Structural Health Monitoring")

# 1. Dynamically locate and process all Excel sensor files
data_folder = "data"
excel_files = glob.glob(os.path.join(data_folder, "*.xlsx"))

if not excel_files:
    excel_files = glob.glob("*.xlsx")

if not excel_files:
    st.warning("No Excel sensor data files found in the repository.")
else:
    all_sensor_data = []
    
    for file_path in excel_files:
        try:
            df = pd.read_excel(file_path)
            sensor_id = os.path.basename(file_path).replace(".xlsx", "")
            df['Sensor_Source'] = sensor_id
            all_sensor_data.append(df)
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")

    if all_sensor_data:
        combined_df = pd.concat(all_sensor_data, ignore_index=True)
        
        # Sidebar Filter
        st.sidebar.header("Filter Options")
        sensors = combined_df['Sensor_Source'].unique()
        selected_sensor = st.sidebar.selectbox("Select Sensor File", options=["All"] + list(sensors))

        if selected_sensor != "All":
            filtered_df = combined_df[combined_df['Sensor_Source'] == selected_sensor]
        else:
            filtered_df = combined_df

        # Key Metrics Row
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Data Points", len(filtered_df))
        col2.metric("Active Sensors Processed", len(sensors))
        col3.metric("Selected Dataset", selected_sensor)

        # Plot Graphs Dynamically
        st.subheader("Sensor Time-Series Data")
        
        # Automatically select numeric columns (e.g., strain, acceleration)
        numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if numeric_cols:
            selected_col = st.selectbox("Select Sensor Parameter to Plot", numeric_cols)
            
            fig = px.line(
                filtered_df, 
                y=selected_col, 
                color="Sensor_Source" if selected_sensor == "All" else None,
                title=f"{selected_col} Readings Across Sensors",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Raw Sensor Data")
        st.dataframe(filtered_df, use_container_width=True)
