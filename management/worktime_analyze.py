import pandas as pd
from datetime import datetime

excel_file = "/home/ubuntu/Downloads/2024_1_2.xlsx"
df = pd.read_excel(excel_file)
df = df[df['start'] != '-']
df = df[df['end'] != '-']
df['start'] = pd.to_datetime(df['start'].astype(str),format='%H:%M')
df['end'] = pd.to_datetime(df['end'].astype(str),format='%H:%M')
df['start_h'] = df['start'].dt.hour
df['end_h'] = df['end'].dt.hour
df['start_m'] = df['start'].dt.minute
df['end_m'] = df['end'].dt.minute
df['time_diff_hour'] = df['end_h'] - df['start_h']
df['time_diff_min'] = df['end_m'] - df['start_m']
df['time_diff'] = df['time_diff_hour'] + (df['time_diff_min']/60) -1

df['avg'] = df.groupby('name')['time_diff'].transform('mean')
df2 = df.drop_duplicates(subset=['name','avg'], keep='first')
df2 = df2[['name','avg']]
df2.to_csv('/home/ubuntu/Downloads/2024_1_2_worktime.csv',index=False)