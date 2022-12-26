import streamlit as st
import pandas as pd
import plotly.express as px

# source: https://www.youtube.com/watch?v=__Zelpz4Ihw&t=725s


def addtional_bedroom_oppertunity(x):
    """
    Possible add in a bedroom
    2bd >= 1300 
    3bd >= 1950 
    4bd >= 2600
    """
    try:
        # possible add in a bedroom
        # 2bd >= 1300 
        # 3bd >= 1950 
        # 4bd >= 2600
        if (x['ratio_sqft_bd'] >= 650) and (x['ratio_sqft_bd'] is not None) and (x['BEDS'] > 1) and (x['PROPERTY TYPE'] == 'Single Family Residential'):
            return True
        else:
            return False
    except:
        return False


def adu_potential(x):
    """
    Addtional Unit Potential 
    """
    try:
        if (x['ratio_lot_sqft'] >= 5) and (x['ratio_lot_sqft'] is not None) and (x['HOA/MONTH'] and (x['PROPERTY TYPE'] == 'Single Family Residential')):
            return True
        else:
            return False
    except:
        return False


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8') 

def upload_redfin():
    """
    download redfin.com housing data
    """
    uploaded_file = st.file_uploader("Upload a CSV file: ", help='Go to redfin.com to get the house price', type=['csv'])
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        return dataframe

def my_metric(dataframe):
    """
    Display few housing metrics
    Total properties in search
    ...
    ...
    """
    # metirics
    st.markdown('## Metrics')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', len(dataframe), help='The total properties in search')
    with col2:
        st.metric('Avg. Price', "${:,}".format(dataframe['PRICE'].mean()).split(',')[0]+'K', help='Average sale price of properties in search')
    with col3:
        st.metric('Avg. DoM', int(dataframe['DAYS ON MARKET'].mean()), help='Average dyas on market of properties in search')
    with col4:
        st.metric('Avg. PPSQFT', "${:,}".format(int(dataframe['$/SQUARE FEET'].mean())), help='Average $/FT2')


def my_charts(dataframe):
    # charts
    st.markdown('## Data Visualization')
    with st.expander('Charts', expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            fig = px.histogram(dataframe, x='DAYS ON MARKET', nbins=30, title='Days on Market')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(dataframe, x='PRICE', title='Price Box')
            st.plotly_chart(fig, use_container_width=True)
        with col3:
            fig = px.histogram(dataframe, x='$/SQUARE FEET', title='Price per SQFT')
            st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        # map
        st.markdown('## Map')
        st.map(dataframe)

    with col2:
        pass
        

def my_features(dataframe):
    # features
    df_features = dataframe.copy()
    df_features['ratio_sqft_bd'] = df_features['SQUARE FEET'] / df_features['BEDS']
    df_features['addtional_bd_opp'] = df_features.apply(lambda x: addtional_bedroom_oppertunity(x), axis=1)
    df_features['ratio_lot_sqft'] = df_features['LOT SIZE'] / df_features['SQUARE FEET']
    df_features['adu_potential'] = df_features.apply(lambda x: adu_potential(x), axis=1)

    # tables
    with st.expander('Oppertunies', expanded=True):
        st.markdown('## Oppertunities')
        df_add_bd = df_features.loc[df_features['addtional_bd_opp'] == True]
        df_adu = df_features.loc[df_features['adu_potential'] == True]

        col1, col2 =st.columns(2)
        with col1:
            st.metric('Total Add Bd', len(df_add_bd), help='Number of properties with addtional bedroom oppertunity')
        with col2:
            st.metric('Total ADU', len(df_adu), help='Number of porperties with accessory dwelling unit potential')

        st.dataframe(df_features)

    csv = convert_df(df_features)

    st.download_button('Download', csv, "file.csv", "text/csv", key='download-csv')


st.set_page_config(page_title='My First App', layout='wide', page_icon=':smiley')
st.title('Housing Data Analysis')
with st.expander('Glossary', expanded=False):
    st.markdown('## an alphabetical list of terms or words found in or relating to a specific subject, text, or dialect, with explanations; a brief dictionary.')
df= upload_redfin()
if df is not None:
    my_metric(df)
    my_charts(df)
    my_features(df)


