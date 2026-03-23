import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Health Dashboard", layout="wide")

st.title("*Cardiac Disease Dashboard*", width="stretch", text_alignment="center")
st.subheader("_An important *:red[analysis on heart failure diseases]* and its complications_ :heart:",text_alignment="center")

def load_data(filepath):
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        return None


def clean_data(df):
    df = df.drop_duplicates()
    df = df[df['Cholesterol']>0]
    df = df[df['RestingBP']>0]
    df = df[df['Age'].between(20,100)]
    return df

def show_metrics(df): 
    col1, col2, col3,col4 = st.columns(4)
    col1.metric("Total Patients", f":busts_in_silhouette: {len(df)}", border = True)
    col2.metric("Average Age", round(df['Age'].mean(), 1), border = True)
    col3.metric("Heart Disease (%)", f":heart: {round(df['HeartDisease'].mean() * 100, 1)}%", border = True)
    male_heart_disease = round(df[df['Sex'] == 'M']['HeartDisease'].mean() * 100, 1)
    female_heart_disease = round(df[df['Sex'] == 'F']['HeartDisease'].mean() * 100, 1)
    if male_heart_disease > female_heart_disease:
        col4.metric("Most Affected Sex", f":man: Male: {male_heart_disease}", border = True)
    else:
        col4.metric("Most Affected Sex", f":woman: Female: {female_heart_disease}", border = True)
    st.divider()
def sidebar_filters(df):
    st.sidebar.header("Filters")
    sex = st.sidebar.multiselect("Sex", options = df["Sex"].unique(), default = df['Sex'].unique())
    age_range = st.sidebar.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))
    heart_disease = st.sidebar.multiselect("Heart Disease", options = [0,1], default = [0,1], format_func = lambda x: "Yes" if x==1 else "No")

    df_filtered = df[
        (df['Sex'].isin(sex) &
         df['Age'].between(age_range[0], age_range[1]) &
         df['HeartDisease'].isin(heart_disease))
    ]
    return df_filtered

def plot_age_distribuition(df):
    df = df.copy()
    df['Heart Disease'] = df['HeartDisease'].map({0: 'No', 1: 'Yes'})
    st.subheader("Age distribution")
    fig = px.histogram(df, x = 'Age', 
                       nbins = 20,
                       color = 'Heart Disease',
                       color_discrete_map = {'No': '#2ecc71', 'Yes': '#e74c3c'},
                       labels = {'HeartDisease': 'Heart Disease'},
                       barmode = 'overlay',
                       opacity = 0.7)
    st.plotly_chart(fig, use_container_width = True)
    st.divider()

def plot_heart_disease_by_sex(df):
    st.subheader("Heart Disease by Sex")
    fig = px.histogram(df, x = 'Sex',
                       color = 'Heart Disease',
                       color_discrete_map = {'No': '#2ecc71', 'Yes': '#e74c3c'},
                       barmode = 'group')
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

def plot_cholesterol(df):
    st.subheader("Cholesterol by Heart Disease")
    fig = px.box(df, x = 'Heart Disease', y ='Cholesterol',
                 color = 'Heart Disease',
                 color_discrete_map = {'No': '#2ecc71', 'Yes': '#e74c3c'})
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

def plot_heart_rate(df):
    st.subheader("Max Heart Rate by Age")
    fig = px.scatter(df, x='Age', y = 'MaxHR',
                     color = 'Heart Disease',
                     color_discrete_map = {'No': '#2ecc71', 'Yes': '#e74c3c'},
                     opacity = 0.7)
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

def plot_correlation_heatmap(df):
    st.subheader("Correlation Heatmap")
    numeric_df = df.select_dtypes(include=['number'])
    corr = numeric_df.corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r',
                    zmin= -1, zmax = 1)
    st. plotly_chart(fig,use_container_width=True) 


df = load_data('heart_failure_data.csv')
if df is None:
    st.error("Could not load data")
    st.stop()
df = clean_data(df)
df['Heart Disease'] = df['HeartDisease'].map({0: 'No', 1: 'Yes'})
show_metrics(df)
df_filtered = sidebar_filters(df)
plot_age_distribuition(df_filtered)
plot_heart_disease_by_sex(df_filtered)
plot_cholesterol(df_filtered)
plot_heart_rate(df_filtered)
plot_correlation_heatmap(df_filtered)