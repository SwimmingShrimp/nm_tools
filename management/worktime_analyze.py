import pandas as pd
from datetime import datetime

excel_file = "/home/ubuntu/Downloads/2024_1_2.csv"
df = pd.read_csv(excel_file)
df = df[df['end'] != '-']

df['start'] = pd.to_datetime(df['start'].astype(str),format='%H:%M')
df['end'] = pd.to_datetime(df['end'].astype(str),format='%H:%M')

df['time_diff'] = df['end'] - df['start']

df['avg'] = df.groupby('name')['time_diff'].transform('mean')
df2 = df.drop_duplicates(subset=['name','avg'], keep='first')
df2 = df2[['name','avg']]
df2.to_csv('/home/ubuntu/Downloads/2024_1_2_worktime.csv',index=False)