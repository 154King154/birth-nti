import pandas as pd
import datetime as dt

db_pnti = pd.read_csv(r'PNTI.csv', delimiter=";")
db_unti = pd.read_csv(r'UNTI.csv', delimiter=";")
db = db_pnti.append(db_unti).reset_index()

db["Дата рождения"] = pd.to_datetime(db["Дата рождения"], format="%d.%m.%Y")

db['day'] = db['Дата рождения'].dt.day
db['month'] = db['Дата рождения'].dt.month

db = db.drop_duplicates(keep="first", ignore_index=True, subset=["Сотрудник"]).reset_index()

db.to_csv("db_nti.csv")
