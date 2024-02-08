import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize session state for page navigation if not already set
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'

# Define navigation function
def navigate(page):
    st.session_state['current_page'] = page

# Display content based on current_page
file = st.file_uploader('Upload your csv file here')
if file is not None:
    data = pd.read_csv(file)
    df = pd.DataFrame(data)
    if (st.session_state['current_page'] == 'Home') or (st.session_state['current_page'] == 'Home1'):
        st.write("file",file)
        st.button('Data Description >', on_click=navigate, args=('Data Description',))

    # Data Description page
    if st.session_state['current_page'] == 'Data Description':
        st.title("Data Description")
        st.write(df.describe(include = 'all'))
        st.title("Data Header")
        st.write(df.head())
        st.button('Features Analysis >', on_click=navigate, args=('Features Analysis',))

    # Feature Analysis page
    elif st.session_state['current_page'] == 'Features Analysis':
        # Identifying numerical columns
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
        # Identifying categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        # Calculating missing values
        missing_val = df.isnull().sum()

        st.title("Data Shape")
        shape=df.shape
        st.write("Number of rows : ",shape[0])
        st.write("Number of columns : ",shape[1])
        st.title("Numerical Columns")
        st.write("Number of numerical columns : ",len(numerical_cols))
        st.write(numerical_cols)
        st.title("Categorical Columns")
        st.write("Number of categorical columns : ",len(categorical_cols))
        st.write(categorical_cols)
        st.title("Missing Values")
        st.write("Number of missing values in data :")
        st.write(missing_val[missing_val > 0])
        st.button('Data Statistics >', on_click=navigate, args=('Data Statistics',))

    # Data Statistics page
    elif st.session_state['current_page'] == 'Data Statistics':
        # Identifying numerical columns
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
        # Identifying categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns

        st.title('Histograms for Numerical Features')
        if len(numerical_cols)>0:
            for column in numerical_cols:
                if column != 'Unnamed: 0':
                    plt.figure()
                    df[column].hist(bins=20)
                    plt.title(f'Histogram of {column}')
                    plt.xlabel(column)
                    plt.ylabel('Frequency')
                    st.pyplot(plt)

        if len(categorical_cols)>0:
            st.title('Bar Charts for Categorical Features')
            for column in categorical_cols:
                plt.figure(figsize=(10, 6))
                sns.countplot(x=column, data=df)
                plt.title(f'Frequency of Categories in {column}')
                plt.xticks(rotation=45)
                st.pyplot(plt)
        st.button('Upload Another File >', on_click=navigate, args=('Home',))
            