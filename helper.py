import numpy as np


def fetch_medal_tally(df, year, country):
    
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    flag = 0   
        
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1 # This is for to display all years data when user choose 'Overall' year
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year] 
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]
        
    if flag == 1:  
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year', ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending=False).reset_index()
        
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    x.index += 1 # Index starts from 1
    
    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    medal_tally.index += 1 # Index starts from 1

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def data_over_time(df, col):
        events_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')
        events_over_time.rename(columns={'index': 'Edition','Year': col}, inplace=True)
        return events_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal']) # Dropping NaN from Medal column
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        
    x = temp_df['Name'].value_counts().reset_index().head(20).merge(df, left_on='index', right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index').reset_index(drop=True)
    x. rename(columns={'index':'Name',
                      'Name_x': 'Medal',
                      'region' :'Country'}, inplace=True)
    x.index += 1
    return x

def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pivot = new_df.pivot_table(index = 'Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')
    return pivot

def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal']) # Dropping NaN from Medal column
    
    temp_df = temp_df[temp_df['region'] == country]
        
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates('index').reset_index(drop=True)
    x. rename(columns={'index':'Name',
                      'Name_x': 'Medal'}, inplace=True)
    x.index += 1
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.columns = ['Year','Male','Female']
    final.fillna(0, inplace=True)

    return final

