import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="ecommerce",page_icon=":chart_with_upwards_trend:",layout="wide")
if st.button("Home"):
    st.switch_page("home.py")
st.title(":bar_chart: Indian ecommerce sales analysis")
# try API
import requests

url = "https://currency-convertor21.p.rapidapi.com/"
querystring = {"from":"USD","to":"INR","input":"1"}  
headers = {
    "x-rapidapi-key": "dc6949fc14mshb12d1b4b07b59ebp161db9jsn0d4948ee2709",
    "x-rapidapi-host": "currency-convertor21.p.rapidapi.com"
}

try:
    response = requests.get(url, headers=headers, params=querystring, timeout=5)
    data = response.json()
    usd_to_inr = data.get("result") or data.get("INR") or 83.0   # fallback
except Exception as e:
    usd_to_inr = 83.0   # fallback when API fails

print("✅ USD to INR:", usd_to_inr)
df = pd.read_csv("indian_ecommerce2.csv")
col1,col2=st.columns((2))
df["Order Date"]= pd.to_datetime(df["Order Date"])

#getting the  min and  max date
startDate=pd.to_datetime(df["Order Date"]).min()
endDate=pd.to_datetime(df["Order Date"]).max()
with col1:
    date1= pd.to_datetime(st.date_input("Start Date",startDate))
with col2:
    date2= pd.to_datetime(st.date_input("End Date",endDate))
df=df[(df["Order Date"]>=date1)&(df["Order Date"]<=date2)].copy()
st.sidebar.header("choose your filter:")
#create for region
region=st.sidebar.multiselect("Pick your region",df["Region"].unique())
if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)]
#create for state
state= st.sidebar.multiselect("Pick the state",df2["State"].unique())
if not state:
    df3=df2.copy()
else:
    df3=df2[df2["State"].isin(state)]
#create for city
city=st.sidebar.multiselect("Pick the City:",df3["City"].unique())
#filter the  data based on Region,State and City
if not region and not  state  and not city:
    filtered_df=df
elif not  state and not city:
    filtered_df=df3[df3["Region"].isin(region)]
elif not  region and not city:
    filtered_df=df3[df3["State"].isin(state)]
elif state and city:
    filtered_df=df3[df3["State"].isin(state)&df3["City"].isin(city)]
elif region and city:
    filtered_df=df3[df3["Region"].isin(region)&df3["City"].isin(city)]
elif state and region:
    filtered_df=df3[df3["State"].isin(state)&df3["Region"].isin(region)]
elif city:
    filtered_df=df3[df3["City"].isin(city)]
else:
    filtered_df=df3[df3["Region"].isin(region)&df3["State"].isin(state)&df3["City"].isin(city)]
category_df=filtered_df.groupby(by=["Category"],as_index=False)["Sales"].sum()
with col1:
    st.subheader("Category Wise Sales:")
    fig = px.bar(
        category_df,
        x="Category",
        y="Sales",
        text=[f"₹{x*usd_to_inr:,.2f}" for x in category_df['Sales']],
        color="Category",
        color_discrete_sequence=['#5DADE2', '#2874A6', '#16A085', '#48C9B0', '#ABB2B9']
    )

    # Increase bar width
    fig.update_traces(width=0.9)  # default is ~0.4, you can try 0.6, 0.7 etc.

    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )

    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Region Wise Sales:")
    fig=px.pie(filtered_df,values="Sales",names="Region",hole=0.5,
               color_discrete_sequence=['#5DADE2', '#2874A6', '#16A085', '#48C9B0', '#ABB2B9'])
    fig.update_traces(text=filtered_df['Region'],textposition="outside")
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig,use_container_width=True)
cl1,cl2=st.columns(2)
with cl1:
    with st.expander("Category_VeiwData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv=category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data=csv,file_name="Category.csv",mime="text/csv",
                           help="Click here to download the data  as csv file:")
with cl2:
    with st.expander("Region_VeiwData"):
        region=filtered_df.groupby(by="Region",as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv=region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data=csv,file_name="Region.csv",mime="text/csv",
                           help="Click here to download the data  as csv file:")
        st.subheader("Time Series Analysis")
linechart = (
    filtered_df
    .groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)
linechart["month_year"] = linechart["Order Date"].astype(str)
fig2=px.line(linechart,x="month_year",y="Sales",labels={"Sales":"Amount"},height=500,width=1000,
             color_discrete_sequence=['#5DADE2'])
