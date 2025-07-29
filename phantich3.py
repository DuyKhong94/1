import pandas as pd
import numpy as np
import streamlit as st


st.set_page_config(page_title="MR USD Dollar Cost Analysis")
cost_file = "https://github.com/DuyKhong94/1/blob/main/Material%20saving%20study%20cost%20Oct2024.xlsb?raw=true"
df = pd.read_excel(cost_file, engine='pyxlsb', sheet_name='Sheet1')

df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df = df.dropna(subset=['unit_price', 'item','description'])
df = df.drop_duplicates(subset='item', keep='first')
df['item'] = df['item'].astype(str).str.strip().str.lstrip("'").str.upper()
df_cleaned= df[['item','description','unit_price']].copy()
st.write(df_cleaned.head(10))
st.title("MR USD Dollar Cost Analysis")
col1,col2=st.columns(2)
with col1:
    item_number = st.text_input("nhập mã linh kiện").strip().upper()
with col2:
    quantity = st.number_input("nhập số lượng", min_value=1, value=1, step=1)

if st.button('tra cứu'):
    result = df[df['item'] == item_number]
    if not result.empty:
        price = result.iloc[0]['unit_price']
        desc = result.iloc[0]['description']
        total = price * quantity
        
        st.success(f"✅ Đã tìm thấy mã: `{item_number}`")
        st.write(f"📦 **Mô tả**: {desc}")
        st.write(f"💵 **Đơn giá**: {price:,.0f} $USD")
        st.write(f"🧾 **Thành tiền**: {total:,.0f} $USD")
    else:
        st.error("❌ Không tìm thấy mã linh kiện.")

