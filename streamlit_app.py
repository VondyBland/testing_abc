
import streamlit as st

st.title("ABC-TESTING")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import pandas as pd
file = st.file_uploader("Drop your CSV here to load to Snowflake", type={"csv"})
import plotly.express as px

if file != None: 
    df = pd.read_csv(file)
    df['Соинвест'] = abs(df['Соинвест'])

    # Создаем интерактивную визуализацию
    fig = px.scatter(df,
                    x='Выручка_итог',
                    y='Соинвест',
                    color='full_ABC',
                    hover_name='Артикул',
                    title='Интерактивная визуализация данных')

    # Отображаем визуализацию
    st.plotly_chart(fig, use_container_width=True)
