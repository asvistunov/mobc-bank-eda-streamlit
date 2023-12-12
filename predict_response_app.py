import random
from matplotlib.pylab import rand
import pandas as pd
import seaborn.objects as so
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from wordcloud import WordCloud
import matplotlib.pyplot as plt


from preprocess_data import clients_extended

st.set_page_config(
    page_icon='random',
    layout="wide"
)

color_sequence = ('#09b2ec', '#a97c72', '#7b3f48', '#F1e3aa', '#cda57a', '#b0c9cc', '#676561')

def plot_styled(so):
    fig = plt.figure(figsize=[10, 7])

    (
        so
        .theme(
        {
            'axes.grid': False,
            'axes.facecolor':'white',
            'xtick.color': 'black',
            'ytick.color': 'black',
            'axes.linewidth':1.3,
            'axes.edgecolor':'lightgrey',
            'axes.spines.left': True,
            'axes.spines.bottom': True,
            'axes.spines.right': False,
            'axes.spines.top': False

        }
    )
        .on(fig)
        .plot()
    )

    return fig

st.title('Отклик на маркетинговую компанию')
st.header('Исследуем отклик на маркетинговые компании')
st.write('Данные для исследования - информация о клиенах банка, и их отклик на маркетинговую компанию')

st.image('datasets/bank_marketing.png')
# st.divider()

tab1, tab2, tab3 = st.tabs(["Демография", "Работа и финансы", "Реакция на маркетинговую компанию"])

