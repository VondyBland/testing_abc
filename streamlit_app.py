
import streamlit as st

st.title("ABC-TESTING")
st.write(
    "Тестирование"
)
import pandas as pd
file = st.file_uploader("Drop your CSV here to load to Snowflake", type={"csv"})
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer

def example_one():
    global filtered_df
    filtered_df = dataframe_explorer(df, case=False)
    st.dataframe(filtered_df, use_container_width=True)

if file != None: 
    df = pd.read_csv(file)
    example_one()

    df['Соинвест'] = abs(df['Соинвест'])

    # Создаем интерактивную визуализацию
    fig = px.scatter(filtered_df,
                    x='Выручка_итог',
                    y='Соинвест',
                    color='full_ABC',
                    hover_name='Артикул',
                    title='Интерактивная визуализация данных')

    # Отображаем визуализацию
    st.plotly_chart(fig, use_container_width=True)
