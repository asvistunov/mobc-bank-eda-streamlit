import pandas as pd

employment_status = pd.read_csv('datasets/D_work.csv')
retirement_status = pd.read_csv('datasets/D_pens.csv')
clients = pd.read_csv('datasets/D_clients.csv')
target = pd.read_csv('datasets/D_target.csv')
jobs_description = pd.read_csv('datasets/D_job.csv')
salary = pd.read_csv('datasets/D_salary.csv').drop_duplicates(inplace=False)
credit = pd.read_csv('datasets/D_last_credit.csv')
loan_status = pd.read_csv('datasets/D_loan.csv').merge(pd.read_csv('datasets/D_close_loan.csv'), on='ID_LOAN', validate='one_to_one')

clients_extended = (
    clients
    .merge(salary, left_on='ID', right_on='ID_CLIENT', validate='one_to_one', how='left')
    .drop('ID_CLIENT', axis=1)
    .merge(jobs_description, left_on='ID', right_on='ID_CLIENT', validate='one_to_one', how='left')
    .drop('ID_CLIENT', axis=1)
    .merge(target, left_on='ID', right_on='ID_CLIENT', validate='one_to_one', how='left')
    .drop('ID_CLIENT', axis=1)
    # .merge(credit, left_on='ID', right_on='ID_CLIENT', how='left')
    # .merge(loan_status, left_on='ID', right_on='ID_CLIENT', how='left')
    # .drop('ID_CLIENT', axis=1)
)


clients_loans = (
    clients_extended
    .merge(credit, left_on='ID', right_on='ID_CLIENT', how='left')
    .drop('ID_CLIENT', axis=1)
    .merge(loan_status, left_on='ID', right_on='ID_CLIENT', how='left')
    .drop('ID_CLIENT', axis=1)
)

clients_extended.columns = [col_name.lower() for col_name in clients_extended.columns]


clients_extended['gender_desc'] = clients_extended['gender'].map({1:'Мужчина', 0:'Женщина'})
clients_extended['employment_status'] = clients_extended['socstatus_work_fl'].map({1:'Работает', 0:'Не работает'})
clients_extended['retirement_status'] = clients_extended['socstatus_pens_fl'].map({1:'Пенсионер', 0:'Не пенсионер'})
clients_extended['retirement_status'] = clients_extended['fl_presence_fl'].map({1:'Есть квартира', 0:'Нет квартиры'})