fig2.update_layout(template='plotly_dark', plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
st.plotly_chart(fig2,use_container_width=True)
with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')
#create treemap based on Region,category,sub-category

st.subheader("Hierarchical view of Sales Data using TreeMap")

# Updated color palette with the new specified colors
category_colors = {
    "Home & Kitchen": "#5DADE2",   # Light Blue
    "Fashion": "#2874A6",          # Steel Blue
    "Books": "#16A085",            # Teal
    "Beauty & Personal Care": "#48C9B0", # Light Teal
    "Electronics": "#ABB2B9",      # Silver Gray
    "Sports & Fitness": "#F4F6F7"  # Off-White
}

# Region colors using the new palette
region_colors = {
    'North': "#5DADE2",      # Light Blue
    'South': "#2874A6",      # Steel Blue
    'East': "#16A085",       # Teal
    'West': "#48C9B0",       # Light Teal
    'Central': "#ABB2B9"     # Silver Gray
}

# Create a custom color mapping function
def color_map(category):
    if category in category_colors:
        return category_colors[category]
    
    # For regions, use the region colors
    if category in region_colors:
        return region_colors[category]
    
    # Default color if not found
    return '#5DADE2'

# Create a new column for coloring
filtered_df['color_col'] = filtered_df.apply(
    lambda row: row['Region'] if row['Region'] in region_colors else row['Category'], 
    axis=1
)

fig3 = px.treemap(
    filtered_df,
    path=["Region", "Category", "Sub-Category"],
    values="Sales",
    hover_data=["Sales"],
    color="color_col",
    color_discrete_map={**region_colors, **category_colors}
)

# Enhanced border for better contrast and white font color
fig3.update_traces(
    marker=dict(
        line=dict(
            width=2,  # Thicker border for better visibility
            color='#000000'  # Pure black for maximum contrast
        )
    ),
    textfont=dict(color='white', size=14),  # White font color for better readability
    textposition='middle center',
    texttemplate='<b>%{label}</b><br>₹%{value:,.0f}',
    hovertemplate='Sales: ₹%{value:,.2f}'


)

# Match with dark theme with settings to show all text
fig3.update_layout(
    width=800,
    height=650,
    margin=dict(t=40, l=10, r=10, b=10),
    paper_bgcolor="#1E1E1E",  # dark grey background
    plot_bgcolor="#1E1E1E",
    font=dict(color="white", size=14),
    uniformtext=dict(minsize=10, mode=False)  # Show all text, don't hide any
)

st.plotly_chart(fig3, use_container_width=True)
chart1,chart2=st.columns((2))
with chart1:
    st.subheader('Segment Wise Sales')
    fig=px.pie(filtered_df,values="Sales",names="Segment",template="plotly_dark",
               color_discrete_sequence=['#5DADE2', '#2874A6', '#16A085', '#48C9B0'])
    fig.update_traces(text=filtered_df["Segment"],textposition="inside")
    st.plotly_chart(fig,use_container_width=True)
with chart2:
    st.subheader('Category Wise Sales')
    fig=px.pie(filtered_df,values="Sales",names="Category",template="plotly_dark",
               color_discrete_sequence=['#5DADE2', '#2874A6', '#16A085', '#48C9B0', '#ABB2B9'])
    fig.update_traces(text=filtered_df["Category"],textposition="inside")
    st.plotly_chart(fig,use_container_width=True)
import plotly.figure_factory as ff
st.subheader(":point_right: Monthly wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample =df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig=ff.create_table(df_sample,colorscale=[[0, '#16A085'], [0.5, '#48C9B0'], [1, '#5DADE2']])
    fig.update_layout(
        font=dict(color="white"),
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E"
    )
    st.plotly_chart(fig,use_container_width=True)
st.markdown("Month wise Sub-category Table")
filtered_df["month"]=filtered_df["Order Date"].dt.month_name()
sub_category_year= pd.pivot_table(data=filtered_df,values="Sales",index=["Sub-Category"],columns="month")
st.write(sub_category_year.style.background_gradient(cmap="Blues"))
data1 = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    size="Quantity"
)
data1.update_layout(
    title=dict(
        text="Relationship between Sales and Profits Using Scatter Plot",
        font=dict(size=20)
    ),
    xaxis=dict(
        title=dict(text="Sales", font=dict(size=19))
    ),
    yaxis=dict(
        title=dict(text="Profit", font=dict(size=19))
    )
)


st.plotly_chart(data1,use_container_width=True)
with st.expander("View Data"):
    st.write(
        filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Blues")
    )

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Data",
    data=csv,
    file_name="Data.csv",
    mime="text/csv"
)
st.markdown("---")
st.subheader(" Want to talk to Chatbot?")

st.write("Click the button below to open our smart assistant for help and insights.")

if st.button("💬 Open Chatbot"):
    st.switch_page("pages/chatbot.py")
