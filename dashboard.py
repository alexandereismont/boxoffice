#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 09:20:16 2022

@author: Alexander E.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime
from menu import menu

from util import runtime_to_minutes

st.set_page_config(layout="wide")

def prepare_diff(df):
    df_diff = df.copy()
    return df_diff

@st.cache()
def load_data():
    df = pd.read_csv('./data/Mojo_budget_data.csv')
    df['profit_ratio'] = df['worldwide'] / df['budget']
    df = df.drop(columns=(['link', 'movie_id']))
    df['worldwide'] = df['worldwide']/1000000
    df['domestic'] = df['domestic']/1000000
    df['budget'] = df['budget']/1000000
    df['international'] = df['international']/1000000
    df['runtime_minutes'] = df['run_time'].apply(lambda x: runtime_to_minutes(x))
    df_diff = prepare_diff(df)
    return df, df_diff

df, df_diff = load_data()
df_melt = df.melt('movie_year', var_name='name', value_name='value', value_vars=['worldwide', 'domestic', 'international'])
max_year = df_diff['movie_year'].max()

#median = df_diff[df_diff['movie_year'] == max_year].median()

#numeric_colums = np.array((df_diff.dtypes == 'float64') | (df_diff.dtypes == 'int64'))

# df_diff.iloc[:, numeric_colums] = (df_diff.iloc[:, numeric_colums] - median).div(median)

menu(df=df)