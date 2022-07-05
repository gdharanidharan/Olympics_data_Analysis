from pydoc import Helper
import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import warnings
warnings.filterwarnings('ignore')


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df) # calling preprocess function in preprocessor.py and saving the result in df

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

# MEDAL TALLY MODULE

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    medal_tally.rename(columns={'region':'Country',
                       'total':'Total'},inplace=True)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally in Olympics')
    
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + 'Olympics')

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of ' + (selected_country) + ' in Olympics')

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of ' + (selected_country) +' in '+str(selected_year) +' Olympics')   

    st.table(medal_tally)


# OVERALL ANALYSIS MODULE

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('TOP STATISTICS')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.title('Editions')
        st.title(editions)
    with col2:
        st.title('Hosts')
        st.title(cities)
    with col3:
        st.title('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.title('Events')
        st.title(editions)
    with col2:
        st.title('Athletes')
        st.title(athletes)
    with col3:
        st.title('Nations')
        st.title(nations)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(data_frame=nations_over_time, x='Edition', y='region',
                  labels={
                     'region': 'No of Countries'})
    st.title('Participating Nations Over the Years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(data_frame=events_over_time, x='Edition', y='Event',
                  labels={
                     'Event': 'No of Events'})
    st.title('Events Over the Years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(data_frame=athletes_over_time, x='Edition', y='Name',
                  labels={
                     'Name': 'No of Athletes'})
    st.title('Athletes Over the Years')
    st.plotly_chart(fig)

    st.title('No of Events Over time(Every Sports)')
    fig, ax = plt.subplots(figsize=(15,15))
    x  = df.drop_duplicates(['Year','Sport','Event'])
    pivot = x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(pivot.fillna(0).astype('int'),annot=True, cmap='Blues', linewidths=2, linecolor='yellow', cbar=False)
    st.pyplot(fig)

    st.title('Most Successful Athletes')

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
        
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)

    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal",
                  labels={'Medal': 'Medals'})
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    pivot = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pivot,annot=True, cmap='Blues', linewidths=2, linecolor='yellow', cbar=False)
    st.title(selected_country + " Excels in the Following Sports")
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna() # All Age dist
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna() # Age dist of Gold Medal
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna() # Age dist of Silver Medal
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna() # Age dist of Bronze Medal
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=700,height=500)
    st.title('Age Distribution of Atheletes' )
    fig.update_layout(autosize=False, width=700, height=500,
                      xaxis_title="Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=700,height=500)
    st.title('Age Distribution of Atheletes With Respect to Sports (Gold Medalist)')
    fig.update_layout(autosize=False, width=700, height=500,
                      xaxis_title="Age")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Athletes Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=700, height=500,
                      xaxis_title="Edition",
                      yaxis_title="No of Participants")
    st.plotly_chart(fig)


    







