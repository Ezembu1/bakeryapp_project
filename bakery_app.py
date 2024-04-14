import pandas as pd
import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt 
from urllib.error import URLError

# load data function ( is used to load the data, all data cleaning is done under the load data function)
@st.cache_data 
def load_data():
    df = pd.read_csv("Bakery sales.csv")
    df = df.drop(columns="Unnamed: 0", axis=1)
    df['unit_price'] = df['unit_price'].str.replace(",",".").str.replace(" €","")
    df['unit_price'] = df["unit_price"].astype("float")
    sales = df.Quantity * df.unit_price
    df["sales"] = sales
    df = df.rename(columns={'unit_price':"unit_price (€)"}) 
    return df


df = load_data()
try:
    # to display your table
    st.subheader("Table Preview")
    st.dataframe(df.head())


    # add a filter 
    articles = df['article'].unique()
    selected_article = st.sidebar.multiselect("Select a product",articles,articles[1])

    # show a table based on the selection
    st.subheader("Preview Your Selected Articles")
    temp_table = df[df['article'].isin(selected_article)]
    if not selected_article:
        st.error('Please select a product')
    else:
        st.dataframe(temp_table.sample(6))

     # columns 
    col1, col2, col3 = st.columns(3)
    # total number of products 
    total_products = df['article'].nunique()
    selected_products = temp_table["article"].nunique()
    if not selected_products:
        col1.metric("Total No. of Products", total_products)
    else:
        col1.metric("Products", selected_products)

    # Total Quantity sold 
    total_qty = np.sum(df['Quantity'])
    selected_qty = np.sum(temp_table["Quantity"])
    if not selected_qty:
        col2.metric("Total Quantity of Items Sold", f'{total_qty:,}')
    else:
        col2.metric("Items Sold", f'{selected_qty:,}')

    # Total sales 
    total_sales = np.sum(df['sales'])
    selected_sales = np.sum(temp_table["sales"])
    if not selected_sales:
        col3.metric("Total Sales", f'{total_sales:,}')
    else:
        col3.metric("Sales", f'{selected_sales:,}')


    # plots
    st.header("Plotting")

    # data
    article_grp = df.groupby('article')['sales'].sum()
    article_grp = article_grp.sort_values(ascending=False)[:-3]
    temp_table2 = article_grp.reset_index()

    # Bring in selection from the filter 
    temp_table3 = temp_table2[temp_table2["article"].isin(selected_article)]

    # plot filtered selection
    fig1, ax1 = plt.subplots(figsize=(7,5))
    ax1.bar(temp_table3['article'],temp_table3['sales'])
    st.pyplot(fig1)
    

    # for pie plot
    st.subheader("Pie chart")
    fig2, ax2 = plt.subplots(figsize=(7,5))
    ax2.pie(temp_table3['sales'],
            labels=selected_article,
            autopct="%1.1f%%")
    st.pyplot(fig2)
    

except URLError as e:
    st.error(
        """
        **Error message: %s
    """
         % e.reason
    )
     
# st.dataframe(df)


    