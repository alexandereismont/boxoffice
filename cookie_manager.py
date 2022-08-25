

import extra_streamlit_components as stx
import streamlit as st

@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()