with tab1:
    st.subheader('Распределение возраста клиентов')

    fig = px.histogram(
        clients_extended, 
        x="age", 
        color="gender_desc",
        template='simple_white',
        color_discrete_sequence=color_sequence,
        barmode="overlay",
        opacity=0.7,
        marginal="box",
        labels={
            'gender_desc': 'Пол'
        }
        # hover_data=df.columns,

    ).update_layout(
        xaxis_title_text = '', 
        yaxis_title_text = 'Количество клиентов',
        xaxis = {
            'tickmode': 'linear',
            'dtick': 5
        },
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write('''
    Видно, что с возрастом клиентов становится меньше.
    Возможно, это связанно с определением целевой аудитории для маркетинговой компании.
    Также, количество клиентов женщин достаточно резко падает с увелечением возраста.
    Для мужчин тренд более ровный, с резким уменьшением клиентов после ~55 лет. Медианный
    возраст мужчин (41) на 5 лет больше, чем женщин (36).
    ''')

    st.divider()
    st.subheader('Пол клиентов')

    gender_proportion = (
            clients_extended
            .gender_desc
            .value_counts(normalize=True)
            .to_frame('proportion')
            .assign(proportion=lambda df: df['proportion'] * 100)
            .reset_index()
            .assign(gender='Пол')
)

    fig = (
        px.bar(
            data_frame=gender_proportion,
            x='proportion',
            y='gender',
            color_discrete_sequence=color_sequence,
            template='simple_white',
            color='gender_desc',
            labels={
                'gender_desc':'Пол'
            },
            width=600, 
            height=250
        )
        .update_traces(textposition='auto')
        .update_layout(
            xaxis_title_text = '', 
            yaxis_title_text = '',
            xaxis={
                'visible': False, 
            },
            yaxis={
                'visible': False, 
            },
            hovermode=False,
            uniformtext_minsize=100,
            bargap=0.5
        )
        )

    fig.add_annotation(
        x=35, 
        y=0, 
        text="65.33%",
        showarrow=False,
        font={
            'size':20,
            'color': 'white'
        }
    )

    fig.add_annotation(
        x=83, 
        y=0, 
        text="34.67%",
        showarrow=False,
        font={
            'size':20,
            'color': 'white'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.write('''
    Мужчин в выборке почти в 2 раза больше, чем женщин.  
    Всего в выборке 16000 клинтов, из них 10452 мужчин и 5548 женщин.
    ''')


    st.divider()
    st.subheader('Образование клиентов')

    education_levels = (
        clients_extended
        .groupby('gender_desc')['education']
        .value_counts(normalize=True)
        .to_frame('proportion')
        .reset_index()
        .sort_values('proportion')
        .assign(proportion=lambda df: df['proportion'] * 100)
    )

    fig = (
        px.bar(
            data_frame=education_levels,
            x='proportion',
            y='education',
            color_discrete_sequence=color_sequence,
            template='simple_white',
            text=[f'{prop:.2f}%' for prop in education_levels['proportion']],
            color='gender_desc',
            barmode='group',
            labels={
                'gender_desc': 'Пол'
            }
        )
        .update_traces(textposition='outside')
        .update_layout(
            xaxis_title_text = '', 
            yaxis_title_text = '',
            xaxis={
                'visible': False, 
            },
            legend={
                'yanchor': "bottom",
                'xanchor': "right",
                'y': 0.01,
                # 'x': 0.01
            }
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write('''
    Больше всего клиентов со средним специальным образованием, средним и высшим образованием.
    Распределение уровней образования для мужчин и женщин не отличается.
    Два и более образований и ученая степень есть только у ~1% людей. 
    ''')

    st.divider()
    st.subheader('Семейное положение')

    marital_statuses = (
        (
        clients_extended
        .groupby('gender_desc')['marital_status']
        .value_counts(normalize=True) * 100
        )
        .to_frame('proportion')
        .reset_index()
        .sort_values('proportion')
    )

    fig = (
        px.bar(
            data_frame=marital_statuses,
            x='proportion',
            y='marital_status',
            color_discrete_sequence=color_sequence,
            template='simple_white',
            text=[f'{prop:.2f}%' for prop in marital_statuses['proportion']],
            color='gender_desc',
            barmode='group',
            labels={
                'gender_desc': 'Пол'
            },
            # width=900
        )
        .update_traces(textposition='outside')
        .update_layout(
            xaxis_title_text = '', 
            yaxis_title_text = '',
            xaxis={

            },
            legend={
                'yanchor': "bottom",
                'xanchor': "right",
                'y': 0.01,
                # 'x': 0.01
            },
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write(
    '''
    Больше всего клиентов либо состояли в браке, либо никогда не состояли.  
    У клиентов мужчин наблюдается большее количество разводов и случаев потери партнера, чем у женщин (10% против 5% и 5% против 0.5%, соответсвенно).
    '''
    )

    st.divider()

    st.subheader('Количество детей/иждивенцев')
    genre = st.radio(
        "",
        ['По полу', 'По уровню образования', 'По семейному положению', 'По возрасту']
    )

    def plot_dependants(col, label, use_seq=True):
        color_seq = {'color_discrete_sequence': color_sequence} if use_seq else {}
        fig = (
            px.box(
                data_frame=(
                    clients_extended
                    .rename({
                        'dependants': 'Количество иждивенцев',
                        'child_total': 'Количество детей'
                    },
                    axis=1
                    )
                ),
                y=['Количество иждивенцев', 'Количество детей'],
                color=col,
                template='simple_white',
                labels={
                    col: label,
                },
                **color_seq
            )
            .update_layout(
                xaxis_title_text = '', 
                yaxis_title_text = '',
                legend={
                    # 'yanchor': "bottom",
                    # 'xanchor': "right",
                    'y': 0.99,
                    'x': 0.90
                },
                xaxis = {
                    'tickmode': 'linear',
                    'dtick': 1
                }
            )
        )

        return fig


    if genre == 'По полу':
        st.plotly_chart(plot_dependants('gender_desc', 'Пол'))
    elif genre == 'По уровню образования':
        st.plotly_chart(plot_dependants('education', 'Уровень образования'), use_container_width=True)
    elif genre == 'По семейному положению':
            st.plotly_chart(plot_dependants('marital_status', 'Семейное положение'), use_container_width=True)
    elif genre ==  'По возрасту':
        fig = (
            px.scatter(
                data_frame=(
                    clients_extended
                    .rename({
                        'dependants': 'Количество иждивенцев',
                        'child_total': 'Количество детей'
                    },
                    axis=1
                    )
                ),
                x='age',
                y='Количество детей',
                # color='gender_desc',
                template='simple_white',
                color_discrete_sequence=color_sequence,
                # labels={
                #     'gender_desc': 'Пол',
                # }
            )
            .update_layout(
                xaxis_title_text = 'Возраст', 
                yaxis_title_text = 'Количество детей',
                legend={
                    # 'yanchor': "bottom",
                    # 'xanchor': "right",
                    'y': 0.99,
                    'x': 0.90
                },
                xaxis = {
                    'tickmode': 'linear',
                    'dtick': 5
                }
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        
    
    st.write('''
    Чаще всего у клиента либо нет детей, либо от 1 до 2 детей.
    В данных есть клиенты с 5 и более детьми. У около половины клиентов либо нет иждивенцев,
    либо есть от 1 до 2. Распределения количества детей у мужчин и женщин почти одинаковые.
    Количество детей не зависит от уровня образования, единтсвенный отличие - это медиана в 0 детей у клиентов с неоконченным высшим, у остальных тенденция в 1-2 ребенка сохраняется. 
    Зависимости количества детей от возраста не наблюдается.
    '''
        )

with tab2:
    st.subheader('Распределение персонального заработка')

    fig = (
        px.histogram(
            data_frame=clients_extended,
            x='personal_income',
            template='simple_white',
            color_discrete_sequence=color_sequence,
            marginal='box'
        )
        .update_layout(
            xaxis_title_text = 'Зарлата', 
            yaxis_title_text = '',
            legend={
                # 'yanchor': "bottom",
                # 'xanchor': "right",
                'y': 0.99,
                'x': 0.90
            }
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.write('Медианная зарплата равна 12000. Видно, что есть много выбросов. Распеределение немного скошено влево.')
    st.divider()



    industries = ','.join([word for word in clients_extended.gen_industry.values.tolist() if word == word])
    
    fig, ax = plt.subplots()
    
    wordcloud = WordCloud(background_color='white', colormap='RdBu_r', random_state=1337).generate(industries)

    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.image(wordcloud.to_array(), width=600)
    
    with col2:
        st.subheader('Топ-5 индустрий')

        st.markdown('''
        :department_store: Торговля  
        :office: Металлургия  
        :factory: Промышленность  
        :oncoming_automobile: Машиностроение  
        :briefcase: Государственная служба  
        :mortar_board: Образование  
        :metro: Транспорт  
        :cow2: Сельское хозяйство  
        :building_construction: Строительство  
        :railway_car: Дорожные службы
        ''')

    st.divider()

    employment_proportion = (
        clients_extended
        .employment_status
        .value_counts(normalize=True)
        .to_frame('proportion')
        .assign(proportion=lambda df: df['proportion'] * 100)
        .reset_index()
        .assign(employment='Занятость')
    )

    st.subheader('Пропорция работающих клиентов')

    fig = (
        px.pie(
            data_frame=employment_proportion,
            values='proportion',
            names='employment_status',
            color_discrete_sequence=color_sequence,
            template='simple_white',
            # # color='employment_status',
            # labels={
            #     'employment_status':'Занятость'
            # },
            width=600, 
            height=400,
            hole=0.8
        )
        .update_traces(textposition='auto')
        .update_layout(
            xaxis_title_text = '', 
            yaxis_title_text = '',
            xaxis={
                'visible': False, 
            },
            yaxis={
                'visible': False, 
            },
            hovermode=False,
            uniformtext_minsize=100
        )
    )

    st.plotly_chart(fig)

    st.write('Всего около 10% клиентов не работают.')

    st.divider()

    st.subheader('Семейный доход')


    family_incomes = (
        (
        clients_extended
        .family_income
        .value_counts(normalize=True) * 100
        )
        .to_frame('proportion')
        .reset_index()
        .sort_values('proportion')
    )

    fig = (
        px.bar(
            data_frame=family_incomes,
            x='proportion',
            y='family_income',
            color_discrete_sequence=color_sequence,
            template='simple_white',
            text=[f'{prop:.2f}%' for prop in family_incomes['proportion']],
        )
        .update_traces(textposition='outside')
        .update_layout(
            xaxis_title_text = '', 
            yaxis_title_text = '',
            xaxis={
                'visible': False, 
            },
            legend={
                'yanchor': "bottom",
                'xanchor': "right",
                'y': 0.01,
                # 'x': 0.01
            }
        )
    )

    st.plotly_chart(fig)

    st.write('Большинство семей зарабатывают от 10000 до 50000. Около 10 процентов зарабатывает меньше 10000 рублей. Также есть 3% семей, которые зарабатывают свыше 50000 рублей.')

    st.divider()

    st.subheader('Зависимость дохода от разных факторов')

    def plot_income_factor(col, label):

        fig = (
            px.scatter(
                data_frame=clients_extended,
                x=col,
                y='personal_income',
                # color='gender_desc',
                template='simple_white',
                color_discrete_sequence=color_sequence,
                # labels={
                #     'gender_desc': 'Пол',
                # }
            )
            .update_layout(
                xaxis_title_text = label, 
                yaxis_title_text = 'Зароботная плата',
                legend={
                    # 'yanchor': "bottom",
                    # 'xanchor': "right",
                    'y': 0.99,
                    'x': 0.90
                }
            )
        )

        return fig

    option = st.selectbox(
    'С какой переменной?',
    ('Возраст', 'Количество детей', 'Количество иждивенцев', 'Количество месяцев на одном месте'))

    options = dict(
        age='Возраст',
        child_total='Количество детей',
        dependants='Количество иждивенцев',
        work_time="Количество месяцев на одном месте"
    )

    options_reversed = {name:col for col, name in options.items()}


    st.plotly_chart(plot_income_factor(options_reversed[option], option))


    with tab3:

        st.subheader('Процент откликов на маркетинговую компанию')

        target_proportion = (
        clients_extended
        .target
        .map({1:'Есть отклик', 0: 'Нет отклика'})
        .value_counts(normalize=True)
        .to_frame('proportion')
        .assign(proportion=lambda df: df['proportion'] * 100)
        .reset_index()
    )


        fig = (
            px.pie(
                data_frame=target_proportion,
                values='proportion',
                names='target',
                color_discrete_sequence=color_sequence,
                template='simple_white',
                # # color='employment_status',
                width=600, 
                height=400,
                hole=0.8
            )
            .update_traces(textposition='auto')
            .update_layout(
                xaxis_title_text = '', 
                yaxis_title_text = '',
                xaxis={
                    'visible': False, 
                },
                yaxis={
                    'visible': False, 
                },
                hovermode=False,
                uniformtext_minsize=100
            )
        )

        st.plotly_chart(fig)

        st.write('Только около 10% пользователей откликуются на нашу маркетинговую компанию, что может показывать о ее неэффективность.')

        st.divider()

        st.subheader('Пропорция откликов')

        option = st.selectbox(
        'Имя переменной?',
        ('Возраст', 'Количество детей', 'Количество иждивенцев', 'Количество месяцев на одном месте')
        )

        target_feat = (
            clients_extended
            .groupby('target')[options_reversed[option]]
            .value_counts(normalize=True)
            .sort_index()
            .to_frame('proportion')
            .reset_index()
            .pivot(index=options_reversed[option], columns='target', values='proportion')
        )

        target_feat.columns = ['Нет отклика', 'Есть отклик']

        st.write(target_feat)



