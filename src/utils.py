# clean up membership table
import pandas as pd

def clean_members_table(df = pd.DataFrame()):
    if df.empty:
        df = pd.read_csv("data/bike_root_memberships.csv",dtype={'Student Number':'str'})
    if "Timestamp" in df.columns: 
        df.rename(columns = {"Timestamp":"Member Since"},inplace=True)
    df['Postal Code'] = df['Postal Code'].str.replace('\W','',regex=True).str.upper()
    df['Member Since']= pd.to_datetime(df['Member Since']).dt.date
    df['Phone Number'] = df['Phone Number'].str.replace('\W','',regex=True)

    return df

def member_search(df,name=None):
    info = df[df['First and Last Name'].str.lower().str.contains(name)]
    if info.empty:
        return None
    elif info.shape[0] > 1:
        return None
    else:
        return info.iloc[0,:3]

def member_stats(df,normalize = True):
    return df['Relation to the University of Calgary'].value_counts(normalize)
