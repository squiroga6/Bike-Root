# clean up membership table

import pandas as pd

def clean_members_table(df = pd.DataFrame()):
    if df.empty:
        df = pd.read_csv("data/memberships.csv",dtype={'Student Number':'str'})
    df['Timestamp']= pd.to_datetime(df['Timestamp'])
    df['Postal Code'] = df['Postal Code'].str.replace('\W','',regex=True).str.upper()
    df['Phone Number'] = df['Phone Number'].str.replace('\W','',regex=True)

    return df