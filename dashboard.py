import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Branded Electronics Analytics', page_icon='📊', layout='wide', initial_sidebar_state='expanded')

st.markdown('''<style>
.block-container{padding:.35rem .7rem .2rem!important;max-width:100%!important}
[data-testid="stHeader"]{height:.8rem}
h1{font-size:1.35rem!important;margin:0!important}h2{font-size:1rem!important;margin:.15rem 0!important}
[data-testid="stMetric"]{padding:.25rem .35rem!important}[data-testid="stMetricValue"]{font-size:1.05rem!important}[data-testid="stMetricLabel"]{font-size:.65rem!important}
div[data-testid="stVerticalBlock"]>div{gap:.15rem}.stPlotlyChart,.stPyplot{margin:0!important}
section[data-testid="stSidebar"]{width:190px!important}section[data-testid="stSidebar"]>div{padding-top:.5rem!important}
</style>''', unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('Branded_Electronics_Business_Analytics_Project_Dataset.csv')

data = load_data()
data['Date'] = pd.to_datetime(data['Date'])

st.sidebar.title('🔎 Dashboard Filters')
brands = st.sidebar.multiselect('Select Brand', sorted(data['Brand'].unique()), default=sorted(data['Brand'].unique()))
cities = st.sidebar.multiselect('Select City', sorted(data['City'].unique()), default=sorted(data['City'].unique()))
filtered = data[data['Brand'].isin(brands) & data['City'].isin(cities)].copy()

st.markdown("<h1 style='text-align:center;'>📊 Branded Electronics Business Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-size:.65rem;margin:0 0 .2rem 0;'>Sales • Revenue • Customers • Marketing Analysis</p>", unsafe_allow_html=True)

k1,k2,k3,k4=st.columns(4)
k1.metric('💰 Total Revenue',f"₹{filtered['Revenue'].sum():,.0f}")
k2.metric('📦 Sales Units',f"{filtered['Sales_Units'].sum():,.0f}")
k3.metric('⭐ Customer Rating',f"{filtered['Rating'].mean():.2f}")
k4.metric('🧾 Total Orders',f"{len(filtered):,}")

def small_bar(series,title,xlabel):
    fig,ax=plt.subplots(figsize=(3.7,1.65))
    series.sort_values(ascending=False).plot(kind='bar',ax=ax)
    ax.set_title(title,fontsize=8); ax.set_xlabel(xlabel,fontsize=6); ax.set_ylabel('Revenue',fontsize=6)
    ax.tick_params(axis='x',labelsize=6,rotation=25); ax.tick_params(axis='y',labelsize=5)
    fig.tight_layout(pad=.7); return fig

c1,c2,c3=st.columns(3)
with c1:
    st.pyplot(small_bar(filtered.groupby('Brand')['Revenue'].sum(),'💼 Revenue by Brand','Brand'),use_container_width=True)
with c2:
    st.pyplot(small_bar(filtered.groupby('Product')['Revenue'].sum(),'🛍️ Revenue by Product','Product'),use_container_width=True)
with c3:
    counts=filtered['Customer_Type'].value_counts(); fig,ax=plt.subplots(figsize=(3.7,1.65))
    ax.pie(counts.values,labels=counts.index,autopct='%1.0f%%',textprops={'fontsize':6}); ax.set_title('👥 Customer Type',fontsize=8)
    fig.tight_layout(pad=.5); st.pyplot(fig,use_container_width=True)

c4,c5=st.columns(2)
with c4:
    monthly=filtered.groupby(filtered['Date'].dt.to_period('M'))['Revenue'].sum()
    fig,ax=plt.subplots(figsize=(5.5,1.65)); ax.plot(monthly.index.astype(str),monthly.values,marker='o',linewidth=1.5)
    ax.set_title('📈 Monthly Revenue Trend',fontsize=8); ax.set_xlabel('Month',fontsize=6); ax.set_ylabel('Revenue',fontsize=6)
    ax.tick_params(axis='x',labelsize=5,rotation=45); ax.tick_params(axis='y',labelsize=5); fig.tight_layout(pad=.7); st.pyplot(fig,use_container_width=True)
with c5:
    fig,ax=plt.subplots(figsize=(5.5,1.65)); sns.scatterplot(data=filtered,x='Marketing_Spend',y='Revenue',hue='Brand',s=18,ax=ax,legend=False)
    ax.set_title('🎯 Marketing Spend vs Revenue',fontsize=8); ax.set_xlabel('Marketing Spend',fontsize=6); ax.set_ylabel('Revenue',fontsize=6)
    ax.tick_params(axis='both',labelsize=5); fig.tight_layout(pad=.7); st.pyplot(fig,use_container_width=True)

st.markdown("<div style='font-size:.85rem;font-weight:600;margin-top:.05rem;'>📋 Filtered Sales Data (Preview)</div>",unsafe_allow_html=True)
preview=filtered[['Order_ID','Date','Brand','Product','City','Revenue']].head(3).copy(); preview['Date']=preview['Date'].dt.strftime('%Y-%m-%d')
st.dataframe(preview,hide_index=True,use_container_width=True,height=105)
st.caption('Use the sidebar filters to update all KPIs and charts.')
