import pandas as pd

df=pd.read_csv("C:\\Users\\范春\Desktop\测试1.csv",header=0)

means=df.mean()
print(df)
df.fillna(means,inplace=True)
print(df)