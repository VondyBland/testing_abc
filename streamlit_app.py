
import streamlit as st

st.title("ABC-TESTING")
st.write(
    "Тестирование"
)
import pandas as pd
file_1 = st.file_uploader("Drop your main1 csv data here", type={"csv"},key='1')
file_2 = st.file_uploader("Drop your main2 csv data here", type={"csv"},key='2')
file_3 = st.file_uploader("Drop your main3 csv data here", type={"csv"},key='3')
art_spis = st.file_uploader("Drop your art spisok in excel here", type={"xlsx"},key='4')
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.mandatory_date_range import date_range_picker
from streamlit_extras.stateful_button import button
from datetime import timedelta, datetime 
import pandas as pd 
from datetime import timedelta, datetime


def abc_xyz_analysis(): 
    global final_df
    global xyz_df
    
    start_date = pd.to_datetime(result[0])
    end_date = pd.to_datetime(result[1])
    # periods = int(input('Введите кол-во периодов')) 
    periods = 4
 
    un_df = pd.read_excel(art_spis, sheet_name='Лист1') 
    df = pd.read_csv(file, sep=';') 
    df['Принят в обработку'] = df['Принят в обработку'].astype('datetime64[s]') 
    df = df[df['Принят в обработку'] < end_date].reset_index() 
    df = df[df['Принят в обработку'] >= start_date].reset_index() 
    df['Выручка_итог'] = df['Итоговая стоимость товара'] * df['Количество'] 
    df['Выручка_реал'] = df['Стоимость товара для покупателя'] * df['Количество'] 
    df['Соинвест'] = df['Выручка_реал'] - df['Выручка_итог'] 
 
    main_df = un_df.join(df.groupby(by=['Артикул'])[['Количество', 'Выручка_итог', 'Соинвест']].sum(), on='Артикул', how='left')
    
    main_df['Доля выручки итог'] = (main_df['Выручка_итог'] / main_df['Выручка_итог'].sum()) 
    main_df = main_df.sort_values(by='Выручка_итог', ascending=False) 
    main_df['Накопление_доля_итог'] = main_df['Выручка_итог'].cumsum() / main_df['Выручка_итог'].sum() 
    
    share = main_df['Накопление_доля_итог'] 
    
    def abc(share): 
        if share <= 0.8: 
            return 'A' 
        elif share <= 0.95: 
            return 'B' 
        else: 
            return 'C' 
                
    main_df['ABC'] = main_df['Накопление_доля_итог'].apply(abc) 
    
    df_A = main_df[main_df['ABC'] == 'A'] 
    df_A['new_share'] = df_A['Выручка_итог'] / df_A['Выручка_итог'].sum() 
    df_A = df_A.sort_values(by='new_share', ascending=False) 
    df_A['cumulative_percentage'] = df_A['new_share'].cumsum() 
    df_A['AABBCC'] = df_A['cumulative_percentage'].apply(abc) 
    
    df_B = main_df[main_df['ABC'] == 'B'] 
    df_B['new_share'] = df_B['Выручка_итог'] / df_B['Выручка_итог'].sum() 
    df_B = df_B.sort_values(by='new_share', ascending=False) 
    df_B['cumulative_percentage'] = df_B['new_share'].cumsum() 
    df_B['AABBCC'] = df_B['cumulative_percentage'].apply(abc) 
    
    df_C = main_df[main_df['ABC'] == 'C'] 
    df_C['new_share'] = df_C['Выручка_итог'] / df_C['Выручка_итог'].sum() 
    df_C = df_C.sort_values(by='new_share', ascending=False) 
    df_C['cumulative_percentage'] = df_C['new_share'].cumsum() 
    df_C['AABBCC'] = df_C['cumulative_percentage'].apply(abc) 
    
    final_df = pd.concat([df_A, df_B, df_C]).reset_index(drop=True) 
    final_df['Доля соинвеста'] = final_df['Соинвест'] / final_df['Выручка_итог'] 
 
    # XYZ 
 
    


    xyz_df = df.groupby('Артикул')['Количество'].sum().reset_index()
    period = abs(start_date - end_date) 
    periodsize = timedelta(period.days // periods) 
    per_list = [start_date] 
    for n in range(periods): 
        lala = per_list[n] + periodsize 
        per_list.append(lala) 

    # Подсчет количества заказов в каждом периоде
    for i in range(len(per_list) - 1): 
        period_mask = (df['Принят в обработку'] >= per_list[i]) & (df['Принят в обработку'] < per_list[i+1])
        period_orders = df[period_mask].groupby('Артикул')['Количество'].sum()
        xyz_df[f'{i+1}-период'] = df['Артикул'].map(period_orders).fillna(0)  # Заполняем 0, если нет заказов


    xyz_df['Среднее']= round(xyz_df.iloc[0:,2:].mean(axis=1,numeric_only=True),2)
    xyz_df['Откл']= xyz_df.iloc[:,2:-1].std(axis=1,numeric_only=True)
    xyz_df['Вариация'] = xyz_df['Откл']/xyz_df['Среднее']

    share = xyz_df['Вариация']
    def XYZ(share): 
        if share <= 0.15: 
            return 'X' 
        elif share <= 0.4: 
            return 'Y' 
        else: 
            return 'Z'

    xyz_df['XYZ'] = xyz_df['Вариация'].apply(XYZ)  
        
    
    global data
    data = final_df.merge(xyz_df,on='Артикул',how='left')
    data['full_ABC'] = data['ABC'] + data['AABBCC'] 
    data.sort_values(by='full_ABC', ascending=False)
    df = data.copy()
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


def example_one():
    global filtered_df
    filtered_df = dataframe_explorer(data, case=False)
    st.dataframe(filtered_df, use_container_width=True)

result = date_range_picker("Select a date range")
if button("Button 1", key="button1"):
    st.write("Начинаем расчеты")
    file = pd.concat([file_1,file_2,file_3], ignore_index=True, sort=False)
    if (file != None) & (art_spis!=None) &(result!=None): 
            abc_xyz_analysis()

