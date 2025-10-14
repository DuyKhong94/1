import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([2, 2, 2])

    
with col1:
    img_url = "https://raw.githubusercontent.com/DuyKhong94/1/8623680f05ca030f6fc8bdbff4041d7abd6a6658/cert-ssblck-belt.jpg"
    st.image(img_url, width=500)
    
    st.title("MASTER PLAN & TO-DO LIST")
    st.write("""This app was developed by Khổng Trung Duy - Certified Six Sigma Black Belt""")
    st.write("""American Society for Quality (ASQ)- ID: 26844""")


    st.markdown(
        "<hr style='border:2px solid #000000; border-radius:5px; width:100%;'>", 
        unsafe_allow_html=True
        )
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xlsb"])
    #doc file excel
    if uploaded_file is not None:
        df= pd.read_excel(uploaded_file,sheet_name="Combine",skiprows=3)
        df.columns = df.columns.str.strip()
        column_to_keep=['TTI Model No','Weekly','Job No','Curent line','QTY']
        df= df[column_to_keep]
        filtered_df = df[df['Job No'].str.startswith(('030','001597','001606','001514','RW030','QB030','ESB030','MP030','SAM030'
                                                      ,'RW001597','RW001606','RW001514','PR001597','PR001606','PR001514'), na=False)]
        selected_line = st.selectbox("Select a line", filtered_df['Curent line'].unique())
        st.write('Jobs On Schedule:')
        st.dataframe(filtered_df[filtered_df['Curent line'] == selected_line])
        st.markdown(
        "<hr style='border:2px solid #000000; border-radius:5px;'>", 
        unsafe_allow_html=True
        )
        top_model = (
        filtered_df
        .groupby(["TTI Model No", "Curent line"], as_index=False)['QTY']
        .sum()
        .sort_values('QTY', ascending=False)
        .head(10)
        )
        top_model1= (filtered_df
        .groupby(["TTI Model No"], as_index=False)['QTY']
        .sum()
        .sort_values('QTY', ascending=False)
        .head(5)
        )
        top5_df=pd.DataFrame(top_model)

        #QTY=filtered_df.sort_values('QTY', ascending=False).head(5)
        st.write("Top 5 Models need focus:")
        st.dataframe(top5_df)
        top5_df1=pd.DataFrame(top_model1)
with col2:  
    st.title("TO-DO LIST")      
    st.markdown(
    "<hr style='border:2px solid #000000; border-radius:5px;'>", 
    unsafe_allow_html=True
    )
            
    todo_list = [
    f"1. Check documents(WI,PCP,PM,Layout,...): {top5_df['TTI Model No'].values.tolist()}",
    "2. Check historical issues.",
    "3. Daily EOL Report.",
    "4. Findings Kaizen Improvement Project.",
    "5. Training Plan."
    ]
    
    for item in todo_list:
        st.write(item)
    import matplotlib.pyplot as plt

    bars=plt.bar(top5_df1['TTI Model No'], top5_df1['QTY'], color='green', edgecolor='black', width=0.4)
    for bar in bars:
        height=bar.get_height()
        width=bar.get_width()
        plt.text(bar.get_x()+width/2, height*1.01,f"{height:.0f}", ha='center', fontsize=7)
    plt.xlabel('Model')
    plt.ylabel('Scheduled QTY')
    plt.title('Top 5 Models AC & BW & PK ')
    st.pyplot(plt)

with col3:
    st.title("Pending Tasks")
    st.markdown(
        "<hr style='border:2px solid #000000; border-radius:5px;'>", 
        unsafe_allow_html=True
        )
    col1, col2= st.columns([1,1])
    with col1:
    
        st.write("WI AC Improvement Status:")
        
        df1= pd.read_excel(r'https://docs.google.com/spreadsheets/d/e/2PACX-1vTD6Hev7ya8IQPQTGkvJzFMlkaE5UpxAPklzrE0fGFNTC1VS4brdqH4BWeyzgeELiCED8B8X5p3T64h/pub?output=xlsx',sheet_name="WI AC")
        df1['TTi Model']=df1['TTi Model'].astype(str).str.strip().str.zfill(9)
        st.dataframe(df1)
    st.markdown(
        "<hr style='border:2px solid #000000; border-radius:5px;'>", 
        unsafe_allow_html=True
        )
    with col1:
        
        st.title("Material Return Cost Monitor")
        
        df2 = pd.read_excel(r'https://docs.google.com/spreadsheets/d/e/2PACX-1vTD6Hev7ya8IQPQTGkvJzFMlkaE5UpxAPklzrE0fGFNTC1VS4brdqH4BWeyzgeELiCED8B8X5p3T64h/pub?output=xlsx', sheet_name="MR")
        selected_mr_model = st.selectbox("Select a line", df2['Line'].unique())
        selected_mr_datefrom=st.selectbox("Select a start date", df2['Date'].unique())
        selected_mr_dateto=st.selectbox("Select a end date", df2['Date'].unique())
        df2mr = df2[(df2['Line'] == selected_mr_model) & (df2['Date'].between(selected_mr_datefrom, selected_mr_dateto))]
        total_cost = df2mr['Price'].sum()
        df21 = df2[df2['Date'].between(selected_mr_datefrom, selected_mr_dateto)]
        df2total = (df21.groupby("Line", as_index=False)["Price"].sum()).sort_values('Price', ascending=False).head(10)
        df2leader=(df21.groupby("Leader",as_index=False)["Price"].sum()).sort_values('Price', ascending=False).head(10)
        st.write(f"Total Material Return Cost for {selected_mr_model} from {selected_mr_datefrom} to {selected_mr_dateto}: ${total_cost:,.2f}")
        
    with col2:
        completed_tasks = (df1['WI status']=="Done").sum()
        total_tasks = len(df1)
        #st.write(f"Completed Tasks: {completed_tasks}")
        #st.write(f"Total Tasks: {total_tasks}")
        plt.figure(figsize=(2, 2))
        plt.pie([completed_tasks, total_tasks - completed_tasks], labels=['Completed', 'Pending'], autopct='%1.1f%%', colors=['#4CAF50', '#FF5733'],textprops={'fontsize': 5})
        
        plt.tight_layout()
        st.pyplot(plt)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
        "<hr style='border:2px solid #000000; border-radius:5px;'>", 
        unsafe_allow_html=True
        )
        plt.figure(figsize=(3, 3))
        bars=plt.bar(df2total['Line'], df2total['Price'], color='skyblue', edgecolor='black', width=0.4)
        for bar in bars:
            height=bar.get_height()
            width=bar.get_width()
            plt.text(bar.get_x()+width/2, height*1.01,f"${height:,.2f}", ha='center', fontsize=7)
        plt.title('MR Amount Ranking')
        plt.xlabel('Line')  
        plt.xticks(rotation=90)
        plt.ylabel('Total Cost ($)')
        st.pyplot(plt)
        #st.dataframe(df2mr)
        plt.figure(figsize=(3, 3))
                bars=plt.bar(df2leader['Leader'], df2leader['Price'], color='skyblue', edgecolor='black', width=0.4)
                for bar in bars:
                    height=bar.get_height()
                    width=bar.get_width()
                    plt.text(bar.get_x()+width/2, height*1.01,f"${height:,.2f}", ha='center', fontsize=7)
                plt.title('MR Amount Ranking')
                plt.xlabel('Leader')  
                plt.xticks(rotation=90)
                plt.ylabel('Total Cost ($)')
                st.pyplot(plt)
        









