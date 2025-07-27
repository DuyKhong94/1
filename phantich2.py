import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Phân tích mode lỗi FVB",
                   page_icon="bar_chart",
                   layout="wide")
upload_file = st.file_uploader("click vào đây để upload file",type=['csv','xlsx'])
if upload_file is not None: 
    if upload_file.name.endswith('.csv'):
        df = pd.read_csv(upload_file)
    else:
        df = pd.read_excel(upload_file)
#st.write('Bạn đã upload file:', upload_file.name)
df.columns=df.columns.str.lower().str.strip().str.replace(' ','_')
df = df.astype(str).apply(lambda x: x.str.strip())
df['test_result'] = df['test_result'].str.lower()
df.rename(columns={'ntcdeldatamin': 'delntcdatamin'}, inplace=True)
df.rename(columns={'ntcdeldatamax': 'delntcdatamax'}, inplace=True)
#st.write("Dữ liệu đã được tải thành công!")
passed_counts = (df['test_result']== 'passed').sum()
failed_counts = (df['test_result']== 'failed').sum()
failure_list = {
    'totalvoltage',
    'usbdischargevoltage',
    'usbdischargecurrent',
    'usbchargevoltage',
    'usbchargecurrent',
    'portchargevoltage',
    'portchargecurrent',
    'ledflashtime',
    'leddutycycle',
    'portdischargevoltage',
    'portdischargecurrent',
    'delntcdata',
}

def detect_failure_mode(row):
    if row['test_result'] == 'passed':
        return None
    failures = []
    try:
        for item in failure_list:
            min_col = item + 'min'
            max_col = item + 'max'
            if min_col in row and max_col in row:
                val = float(row[item])
                val_min = float(row[min_col])
                val_max = float(row[max_col])
                if val < val_min or val > val_max:
                    failures.append(item)
        if failures:
            return failures[0]
        return 'unknown'
    except:
        return 'invalid'

df['failure_mode'] = df.apply(detect_failure_mode, axis=1)
failure_counts = df['failure_mode'].value_counts()
df['failure_mode'] = df.apply(detect_failure_mode, axis=1)
st.sidebar.header("Thống kê hàng lỗi")
result_options = ['All'] + sorted(df['test_result'].unique().tolist())
select_mode = st.sidebar.selectbox("Kết quả", result_options)
if select_mode == 'All':
    df_selection = df[df['test_result'].isin(['passed', 'failed'])]
else:
    df_selection = df[df['test_result'] == select_mode]

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Tổng số sản phẩm:")
    st.subheader(f"{len(df_selection)}")
with middle_column:
    st.subheader("Số sản phẩm Passed:")
    st.subheader(f"{passed_counts}")
with right_column:
    st.subheader("Số sản phẩm Failed:")
    st.subheader(f"{failed_counts}")
st.sidebar.header("Thống kê mode lỗi")



select_failure_mode = st.sidebar.selectbox("Mode lỗi", ['all', 'unknown'] + sorted(list(failure_list)))
if select_failure_mode == 'all':
    df_selection = df_selection[df_selection['test_result'] == 'failed']
else:
    df_selection = df_selection[df_selection['failure_mode'].str.contains(select_failure_mode, na=False)]




plt.figure(figsize=(10, 6))
plt.subplot(2,2,1)
plt.title("Thống kê mode lỗi")  
bars =plt.bar(failure_counts.index, failure_counts.values, color='orange')
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             str(bar.get_height()), ha='center', fontsize=11)

plt.xticks(rotation=90)
plt.ylim(0, failure_counts.max() + 10)
plt.ylabel('Số lượng')

plt.subplot(2,2,2)
bars = plt.bar(['PASSED', 'FAILED'], [passed_counts, failed_counts], color=['green', 'red'])
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             str(bar.get_height()), ha='center', fontsize=11)
plt.ylim(0,max(passed_counts, failed_counts)+500)
plt.ylabel('Số lượng')
plt.title("Tổng số Passed và Failed")

st.pyplot(plt)
img_bytes = BytesIO()
plt.savefig(img_bytes, format='png')
plt.close() 
img_bytes.seek(0)

st.download_button(
    label="📥 Tải biểu đồ PNG",
    data=img_bytes,
    file_name="bieudo_sanluong.png",
    mime="image/png"
)
def highlight_failure(val):
    if val != 'unknown' and val != 'invalid':
        return 'background-color: #ffa07a'
    return ''
with st.expander("📋 Hiện/ẩn bảng dữ liệu"):
    st.dataframe(df_selection.style.applymap(highlight_failure, subset=['failure_mode']))
