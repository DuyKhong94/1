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
    'delntcdata'
}
def detect_failure_mode(row):
    failures = []
    try:
        if float(row['totalvoltage']) < float(row['totalvoltagemin']) and float(row['totalvoltage']) < float(row['totalvoltagemax']):
            failures.append('totalvoltage')
        if float(row['usbdischargevoltage']) < float(row['usbdischargevoltagemin']) and float(row['usbdischargevoltage']) < float(row['usbdischargevoltagemax']):
            failures.append('usbdischargevoltage')
        if float(row['usbdischargecurrent']) < float(row['usbdischargecurrentmin']) and float(row['usbdischargecurrent']) < float(row['usbdischargecurrentmax']):
            failures.append('usbdischargecurrent')
        if float(row['usbchargevoltage']) < float(row['usbchargevoltagemin']) and float(row['usbchargevoltage']) < float(row['usbchargevoltagemax']):
            failures.append('usbchargevoltage')
        if float(row['usbchargecurrent']) < float(row['usbchargecurrentmin']) and float(row['usbchargecurrent']) < float(row['usbchargecurrentmax']):
            failures.append('usbchargecurrent')
        if float(row['portchargevoltage']) < float(row['portchargevoltagemin']) and float(row['portchargevoltage']) < float(row['portchargevoltagemax']):
            failures.append('portchargevoltage')
        if float(row['portchargecurrent']) < float(row['portchargecurrentmin']) and float(row['portchargecurrent']) < float(row['portchargecurrentmax']):
            failures.append('portchargecurrent')
        if float(row['ledflashtime']) < float(row['ledflashtimemin']) and float(row['ledflashtime']) < float(row['ledflashtimemax']):
            failures.append('ledflashtime')
        if float(row['leddutycycle']) < float(row['leddutycyclemin']) and float(row['leddutycycle']) < float(row['leddutycyclemax']):
            failures.append('leddutycycle')
        if float(row['portdischargevoltage']) < float(row['portdischargevoltagemin']) and float(row['portdischargevoltage']) < float(row['portdischargevoltagemax']):
            failures.append('portdischargevoltage')
        if float(row['portdischargecurrent']) < float(row['portdischargecurrentmin']) and float(row['portdischargecurrent']) < float(row['portdischargecurrentmax']):
            failures.append('portdischargecurrent')
        if float(row['delntcdata']) < float(row['ntcdeldatamin']) and float(row['delntcdata']) < float(row['ntcdeldatamax']):
            failures.append('delntcdata')
    except:
        return 'invalid'
    
    if failures:
        return failures[0]  # chỉ lấy lỗi đầu tiên
    else:
        return 'unknown'

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



select_failure_mode = st.sidebar.selectbox("Mode lỗi", ['all'] + sorted(list(failure_list)))
if select_failure_mode == 'all':
    df_selection = df_selection[df_selection['test_result'] == 'failed']
else:
    df_selection = df_selection[df_selection['failure_mode'].str.contains(select_failure_mode, na=False)]



failre_counts = df_selection[df_selection['failure_mode'] != 'unknown']['failure_mode'].value_counts()


plt.figure(figsize=(10, 6))
plt.subplot(2,2,1)
plt.title("Thống kê mode lỗi")
bars =plt.bar(failre_counts.index, failre_counts.values, color='orange')
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             str(bar.get_height()), ha='center', fontsize=11)

plt.xticks(rotation=90)
plt.ylim(0, failre_counts.max() + 10)
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
with st.expander("📋 Hiện/ẩn bảng dữ liệu"):
    st.dataframe(df_selection)