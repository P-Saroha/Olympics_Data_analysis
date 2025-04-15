import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px

df = preprocessor.preprocessor()

st.sidebar.header('Olympics Analysis')

list = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally","Overall Analysis","Country wise Analysis","Athletes wise Analysis") 
)

# st.dataframe(df)

if list == 'Medal Tally':
    st.sidebar.header("Medal Tally") 
    years,country = helper.country_years(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)


    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'overall' and selected_country == 'overall':
        st.title('OverAll Tally')
    
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country + " Overall Performance")

    if selected_year != 'overall' and selected_country == 'overall':
        st.title('Medal Tally in ' + str(selected_year)+ " Olympics")

    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympic")

    st.dataframe(medal_tally)


if list == "Overall Analysis":
    editions = df['Year'].nunique() - 1
    city = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes_name = df['Name'].nunique()
    nations = df['region'].nunique()


    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Total Olympics Held (Till 2016)")
        st.title(editions)

    with col2:
        st.header("Host Cities")
        st.title(city)

    with col3:
        st.header("Different Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Unique Events")
        st.title(events)

    with col2:
        st.header("Participating Athletes")
        st.title(athletes_name)

    with col3:
        st.header("Participating Countries")
        st.title(nations)

    nation_over_time = helper.data_over_time(df,'region')
    st.title("Number of Participating Country over years in Olympics")
    fig = px.line(nation_over_time, x= 'Edition', y = 'region')
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df,'Event')
    st.title("Events over years in Olympics")
    fig = px.line(event_over_time, x= 'Edition', y = 'Event')
    st.plotly_chart(fig)

    Athletes_over_time = helper.data_over_time(df,'Name')
    st.title("Number of Athletes over years in Olympics")
    fig = px.line(Athletes_over_time, x= 'Edition', y = 'Name')
    st.plotly_chart(fig)

