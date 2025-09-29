import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


df = pd.read_csv("hotel_bookings.csv")
st.write(df.head())

st.markdown("<h1 style='text-align: center; color: darkpink; font-size: 42px;'>📊Analiza danych operacyjnych hotelu</h1>", unsafe_allow_html=True)

if st.checkbox("🔍 Pokaż dane źródłowe"):
    st.dataframe(df.head())

hotel_option = st.selectbox("Wybierz typ hotelu:", ["Wszystkie", "City Hotel", "Resort Hotel"])

if hotel_option != "Wszystkie":
    df = df[df['hotel'] == hotel_option]


st.header("1. Status rezerwacji (anulowane vs. potwierdzone)")

cancel_counts = df['is_canceled'].value_counts().reset_index()
cancel_counts.columns = ['status', 'count']
cancel_counts['status'] = cancel_counts['status'].map({0: 'Zrealizowana', 1: 'Anulowana'})

fig2 = px.pie(cancel_counts, names='status', values='count', title='Status rezerwacji')
st.plotly_chart(fig2, use_container_width=True)

st.header("2. Status rezerwacji a typ klienta")


selected_status = st.radio("Wybierz status rezerwacji:", ['Wszystkie', 'Zrealizowana', 'Anulowana'])
status_map = {'Zrealizowana': 0, 'Anulowana': 1}
if selected_status != 'Wszystkie':
    df_filtered = df[df['is_canceled'] == status_map[selected_status]]
else:
    df_filtered = df

cancel_by_type = df_filtered.groupby('customer_type')['is_canceled'].mean().reset_index()
cancel_by_type['is_canceled'] *= 100  

fig = px.bar(cancel_by_type, x='customer_type', y='is_canceled',
             labels={'is_canceled': '% anulowanych'},
             title=f'Anulacje wg typu klienta{" – "+selected_status if selected_status != "Wszystkie" else ""}',
             text=cancel_by_type['is_canceled'].round(1))
fig.update_traces(textposition='outside')
st.plotly_chart(fig)

cancel_by_month= df.groupby('arrival_date_month')['is_canceled'].mean().reset_index()
cancel_by_month['is_canceled']*=100

month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
cancel_by_month['arrival_date_month'] = pd.Categorical(cancel_by_month['arrival_date_month'],
                                                       categories=month_order, ordered=True)
cancel_by_month = cancel_by_month.sort_values('arrival_date_month')

fig= px.bar(cancel_by_month, x='arrival_date_month', y='is_canceled',
            labels={'is_canceled': '% anulowanych'},
            title='Anulacje wg miesiąca przyjazdu')
          
st.plotly_chart(fig)