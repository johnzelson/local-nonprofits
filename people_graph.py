
# py -m pip install graphviz
# py -m pip install streamlit-d3graph
# py -m pip install scikit-learn

import streamlit as st
import pandas as pd
import folium  
from streamlit_folium import st_folium
import geopandas as gpd
import math
from folium.features import DivIcon  #TODO: move import

import csv
import re
import math
from datetime import datetime
import urllib.parse

import graphviz
from streamlit_d3graph import d3graph
from d3graph import d3graph, vec2adjmat

APP_TITLE = 'Graph People and Connections in Local Nonprofits'
APP_SUB_TITLE = 'Source:  IRS Tax Returns and IRS BMF '

@st.cache_data
def get_people_df():

    all_people_df = pd.read_csv('data/all_people.csv')
    return all_people_df

def build_people_graph(all_people_df):
    p_graph = graphviz.Digraph()
    for index, row in all_people_df.iterrows():
        p_graph.edge(row['NAME'], row['PersonNm'])    
        #st.write (row['NAME'], row['PersonNm'])

    st.graphviz_chart(p_graph)


def quick_gv():

    # Create a graphlib graph object
    gv_graph = graphviz.Digraph()
    gv_graph.edge("org1", "name1")
    gv_graph.edge("org1", "name2")
    gv_graph.edge("org1", "name3")
    gv_graph.edge("org1", "name4")

    st.graphviz_chart(gv_graph)

def test_graph():

    # Create a graphlib graph object
    graph = graphviz.Digraph()
    graph.edge("run", "intr")
    graph.edge("intr", "runbl")
    graph.edge("runbl", "run")
    graph.edge("run", "kernel")
    graph.edge("kernel", "zombie")
    graph.edge("kernel", "sleep")
    graph.edge("kernel", "runmem")
    graph.edge("sleep", "swap")
    graph.edge("swap", "runswap")
    graph.edge("runswap", "new")
    graph.edge("runswap", "runmem")
    graph.edge("new", "runmem")
    graph.edge("sleep", "runmem")

    st.graphviz_chart(graph)


def simple_graph(all_people_df):
    
    source = []
    target =[]
    weight = []
    
    #for index, row in all_people_df.head(50).iterrows():
    for index, row in all_people_df.iterrows():
        source.append(row['NAME'])
        target.append(row['PersonNm'])
        weight.append(1)
        
    # Create adjacency matrix
    adjmat = vec2adjmat(source, target, weight=weight)

    # Initialize
    d3 = d3graph()

    # Build force-directed graph with default settings
    d3.graph(adjmat)
    d3.show(filepath='data/g1.html')


def main():
    st.set_page_config(APP_TITLE) #, layout="wide")
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    msg = """
    This is a test of graphing people and connections to nonprofit orgs.

    When you open or refresh this page, it builds a graph that will open 
    in a seperate browser window.

    
    """

    st.markdown(msg)

    all_people_df = get_people_df()
    
    simple_graph(all_people_df)
    #build_people_graph(all_people_df)
    
    
    # quick_gv()
    # test_graph()


if __name__ == "__main__":
    main()
