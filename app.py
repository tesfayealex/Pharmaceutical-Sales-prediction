from multiapp import MultiApp
import streamlit as st
import sys
from dashboard import EDA
sys.path.insert(0, './scripts')

# import your app modules here

st.set_page_config(page_title="TellCo Telecom Analytics", layout="wide")

app = MultiApp()


st.sidebar.markdown("""
# 
### Multi-Page App
This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).
### Modifications
\t- Page Folder Based Access
\t- Presentation changed to SideBar
""")

# Add all your application here
# app.add_app("Predict Satisfaction", model_implementation.app)
app.add_app("EDA", EDA.app)
# The main app
app.run()
