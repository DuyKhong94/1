import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt




st.set_page_config(page_title="DPS Phantomich", page_icon=":guardsman:", layout="wide")

st.title("Daily Production Statistics (DPS) Analysis")

col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://raw.githubusercontent.com/DuyKhong94/1/main/logo.png", width=300, caption="RYOBI PE ACBP Engineering")
    uploaded_file = st.file_uploader("Chọn file dữ liệu", type=["xlsx"])
    if uploaded_file:
        sheet_names = pd.ExcelFile(uploaded_file, engine="openpyxl").sheet_names
        selected_line = st.selectbox("Chọn line có sẵn", sheet_names)
        #custom_line = st.text_input("Hoặc nhập line tùy chỉnh (để trống nếu không dùng)", "")
        line_to_analyze =  selected_line
    
with col2:
    if uploaded_file and line_to_analyze:
        try:
            df_dict = pd.read_excel(uploaded_file,
                                    sheet_name=line_to_analyze,
                                    skiprows=4,
                                    header=None,
                                    engine="openpyxl",
                                    dtype={1: str, 3: str})
            #st.success(f"Đã tải dữ liệu từ sheet: {line_to_analyze}")

            df = df_dict.iloc[:, :18]  # Lấy 18 cột đầu tiên

            column_names = [    
                "job_type", "assy", "family", "tti_model_no", "promise_date",
                "part_line", "manpower", "output", "weekly", "customer",
                "so_number", "qty", "ref", "comment", "job_no",
                "change_over", "total_hours", "need_built_qty"
            ]
            df.columns = column_names
            df = df.dropna(how='all')

            for col in ['assy', 'tti_model_no']:
                df[col] = df[col].apply(lambda x: str(int(float(x))).zfill(9) if pd.notnull(x) else '')
                df[col] = df[col].astype(str).str.strip().str[:9]

            df['working_shift'] = (df['total_hours'].fillna(0) / 7.1).round(0).astype(int)
            df['acc_working_shift'] = df['working_shift'].cumsum()
            df['start_time'] = df['acc_working_shift'] - df['working_shift']

            
            
            

            df_plot1 = df[df['job_no'].notnull()].copy()
            df_plot1['job_no'] = df_plot1['job_no'].astype(str)
            df_plot1 = df_plot1.sort_values(by='acc_working_shift', ascending=False)

            plt.figure(figsize=(10, 5))
            bars = plt.barh(df_plot1['job_no'], df_plot1['working_shift'],
                            left=df_plot1['start_time'], color='skyblue')

            for i, (bar, (_, row)) in enumerate(zip(bars, df_plot1.iterrows())):
                start = float(row['start_time'])
                duration = float(row['working_shift'])
                qty = row['need_built_qty']
                center_x = start + duration / 2
                center_y = bar.get_y() + bar.get_height() / 2

                plt.text(center_x, center_y, f'{int(qty)}',
                        va='center', ha='center', fontsize=9, color='black')

            plt.xlabel('Working Shift')
            plt.ylabel('Job No')
            plt.title('Working Shift by Job No')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)

            st.subheader(f"{line_to_analyze}: thống kê số liệu sản xuất")
            st.write(f"Dữ liệu gồm {df.shape[0]} hàng và {df.shape[1]} cột")
            st.dataframe(df[['job_no', 'need_built_qty', 'total_hours', 'working_shift']], use_container_width=True)

        except Exception as e:
            st.error(f"Lỗi khi đọc sheet {line_to_analyze}: {str(e)}")
    else:
        st.warning("Vui lòng tải file và chọn hoặc nhập line để phân tích.")

with col3:
    st.markdown('Overall Production Statistics')
    if uploaded_file is not None:
        try:
            # Đọc 7 dòng đầu tiên (dòng 0–6)
            df_top = pd.read_excel(
                uploaded_file,
                sheet_name='Summary',
                skiprows=3,
                nrows=3,
                header=None,
                engine="openpyxl"
            )

            # Đọc từ dòng 379 đến 396 (sau khi bỏ dòng 7–378)
            df_bottom = pd.read_excel(
                uploaded_file,
                sheet_name='Summary',
                skiprows=378,
                nrows=18,
                header=None,
                engine="openpyxl"
            )

            # Gộp 2 phần lại
            df_overall = pd.concat([df_top, df_bottom], ignore_index=True)

            # Đặt dòng đầu làm header nếu bạn cần
            df_overall.columns = [f"col_{i}" for i in range(df_overall.shape[1])]

            # Bỏ cột có toàn giá trị 0 hoặc NaN
            df_overall = df_overall.loc[:, (df_overall != 0).any() & df_overall.notna().any()]

            st.dataframe(df_overall)
           

        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}")
    else:

        st.warning("Vui lòng tải lên file Excel trước.")    
