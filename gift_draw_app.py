import pandas as pd
import streamlit as st

st.title(":gift: Hediye Çekiliş Uygulaması") 

# "st.session_state object:", st.session_state

if "df_result" not in st.session_state:
    st.session_state['df_result'] = pd.DataFrame(columns=['name','email'])


# st.write(st.session_state)

name = st.text_input('Enter your name:')
email = st.text_input('Enter your email address:')

def onAddRow():
    data = {
            'name':name,
            'email':email  
        }
    st.session_state['df_result'] = st.session_state['df_result'].append(data, ignore_index=True)

st.button("Add row", on_click = onAddRow)

@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')
st.download_button(
    "Press to Download",
    convert_df(st.session_state.df_result),
    "file.csv",
    "text/csv",
    key='download-csv'
)
st.dataframe(st.session_state['df_result'])