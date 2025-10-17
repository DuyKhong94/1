import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(page_title="MR Analysis & Ranking")
col1,col2=st.columns([1,1])
with col1:
    
        st.title("MR Ranking Analysis")  
        st.divider()
        df2 = pd.read_excel(r'https://docs.google.com/spreadsheets/d/e/2PACX-1vTD6Hev7ya8IQPQTGkvJzFMlkaE5UpxAPklzrE0fGFNTC1VS4brdqH4BWeyzgeELiCED8B8X5p3T64h/pub?output=xlsx', sheet_name="MR")
        with st.container():
            selected_mr_model = st.selectbox("Select a line", df2['Line'].unique())
            selected_mr_datefrom=st.selectbox("Select a start date", df2['Date'].unique())
            selected_mr_dateto=st.selectbox("Select a end date", df2['Date'].unique())
        df2mr = df2[(df2['Line'] == selected_mr_model) & (df2['Date'].between(selected_mr_datefrom, selected_mr_dateto))]
        total_cost = df2mr['Price'].sum()
        df21 = df2[df2['Date'].between(selected_mr_datefrom, selected_mr_dateto)]
        df2total = (df21.groupby("Line", as_index=False)["Price"].sum()).sort_values('Price', ascending=False).head(5)
        df2leader=(df21.groupby("Leader",as_index=False)["Price"].sum()).sort_values('Price', ascending=False).head(5)
        total_cost=df21["Price"].sum()
        total_cost_leader=df2.groupby("Leader",as_index=False)["Price"].sum()
        total_cost_leader = total_cost_leader.sort_values("Price", ascending=False)
        top5 = total_cost_leader.head(5)
        others = pd.DataFrame({
        "Leader": ["Others"],
        "Price": [total_cost_leader["Price"].iloc[5:].sum()]
        })
        st.write(f"Total Material Return Cost for {selected_mr_model} from {selected_mr_datefrom} to {selected_mr_dateto}: ${total_cost:,.2f}")
        df_pie = pd.concat([top5, others], ignore_index=True)
        st.divider()
        plt.figure(figsize=(3, 3))
        bars=plt.bar(df2total['Line'], df2total['Price'], color='skyblue', edgecolor='black', width=0.4)
        for bar in bars:
            height=bar.get_height()
            width=bar.get_width()
            plt.text(bar.get_x()+width/2, height*1.01,f"${height:,.2f}", ha='center', fontsize=7)
        plt.title('AC PK BW Scrap Ranking by Line')
        plt.xlabel('Line')  
        plt.xticks(rotation=90)
        plt.ylabel('Total Cost ($)')
        st.pyplot(plt)
        plt.figure(figsize=(4, 4))
        bars=plt.bar(df2leader['Leader'], df2leader['Price'], color='skyblue', edgecolor='black', width=0.4)
        for bar in bars:
            height=bar.get_height()
            width=bar.get_width()
            plt.text(bar.get_x()+width/2, height*1.01,f"${height:,.2f}", ha='center', fontsize=7)
        plt.title('AC PK BW Scrap Ranking by Leader')
        plt.xlabel('Leader')  
        plt.xticks(rotation=90)
        plt.ylabel('Total Cost ($)')
        st.pyplot(plt)
  
        plt.figure(figsize=(5, 5))
        plt.pie(
        df_pie["Price"],
        autopct='%1.1f%%',
        startangle=90,
        counterclock=False
        )
        plt.title("AC PK BW Scrap Contribute by Leader")
        plt.legend(
        df_pie["Leader"],
        loc="lower center",
        bbox_to_anchor=(1, 0.5),
        title="Leader",
        fontsize=5
        )
        plt.tight_layout()
        st.pyplot(plt)        
with col2: 
    st.title("MR USD Dollar Cost Analysis")
    st.divider()
    cost_file="https://github.com/DuyKhong94/1/blob/main/Material%20saving%20study%20cost%20Oct2024.xlsb?raw=true"
    df = pd.read_excel(cost_file, engine='pyxlsb', sheet_name='Sheet1')
    
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    df = df.dropna(subset=['unit_price', 'item','description'])
    df = df.drop_duplicates(subset='item', keep='first')
    df['item'] = df['item'].astype(str).str.strip().str.lstrip("'").str.upper()
    df_cleaned= df[['item','description','unit_price']].copy()
    
    
    col1,col2=st.columns(2)
    with col1:
        item_number = st.text_input("nhập mã linh kiện").strip().upper()
    with col2:
        quantity = st.number_input("nhập số lượng", min_value=1, value=1, step=1)
        
    if st.button('📌 Tra cứu'):
        if item_number and quantity:
            result = df[df['item'] == item_number]
        if not result.empty:
            price = result.iloc[0]['unit_price']
            desc = result.iloc[0]['description']
            total = price * quantity
    
            st.success(f"✅ Đã tìm thấy mã: `{item_number}`")
            st.write(f"📦 **Mô tả**: {desc}")
            st.write(f"💵 **Đơn giá**: {price:,.5f} $USD")
            st.write(f"🧾 **Thành tiền**: {total:,.5f} $USD")
    
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
        if model_number and job_quantity:
            result1 = df[df['item'] == model_number]
        if not result1.empty:
            price = result1.iloc[0]['unit_price']
            total = price * job_quantity
    
            st.success(f"✅ Đã tìm thấy mã: `{model_number}`")
            st.write(f"💵 **Đơn giá**: {price:,.5f} $USD")
            st.write(f"🧾 **Thành tiền**: {total:,.5f} $USD")
    
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
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:,.5f}", ha='center', va='bottom')
    plt.title("Chi phí theo mã linh kiện")
    plt.xlabel("Mã linh kiện")
    plt.ylabel("Thành tiền ($USD)")
    
    plt.subplot(2, 2, 2)
    bars1 = plt.bar(['Tổng giá trị', 'Total scrapped'], [total_job_cost,total_cost], color=['blue', 'red'])
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:,.5f}", ha='center', va='bottom')
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
    st.markdown(f"### Tổng chi phí: {total_cost:,.5f} $USD")











