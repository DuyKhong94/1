import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

    st.set_page_config(page_title="MR USD Dollar Cost Analysis")
    cost_file="https://github.com/DuyKhong94/1/blob/main/Material%20saving%20study%20cost%20Oct2024.xlsb?raw=true"
    df = pd.read_excel(cost_file, engine='pyxlsb', sheet_name='Sheet1')
    
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    df = df.dropna(subset=['unit_price', 'item','description'])
    df = df.drop_duplicates(subset='item', keep='first')
    df['item'] = df['item'].astype(str).str.strip().str.lstrip("'").str.upper()
    df_cleaned= df[['item','description','unit_price']].copy()

    st.title("MR USD Dollar Cost Analysis")
    col1,col2=st.columns(2)
    with col1:
        item_number = st.text_input("nhập mã linh kiện").strip().upper()
    with col2:
        quantity = st.number_input("nhập số lượng", min_value=1, value=1, step=1)
        
    if st.button('📌 Tra cứu'):
        result = df[df['item'] == item_number]
        if not result.empty:
            price = result.iloc[0]['unit_price']
            desc = result.iloc[0]['description']
            total = price * quantity
    
            st.success(f"✅ Đã tìm thấy mã: `{item_number}`")
            st.write(f"📦 **Mô tả**: {desc}")
            st.write(f"💵 **Đơn giá**: {price:,.0f} $USD")
            st.write(f"🧾 **Thành tiền**: {total:,.0f} $USD")
    
            # Ghi vào lịch sử tra cứu
            if "history" not in st.session_state:
                st.session_state.history = []
    
            st.session_state.history.append({
                "Mã linh kiện": item_number,
                "Mô tả": desc,
                "Đơn giá ($USD)": price,
                "Số lượng": quantity,
                "Thành tiền ($USD)": total
            })
        else:
            st.error("❌ Không tìm thấy mã linh kiện.")
    col3,col4=st.columns(2)
    with col3:
        model_number = st.text_input("nhập mã model").strip().upper()
    with col4:
        job_quantity = st.number_input("nhập số lượng job", min_value=1, value=1, step=1)
    if st.button('📌 Tra cứu giá console'):
        result1 = df[df['item'] == model_number]
        if not result1.empty:
            price = result1.iloc[0]['unit_price']
            total = price * job_quantity
    
            st.success(f"✅ Đã tìm thấy mã: `{model_number}`")
            st.write(f"💵 **Đơn giá**: {price:,.0f} $USD")
            st.write(f"🧾 **Thành tiền**: {total:,.0f} $USD")
    
            # Ghi vào lịch sử tra cứu
            if "history1" not in st.session_state:
                st.session_state.history1 = []

            st.session_state.history1.append({
                "Mã console": model_number,
                "Mô tả": "Giá console",
                "Đơn giá ($USD)": price,
                "Số lượng": job_quantity,
                "Thành tiền ($USD)": total
            })
        else:
            st.error("❌ Không tìm thấy mã console.")
    # Hiển thị lịch sử nếu có
    if "history" in st.session_state and st.session_state.history:
        st.markdown("---")
        st.subheader("📋 Lịch sử tra cứu linh kiện")
        df_history = pd.DataFrame(st.session_state.history)
        st.dataframe(df_history, use_container_width=True)
    if "history1" in st.session_state and st.session_state.history1:
        st.markdown("---")
        st.subheader("📋 Lịch sử tra cứu giá console")
        df_history1 = pd.DataFrame(st.session_state.history1)
        st.dataframe(df_history1, use_container_width=True)
    item_list=df_history['Mã linh kiện'].unique().tolist()
    total_cost = df_history['Thành tiền ($USD)'].sum()
    total_job_cost = df_history1['Thành tiền ($USD)'].sum()

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 2, 1)
    bars=plt.bar(item_list, df_history.groupby('Mã linh kiện')['Thành tiền ($USD)'].sum().loc[item_list])
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:,.0f}", ha='center', va='bottom')
    plt.title("Chi phí theo mã linh kiện")
    plt.xlabel("Mã linh kiện")
    plt.ylabel("Thành tiền ($USD)")

    plt.subplot(2, 2, 2)
    bars1 = plt.bar(['Tổng giá trị', 'Total scrapped'], [total_job_cost,total_cost], color=['blue', 'red'])
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:,.0f}", ha='center', va='bottom')
    plt.title("Chi phí scrap tính theo tổng giá trị job")
    plt.ylabel("USD$")
    plt.subplot(2,2,3)
    plt.pie([total_job_cost, total_cost], labels=['Tổng giá trị', 'Total scrapped'], autopct='%1.1f%%', startangle=90)
    plt.title("Tỷ lệ chi phí tổng giá trị và tổng chi phí scrap")

    plt.legend(
        labels=['Tổng giá trị', 'Total scrapped'],
        loc='upper left',
        bbox_to_anchor=(1, 1),  # đưa legend sang bên phải
        frameon=False
    )
    plt.tight_layout()
    st.pyplot(plt)
    st.markdown(f"### Tổng chi phí: {total_cost:,.0f} $USD")







