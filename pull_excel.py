import pandas as pd
import xlrd


def loadPandasDf():
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
    return df


def move(index, name):
    newColRef = df[name]
    df.drop(labels=name, axis=1, inplace=True)
    df.insert(index, name, newColRef)


display(pd.read_pickle('./class_data'))

df = pd.read_pickle('./class_data')


df.to_csv('./class_data.csv', sep='>', header=df.keys().tolist())

df = pd.read_csv('./class_data.csv', sep='>')
del df['Unnamed: 0']
df


def cleanClassData():
    del df['Year']
    df = df.rename(index=str, columns={"date2": "Term"})
    move(12,'Term')

    df = df.rename(index=str, columns={"days": "Days"})
    move(5,'Days')

    df = df.rename(index=str, columns={"q_guide2": "Q Guide"})
    move(9,'Q Guide')

    df = df.rename(index=str, columns={"Unnamed: 7": "Acha's Rating"})
    df = df.rename(index=str, columns={"Unnamed: 12": "Notes 1"})
    df = df.rename(index=str, columns={"Unnamed: 13": "Notes 2"})

    move(18, 'Notes 1')
    move(18, 'Notes 2')

    df = df.rename(index=str, columns={"googleMaps": "Google Maps"})
    df = df.rename(index=str, columns={'location': 'Location'})
    df = df.rename(index=str, columns={'description': 'Description'})

    df['Notes'] = df['Notes 1'].map(str) + " " + df['Notes 2'].map(str)
    del df['Notes 1']
    del df['Notes 2']
    df['Notes'] = df['Notes'].map(lambda x: x.lstrip('nan').rstrip('nan'))

    df.to_pickle('./class_data')
