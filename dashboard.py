# Import necessary libraries and set streamlit webpage name
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Health Dashboard", layout="wide")

# Display the title of the dashboard on the screen, along with its objective
st.title("*Cardiac Disease Dashboard*", width="stretch", text_alignment="center")
st.subheader("_An important *:red[analysis on heart failure diseases]* and its complications_ :heart:",text_alignment="center")


def load_data(filepath):
    """Function that loads the data with error validation"""
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


def clean_data(df):
    """Function responsible for cleaning the data"""
    df = df.drop_duplicates()
    df = df[df['Cholesterol']>0]
    df = df[df['RestingBP']>0]
    df = df[df['Age'].between(20,100)]
    return df

def show_metrics(df): 
    """Function responsible for showing important values on the screen"""
    col1, col2, col3 = st.columns(3)
    col4,col5,col6 = st.columns(3)
    col1.metric("Total Patients", f":busts_in_silhouette: {len(df)}", border = True)
    col2.metric("Average Age", round(df['Age'].mean(), 1), border = True)
    col3.metric("Heart Disease (%)", f"🫀 {round(df['HeartDisease'].mean() * 100, 1)}%", border = True)

    male_heart_disease = round(df[df['Sex'] == 'M']['HeartDisease'].mean() * 100, 1)
    female_heart_disease = round(df[df['Sex'] == 'F']['HeartDisease'].mean() * 100, 1)
    if male_heart_disease > female_heart_disease:
        col4.metric("Most Affected Sex", f":man: Male: {male_heart_disease}", border = True)
    else:
        col4.metric("Most Affected Sex", f":woman: Female: {female_heart_disease}", border = True)

    col5.metric("Resting Blood Pressure", f"🩸 {round(df['RestingBP'].mean(), 1)}" , border = True)
    col6.metric("Cholesterol", f"🧪 {round(df['Cholesterol'].mean(), 1)}", border = True)  
    st.divider()


def sidebar_filters(df):
    """Function responsible for creating a sidebar in order to change values"""
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
    """Function to plot the age distribuition in the data"""
    st.subheader("_Age distribution_")
    fig = px.histogram(df, x = 'Age', 
                       nbins = 20,
                       color = 'Heart Disease',
                       color_discrete_map = {'No': '#2ecc71', 'Yes': '#e74c3c'},
                       labels = {'HeartDisease': 'Heart Disease'},
                       barmode = 'overlay',
                       opacity = 0.7)
    st.plotly_chart(fig, width="stretch")
    st.caption("Patients without heart disease are more concentrated between ages 40–55, while patients with heart disease are more prevalent from age 55 onwards. This confirms the well-known relationship between aging and increased cardiovascular risk.")
    st.divider()

def plot_heart_disease_by_sex(df):
    """Function to plot the heart disease by sex for patients with and without heart disease"""
    st.subheader("_Heart Disease by Sex_")
    fig = px.histogram(df, x = 'Sex',
                       color = 'Heart Disease',
                       color_discrete_map = {'No': '#2ecc71', 'Yes': '#e74c3c'},
                       barmode = 'group')
    st.plotly_chart(fig, width="stretch")
    st.caption("The dataset is heavily male-dominated. Among females, the vast majority do not have heart disease. Among males, heart disease is slightly more prevalent than its absence, suggesting higher cardiovascular risk in men within this population.")
    st.divider()

def plot_cholesterol(df):
    """Function to plot the cholesterol data for patients with and without heart disease"""
    st.subheader("_Cholesterol by Heart Disease_")
    fig = px.box(df, x = 'Heart Disease', y ='Cholesterol',
                 color = 'Heart Disease',
                 color_discrete_map = {'No': '#2ecc71', 'Yes': '#e74c3c'})
    st.plotly_chart(fig, width="stretch")
    st.caption("Both groups show similar cholesterol distributions centered around 200–250 mg/dL, with no clear separation between patients with and without heart disease. This suggests that cholesterol alone is not a strong differentiator in this dataset.")
    st.divider()

def plot_heart_rate(df):
    """Function to plot the maximum heart rate by age for patients with and without heart disease"""
    st.subheader("_Max Heart Rate by Age_")
    fig = px.scatter(df, x='Age', y = 'MaxHR',
                     color = 'Heart Disease',
                     color_discrete_map = {'No': '#2ecc71', 'Yes': '#e74c3c'},
                     opacity = 0.7)
    st.plotly_chart(fig, width="stretch")
    st.caption("Patients without heart disease tend to achieve higher maximum heart rates (140–180 bpm), while patients with heart disease are concentrated in lower ranges (100–140 bpm). This is consistent with chronotropic incompetence, a known clinical indicator of cardiac dysfunction.")
    st.divider()

def plot_correlation_heatmap(df):
    """Function to plot a correlation heatmap to see if there is any correlation between variables"""
    st.subheader("_Correlation Heatmap_")
    numeric_df = df.select_dtypes(include=['number'])
    corr = numeric_df.corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r',
                    zmin= -1, zmax = 1)
    st.plotly_chart(fig, width="stretch") 
    st.caption("MaxHR shows the strongest negative correlation with HeartDisease — higher maximum heart rates are associated with lower cardiac disease risk. Age shows a positive correlation, confirming that older patients are at higher risk.")

def show_statistics(df):
    """Function to show the basic statistics of the data"""
    st.subheader("Basic statistics")
    stats = df[['Age', 'RestingBP', 'Cholesterol', 'MaxHR']].describe().round(1)
    st.dataframe(stats, width='stretch')
    st.divider()


df = load_data('heart_failure_data.csv')
if df is None:
    st.error("Could not load data")
    st.stop()
df = clean_data(df)
df['Heart Disease'] = df['HeartDisease'].map({0: 'No', 1: 'Yes'})
show_metrics(df)
df_filtered = sidebar_filters(df)
show_statistics(df_filtered)
plot_age_distribuition(df_filtered)
plot_heart_disease_by_sex(df_filtered)
plot_cholesterol(df_filtered)
plot_heart_rate(df_filtered)
plot_correlation_heatmap(df_filtered)

st.divider()
st.caption("Data source: Kaggle Heart Failure Prediction Dataset | For educational purposes only.")