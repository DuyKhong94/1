import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Cycle Time Analysis App")

# Step 1: Upload file
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Step 2: Đọc file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

   # # Step 3: Kiểm tra cột cần thiết
   # required_cols = ['time', 'test_result']
   # if not all(col in df.columns for col in required_cols):
   #     st.error("File must contain columns: 'time' and 'test_result'")
   #     st.stop()

    # Step 4: Tiền xử lý
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df['test_result'] = df['test_result'].astype(str).str.strip().str.upper()
    total_passed = (df['test_result'] == 'PASSED').sum()
    total_failed = (df['test_result'] == 'FAILED').sum()

    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['CT'] = df['time'].diff().dt.total_seconds()
    df_filtered = df[(df['CT'] < 65) & (df['CT'] > 15)]

    mean_ct = df_filtered['CT'].mean()
    median_ct = df_filtered['CT'].median()
    q1 = np.percentile(df_filtered['CT'], 25)
    q3 = np.percentile(df_filtered['CT'], 75)
    lw = np.percentile(df_filtered['CT'], 2.5)
    upp = np.percentile(df_filtered['CT'], 97.5)
    est_output_per_hour = int(round(3600 / mean_ct)) if mean_ct else 0

    # Step 5: Thông tin tổng quan
    st.subheader("📊 Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Passed", total_passed)
    col2.metric("Total Failed", total_failed)
    col3.metric("Estimated Output/hour", est_output_per_hour)

    # Step 6: Biểu đồ
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))

    # Biểu đồ Passed vs Failed
    colors = ['green', 'red']
    bars = axs[0, 0].bar(['PASSED', 'FAILED'], [total_passed, total_failed], color=colors)
    axs[0, 0].set_title("Total Passed and Failed")
    axs[0, 0].set_ylim(0, max(total_passed, total_failed) + 100)
    for bar in bars:
        axs[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                       str(bar.get_height()), ha='center', fontsize=11)

    # Line chart CT
    axs[0, 1].plot(df_filtered['CT'].values, marker='o', markersize=3,
                   label=f'Output/hour ≈ {est_output_per_hour}')
    axs[0, 1].axhline(mean_ct, color='red', label=f'Mean = {mean_ct:.2f}s')
    axs[0, 1].set_ylim(0, 100)
    axs[0, 1].set_title("Cycle Time Statistics")
    axs[0, 1].legend(fontsize=9, loc='upper right')

    # Histogram
    axs[1, 0].hist(df_filtered['CT'].dropna(), bins=30, color='skyblue', edgecolor='black')
    axs[1, 0].axvline(mean_ct, color='red', linestyle='--', label=f'Mean = {mean_ct:.2f}')
    axs[1, 0].axvline(median_ct, color='orange', linestyle='--', label=f'Median = {median_ct:.2f}')
    axs[1, 0].axvline(lw, color='black', linestyle='--', label=f'Low = {lw:.2f}')
    axs[1, 0].axvline(upp, color='black', linestyle='--', label=f'High = {upp:.2f}')
    axs[1, 0].set_title("Cycle Time Distribution")
    axs[1, 0].legend(fontsize=9)

    # Boxplot
    axs[1, 1].boxplot(df_filtered['CT'], vert=True, patch_artist=True)
    axs[1, 1].axhline(median_ct, color='red', linestyle='--', label=f'Median = {median_ct:.2f}')
    axs[1, 1].axhline(q1, color='black', linestyle='--', label=f'Q1 = {q1:.2f}')
    axs[1, 1].axhline(q3, color='black', linestyle='--', label=f'Q3 = {q3:.2f}')
    axs[1, 1].set_title("Cycle Time Boxplot")
    axs[1, 1].legend(fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)

    # Step 7: Bảng dữ liệu lọc
    st.subheader("Raw Data")
    st.dataframe(df_filtered)

    # Step 8: Tải bảng kết quả
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download filtered data as CSV",
                       csv,
                       "filtered_ct_data.csv",
                       "text/csv")