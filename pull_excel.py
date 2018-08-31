import pandas as pd
import xlrd


df = pd.read_excel('/Users/sidharthmenon/Desktop/Summer 2018/Harvard Class List.xlsx', header=9)
df = df.rename(index=str, columns={"Full Title ": "Full Title"})
df = df.rename(index=str, columns={"Interesting Classes ": "Interesting Classes"})
df = df.rename(index=str, columns={"Divisional Distribution ": "Divisional Distribution"})
df[['Title', 'Sep', 'Course #']] = df['Full Title'].str.rpartition(" (",  expand=True)
del df['Full Title']
del df['Sep']
newColRef = df['Title']
df.drop(labels='Title', axis=1, inplace=True)
df.insert(1, 'Title', newColRef)
newColRef = df['Course #']
df.drop(labels='Course #', axis=1, inplace=True)
df.insert(2, 'Course #', newColRef)
clean = lambda s: (s.replace(')', '')).replace(' ', '')
df['Course #'] = df['Course #'].apply(clean)
display(df)

def loadPandasDf():
    return df
