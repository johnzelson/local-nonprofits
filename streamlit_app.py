# installs
# py -m pip install streamlit
# py -m pip install pandas
# py -m pip install folium              # don't need as streamlit-folium 
# py -m pip install streamlit_folium
# py -m pip install geopandas
# py -m pip install streamlit-card              # testing
# py -m pip install streamlit_extras            # testing
# py -m pip install streamlit-elements==0.1.*   # testing

# python -m streamlit run your_script.py

import streamlit as st
import pandas as pd
import folium  #TODO: is needed, but didn't install 
from streamlit_folium import st_folium
import geopandas as gpd
import math


import streamlit.components.v1 as components

# test options for layout
#from streamlit_card import card 
#from streamlit_extras.stylable_container import stylable_container 
#from streamlit_extras.colored_header import colored_header
#from streamlit_extras.grid import grid
#from streamlit_elements import elements, mui, html
#from streamlit_elements import dashboard


APP_TITLE = 'Local Nonprofits'
APP_SUB_TITLE = 'Source:  IRS Tax Returns and APS for Census, Congress, Bing '


def do_sidebar(df, np_name, m):
    """ Build sidebar  
    
    Parameters :
    df (dataframe): all the nonprofit info, np_local_df
    np_name (str):  name of nonprofit 
    m (map object): 

    Returns: selected_np (str)

    """

    with st.sidebar:

        nonprofits_tab, selected_tab, tab3, tab4 = st.tabs(["Nonprofits", "Selected", "Help", "Status"])

        with nonprofits_tab:
            np_list = st.session_state.np_list
            # np_index = np_list.index
            st.header("Nonprofits")
            
            if np_name:
                np_index = np_list.index(np_name)
            else:
                np_index = 0

            selected_np = st.radio('Pick NP', np_list, 
                                   index=np_index, 
                                   key="np_radio")

            st.session_state['selected_np'] = selected_np 

            # xxx TODO: check whether this is required
            if 'last_object_clicked_tooltip' in m:
                st.write ("last map click:  ",  m['last_object_clicked_tooltip'])
                st.write ("radio select:  ", selected_np)
            else:
                st.write("no m")

        with selected_tab:
            st.header("Selected")
            st.write(selected_np)
            # get detailed on selected np    
            
            filt = df['NAME'] == selected_np
            st.write(df.loc[filt].T)

        with tab3:
            st.header("Help")
            st.write("Where is data from how to use, etc")

            st.write(f"Number of Nonprofits: {st.session_state.num_rows}")
            st.write(f"Data Elements for each Nonprofit: {st.session_state.num_facts}")
        with tab4:
            st.write ("What up")
            if 'map_click' in st.session_state:
                st.write("map click " + st.session_state('map_click'))
            else:
                st.write ("no map click yet")
            st.write("-- session state -- ")
            for ss in st.session_state:
                st.write(ss, st.session_state[ss])

    # TODO: decide whether to write or just return values
    # for now, copy parts of popup def     

    return selected_np


# deleteme
#def display_np_filter(df, np_name):
#    np_list = [''] + list(df['NAME'])
#    np_list.sort()
#    np_index = np_list.index(np_name)
#    return st.sidebar.selectbox('np list', np_list, np_index)


# deleteme
#def display_np_radio(df):
#  
#    np_list = list(df['NAME'])
#    np_list.sort()

#    return st.sidebar.radio('Pick NP', np_list)



# deleteme
#def list_nonprofits (df):
#    st.write(df[['NAME', 'STREET']])

# deleteme
#def list_np_details(df, np_name):
#    # change to p_org_id 
#    filt = df['NAME'] == np_name
#    # details = df.loc[filt]
#    st.write(df.loc[filt].T)


def get_map_popup(row, df) :
    """ Returns HTML for map popup when user clicks on a Nonprofit """

    st.session_state['selected_np'] = row.NAME
    # st.write(row.NAME)
    # st.write(st_data["last_clicked"])

    return (f'<div>'
    f'<table class="table table-striped table-hover table-condensed table-responsive">'
    f'<tr> '
    f"<td> Name:</td> <td>  {row.NAME} </td> "
    f'</tr> '
    f'<tr> '
    f"<td> Post Addr:</td> <td> {row.STREET}, {row.CITY} </td> "
    f'</tr> </table>')



# ----- end get popup

# deleteme
# def info_panel(np_dict):
#    # st.write(np_dict)
#    st.write(np_dict['NAME'])
#    st.write(np_dict['STREET'])


# unfinished attempt to interactively update map 
# (based on radio button selection)
def update_marker(m, coords):
    fgs = folium.FeatureGroup(name="selected")

    st.write(coords)
    
    fgs.add_child(
        folium.Marker(
                # location=coords,
                location=[  42, -76 ],
                popup=f"added popup"
        )
    )


    d = st_folium(m)
    #          center=[42.5,-76])

    '''
    folium.CircleMarker(    
                location=coords,
                popup=f"added popup",
                tooltip=f"added tooltip",
                icon=folium.Icon(color="green")
    ).add_to(fgs)
    '''
    
    out = st_folium(
        m,
        feature_group_to_add=fgs,
    #    center=[42, -76]
    )
    

def display_map(np_local_df, tracts_cc_gpd):
    """ Draws Map.  Returns st_map and selected nonprofit """
    import math

    m = folium.Map(
        location=[42.5,-76],
        #center=[42.5,-76],  # returns world map vs location
        zoom_start=10,
    )
        # key="np_map"
    #)

    # you can pass gdf to geojson
    folium.GeoJson(tracts_cc_gpd,
                fill_opacity=0.1,
                highlight=True,
                popup=folium.GeoJsonPopup(fields=['NAME']),
                name="Census Tracts").add_to(m)
    
    nps = folium.FeatureGroup("NPs").add_to(m)


    for index, row in np_local_df.iterrows():

        if not math.isnan(row['coord_x']):  # the data has po boxes with no lat long

            folium.CircleMarker(
            #folium.Marker(    
                location=[  row['coord_y'], row['coord_x'] ],
                #folium.Marker(location=[ row['coord_x'], row['coord_y'] ],
                fill=True,
                #Highlight=True,
                color = '#4cdc7c',
                highlight= True,
                # highlight_function= lambda feat: {'fillColor': '#00FF00'},
                #highlight_function=lambda x: {"fillOpacity": 0.9},
                #zoom_on_click=True,
                #popup=row['NAME'],
                #popup=folium.Popup(row['NAME']),
                #popup=folium.Popup(html),
                #popup=folium.Popup(get_popup(row), max_width=300),
                #popup=folium.Popup(get_map_popup(row), max_width=300),
                popup=folium.Popup(get_map_popup(row, np_local_df), max_width=300),
                #tooltip=row['NAME'],
                tooltip = row.NAME,
                #radius=15,
            # fill_color="#3db7e4"
                ).add_to(nps)

    folium.LayerControl().add_to(m)



    st_map  = st_folium(m, 
                        width=700) #, returned_objects=["last_object_clicked"])
    
    selected_np = ''
    if st_map['last_active_drawing']:
        #state_name = st_map['last_active_drawing']['properties']['name']
        selected_np =  st_map["last_object_clicked_tooltip"]
        st.write ("selected np in map click: " + selected_np)
        st.session_state['selected_np'] = selected_np #hm, just in case

    return selected_np, st_map # experiment to return map...

def display_interesting_links(df_dict):
    """ External Links to more data about an Org 

    Paramters: df_dict(dict): dictionary with all data for selected nonprofit

    Return:  link_list (list of dicts):  external links
    Not using return list, just displaying
    
    """
    link_list = []

    # Census Reporter Analysis of census tract of org
    more_info = {}
    more_info['src_name'] = "Census Reporter"
    # more_info['ein'] = df_dict['EIN']
    more_info['general_desc'] = "Censusreporter offers awesome summaries of Census Info"
    

    # https://censusreporter.org/locate/?lat=42.598131&lng=-76.17985
    # lat is coord_y
    lat = df_dict['coord_y']
    lng = df_dict['coord_x']
    #url = f"https://censusreporter.org/locate/?lat={lat}&lng={lng}"

    url = 'https://censusreporter.org/locate/'
    url += f"?lat={lat}&lng={lng}"
    full_link = f"<a href=\"{url}\" target=\"_blank\">Census Reporter Demographics &#8594;</a>"
    more_info['link'] = full_link
    link_list.append(more_info)

    #probublica
    #https://projects.propublica.org/nonprofits/organizations/132951986
    # Census Reporter Analysis of census tract of org
    more_info = {}
    more_info['src_name'] = "Propbublica"
    # more_info['ein'] = df_dict['EIN']
    more_info['general_desc'] = "ProPublica is an independent, nonprofit newsroom that produces investigative journalism with moral force"
    url = f"https://projects.propublica.org/nonprofits/organizations/{df_dict["EIN"]}"
    full_link = f"<a href=\"{url}\" target=\"_blank\">Propublica Nonprofit Explorer &#8594;</a>"
    more_info['link'] = full_link
    link_list.append(more_info)

    tbl_html = "<table> " # class=\"my_table\">  "
    tbl_html += "<tr> <td colspan=3 class=\"my_cell_section\"> "
    tbl_html += "<div class=\"tooltip\">" + "Interesting External Links"
    tbl_html += "\t <span class=\"tooltiptext\">"
    tbl_html +=  "Resources for Learning about Orgs and Demographics"
    tbl_html += "\t </span>"
    tbl_html += "</div>"

    tbl_html +=  "</td> </tr>"

    
    for link in link_list:
        tbl_html += "<tr> "
        tbl_html += "<td>"
        tbl_html += link['src_name']
        tbl_html += "</td>"

        tbl_html += "<td>"
        tbl_html += link['general_desc']
        tbl_html += "</td>"

        tbl_html += "<td>"
        tbl_html += link['link']
        tbl_html += "</td>"

        tbl_html += "</tr> "

    tbl_html += "</table>"
    st.markdown(tbl_html, unsafe_allow_html=True)
    
    return link_list


def display_section(sect, which_display, df_dict, present_lu):
    """ Generate table of data based presentation lookup 

    Parameters:
        present_lu (dict): presentation lookup.    Read from presentation_lookups.csv
        which_display (str):  which fields get included
        sect (str): which section of using presentation lookups, present_lu dict
        df_dict (dict): dictionary from dataframe with one NP

    Returns: None.  (writes html)

    """
    
    #TODO: Investigate whether Using HTML with st.markdown can be avoided by using streamlit functions

    sect_dict = {} # dict of list keys/fields in section

    # load a dict, key of section, with list of data elements to include 
    #TODO: change var name s to something more description (eg. field_name)
    for s in  present_lu:
        sect_name = present_lu[s][which_display]
  
        if sect_name not in sect_dict:
            sect_dict[sect_name] = []

        sect_dict[sect_name].append(s)

    show_list = sect_dict[sect]

    s = ''
    tbl_html = "<table> " # class=\"my_table\">  "
    # tbl_html += "<tr> "
    tbl_html += "<tr> <td colspan=2 class=\"my_cell_section\"> "
    tbl_html += "<div class=\"tooltip\">" + sect
    tbl_html += "\t <span class=\"tooltiptext\">"
    tbl_html +=  present_lu[sect]['help']  
    tbl_html += "\t </span>"
    tbl_html += "</div>"

    tbl_html +=  "</td> </tr>"

    for s in show_list:
        tbl_html += "<tr> "
        
        # tooltip info
        h = "Definition: " + present_lu[s]['help'] + "(data source: " + present_lu[s]['source'] + ")<br>"
        h += "(data element name:  " +  s + ")"
        # tbl_html += "<td title=\"" + h + "\">"
        tbl_html += "<td class=\"td_label\">"    
        
        # lookup field name to get a presentable label
        present_s_name = present_lu[s]['display_name']
        

        tbl_html += "<div class=\"tooltip\">" + present_s_name 
        tbl_html += "\t <span class=\"tooltiptext\">"
        tbl_html += h  
        tbl_html += "\t </span>"
        tbl_html += "</div>"
        tbl_html += "</td>"
        tbl_html += "<td>"


        #TODO: more graceful handling of null, tag not found, and problems with presentat lu    
        #TODO: in S2, used Tag not in file. fixed, but need to regenerate
        #TODO: need to review data processing for consistent nulls and not founds
        if (s in df_dict 
            and df_dict[s] not in ["tag_not_found", "Tag not in file", "nan", "Nan"]
            and not pd.isnull(df_dict[s])
            ):  

            try:

                if present_lu[s]['format'] == 'int':   
                    tbl_html += str(int(df_dict[s])) 

                elif present_lu[s]['format'] == 'currency':    
                    val = float(df_dict[s])    
                    val_string = '${:,.0f}'.format(val)
                    tbl_html += val_string
                elif present_lu[s]['format'] == 'url':
                    # ?: in streamlit,target=_blank with st.markdown, but not with st.html
                    #tbl_html += f"<a href=\"https://{df_dict[s]}\"   rel=\"noopener noreferrer \"> "
                    tbl_html += f"<a href=\"https://{df_dict[s]}\"   target=\"_blank\"> "
                    tbl_html += f"{df_dict[s]} &#8594;</a> "
                elif present_lu[s]['format'] == 'link':
                    tbl_html += df_dict[s]

                elif present_lu[s]['format'] == "cap":   # narratives in sentence case, instead of all caps
                    tbl_html += str(df_dict[s]).capitalize()
                
                else:
                    tbl_html +=   str(df_dict[s])

            except:
                tbl_html += "ERROR: "
                tbl_html +=  "df_dict s: (" + str(df_dict[s]) + ") <br>"
                tbl_html +=  "present_lu s: " + str(present_lu[s]) + "<br>"
                tbl_html +=  "s: " + s
        else:
            if not s in df_dict:
                tbl_html += "This tag in presentation, but not in df"
            else:
                tbl_html += "(tnf)"

        tbl_html += "</td> </tr>"
    #org_dict = df_dict.fromkeys(show_list, 0)
    # st.write(org_dict)
    
    tbl_html += "</table>"
    #st.html (tbl_html)
    st.markdown(tbl_html, unsafe_allow_html=True)



def display_arbitrary_list (df_dict, present_lu, show_list):
    """ Display table of arbitrary data elements """
 
    tbl_html = "<table>  "
    for s in show_list:
        tbl_html += "<tr> "

        # st.write(df_dict[s])
        # org_dict.update(df_dict[s])  # doesn't work??
        
        h = "Definition: " + present_lu[s]['help'] + "(data source: " + present_lu[s]['source'] + ")"
        # tbl_html += "<td title=\"" + h + "\">"
        tbl_html += "<td>"    
        # change keys in dict to presentable?
        present_s_name = present_lu[s]['display_name']
        
        # present_s_help = present_lu[s][5]    
        #org_dict[present_lu[s][1]] = df_dict[s] 
        
        tbl_html += "<div class=\"tooltip\">" + present_s_name 
        tbl_html += " <span class=\"tooltiptext\">"
        tbl_html += h  
        tbl_html += "</span>"
        tbl_html += "</div>"
        # st.markdown(present_lu[s][1], help=h)     
        tbl_html += "</td>"
        tbl_html += "<td>"

 
        #TODO: make a def?   copied from display section
        if (s in df_dict 
            and df_dict[s] not in ["tag_not_found", "Tag not in file", "nan", "Nan"]
            and not pd.isnull(df_dict[s])
            ):  

            try:

                if present_lu[s]['format'] == 'int':   
                    tbl_html += str(int(df_dict[s])) 

                elif present_lu[s]['format'] == 'currency':    
                    val = float(df_dict[s])    
                    val_string = '${:,.0f}'.format(val)
                    tbl_html += val_string
                elif present_lu[s]['format'] == 'url':
                    # in streamlit,target=_blank works when printed with st.markdown, but not with st.html
                    #tbl_html += f"<a href=\"https://{df_dict[s]}\"   rel=\"noopener noreferrer \"> "
                    tbl_html += f"<a href=\"https://{df_dict[s]}\"   target=\"_blank\"> "
                    tbl_html += f"{df_dict[s]} &#8594;</a> "
                elif present_lu[s]['format'] == 'link':
                    tbl_html += df_dict[s]

                elif present_lu[s]['format'] == "cap":   # narratives in sentence case, instead of all caps
                    tbl_html += str(df_dict[s]).capitalize()
                
                else:
                    tbl_html +=   str(df_dict[s])

            except:
                tbl_html += "ERROR: "
                tbl_html +=  "df_dict s: (" + str(df_dict[s]) + ") <br>"
                tbl_html +=  "present_lu s: " + str(present_lu[s]) + "<br>"
                tbl_html +=  "s: " + s
        else:
            if not s in df_dict:
                tbl_html += "This tag in presentation, but not in df"
            else:
                tbl_html += "(tnf)"
        # ---  end copy      

        tbl_html += "</td> </tr>"
    #org_dict = df_dict.fromkeys(show_list, 0)
    # st.write(org_dict)
    
    tbl_html += "</table>"
    st.html (tbl_html)

#    return arb_dict



def get_people(df_dict):
    #TODO: fix this data during data processing, not in app     
    import json

    # the irs data uses single quote in json
    # and in person name
    # "KATHLEEN O'CONNELL"
    import re

    ppl = df_dict['people']
    #st.write (type(ppl))
    #st.write (len(ppl))
    
    #st.write (type(df_dict['people']))
    #st.write(len(dict['people']))
    
    if isinstance(ppl, str):

        quoted_stuff = re.findall('"([^"]*)"', ppl)
        # st.write (quoted_stuff)
        for t in quoted_stuff:        
            fix_t = t.replace("'", " ") # KATHLEEN O CONNELL 
            # ok, try this way
            ppl = ppl.replace(t, fix_t) # replace name with no sq

        # after taking sq from any quoted string
        # then replace dq with single quote   
        ppl = ppl.replace('"', "'")   # with quoted handled, make all sq
        ppl =  ppl.replace("'", '"')  # replace sq with dq for json

        # st.text (ppl)
        ppl_dict = json.loads(ppl)
        # return {'status' : 'no people'}
        return ppl_dict
    else:
        return {'status' : 'no people'}


def load_present_lu():
    """ load present_lu, presentation lookups dict, used to present consistent labels 
    
    """
    #TODO: merge this with processing lookup tables?

    import csv

    present_lu = {}

    with open('data/presentation_lookups.csv', mode='r') as infile:

        reader = csv.reader(infile)
        row_cnt = 1
        for row in reader:
            if row_cnt == 1:
                keys = row
                row_cnt += 1
            else:
                present_lu[row[1]] = dict(zip(keys, row))
                row_cnt += 1

        for fld_dict in present_lu:
            del present_lu[fld_dict]['key_name']
            del present_lu[fld_dict]['sample']

    return present_lu


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # setup styles for used in HTML tables of data and tooltips
    css_table = ''' 
            <style>
            
            table {
                /* border-collapse: collapse; */
                width: 100%;
                border: 1px;
            }

            th, td {
                text-align: left;
                padding: 3px;
                /* border: 1px solid black;  */
            }

            td {
                border: black 1px;
                }

            tr:nth-child(even) {background-color: #f2f2f2;}

            .tooltip {
                position: relative;
                display: inline-block;
                border-bottom: 1px dotted black;
            }

            .tooltip .tooltiptext {
                visibility: hidden;
                width: 300px; 
                background-color: black;
                color: #fff;
                /* text-align: center; */
                border-radius: 6px;
                padding: 15px 15px 15px 15px; 
                /* Position the tooltip */
                position: absolute;
                z-index: 1;
            }

            .tooltip:hover .tooltiptext {
                visibility: visible;
            }

            .my_table{
                border-collapse: collapse; 
                width: 100%;
                border: 1px;

            }

            .my_cell_section {
                text-align: center; 
                vertical-align: middle;
                font-weight:  bold;
            }

                                                        
            </style>

        '''    

    st.markdown (css_table, unsafe_allow_html=True)

    # load data
    # pre-processed in google colab

    dtype = {"CLASSIFICATION": str,
         "EIN" : str,
         "ACTIVITY" : str,
         "AFFILIATION" : str,
         "ORGANIZATION" : str,
         "FOUNDATION" : str,
         "NTEE_CD" : str,
         "RULING" : str,
         "ZIP" : str,
         "TAX_PERIOD" : str,
         "GROUP" : str,
         "cb_BASENAME" : int, 
         "cb_BLKGRP" : int,
         "cb_BLOCK": str,
         "cb_GEOID" : str,
         "ZipCd" : str
         }

    np_local_df = pd.read_csv('data/np_local_df.csv')

    # tracts for new york, filter to cortland county
    tracts_gpd = gpd.read_file('data/tl_2022_36_tract.shp')
    tracts_cc_gpd = tracts_gpd[tracts_gpd['COUNTYFP'] == '023']

    # Initialize session data
    
    #TODO: check-why put in session state? just put in sidebar?
    if 'np_list' not in st.session_state:
        np_list = list(np_local_df['NAME'])
        np_list.sort()
        st.session_state['np_list'] = np_list

    if 'num_nps' not in st.session_state:
        (num_rows, num_facts) = np_local_df.shape
        st.session_state['num_rows'] = num_rows
        st.session_state['num_facts'] = num_facts
    
    # Load presentation dictionary with human-readable labels, definitions
    # and groupings/collections to present
    present_lu = load_present_lu()


    # main content area
    map_tab, sum_tab, all_tab, graph_tests = st.tabs(["Map", "Organization Info", "All Data Elements", "Graph Tests"])


    with map_tab:
        #  ----------- map -----------------------
        selected_np = ''
        (selected_np, st_map) = display_map(np_local_df, tracts_cc_gpd)
        selected_np = do_sidebar(np_local_df, selected_np, st_map)

        # temp debugging
        st.write(st_map)

        #TODO: when user selects from radio buttons, want to adjust map dynamically
        # https://folium.streamlit.app/dynamic_map_vs_rerender
        
        #st.write(st_map['last_object_clicked']['lat'])
        #st.write(st_map['last_object_clicked']['lon'])
        
        # update_marker(st_map, [-42, 76])
        
        # st_folium(st_map, center=[-42, 76])
        # st_folium(st_map, location=[42.5,-76])

        # "center":{
        # "lat":42.500453028125584
        # "lng":-76.03500366210939


    with sum_tab:
        # ----- info -----------------------------
        #st.write("Summary Tab")
        st.subheader(selected_np)
        
        # get detailed on selected np, lookup by name for now  
        #TODO: use something else for ID.  EIN? Name + EIN?  
        filt = np_local_df['NAME'] == selected_np

        # convert the selected nonprofit to dict 
        # https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
        df_dict = np_local_df.loc[filt].to_dict('records')[0]

        #TODO: Add iteration  
        # sects_to_show = ['IRS Business Master File', 'Form 990x', 'Staff and Board']

        # link to all sedtions for reference
        #st.markdown('''
        #            [BMF](#section-1-bmf) | 
        #            [IRS Form 990-series](#section-2-990x) | 
        #            [Stf](#section-3-staff-and-board)  |
        #            [Census](#section-4-census) |
        # interesting
        #            [Web](#section-5-web)    
        #            ''')

        # could use same toc just dump it, but prefer to not link current section
        #toc_md = '[IRS Form 990-series](#section-2-990x) | [Stf](#section-3-staff-and-board)'
        #st.markdown(toc_md)
        
        # sect 1 BMF
        st.markdown('##### Section 1: Business Master File (BMF)')
        st.markdown('''
                     BMF  | 
                    [IRS Form 990-series](#section-2-990x) | 
                    [Staff/Board](#section-3-staff-and-board)  |
                    [Census](#section-4-census) |
                    [Links](#section-5-interesting-links) |
                    [Web](#section-6-web)    
                    ''')
        display_section('IRS Business Master File', 'display_section_summary', df_dict, present_lu)
        st.divider()


        # sect 2 Form 990 series
        st.markdown('##### Section 2: 990x')  # section name
        st.markdown('''
                    [BMF](#section-1-business-master-file-bmf) | 
                    [IRS Form 990-series](#section-2-990x) | 
                    [Staff/Board](#section-3-staff-and-board)  |
                    [Census](#section-4-census) | 
                    [Links](#section-5-interesting-links) |
                    [Web](#section-6-web) 
                    ''')

        #check if form 990x for np is in data, df_dict
        if isinstance(df_dict['filename'], str):
            display_section('Form 990x', 'display_section_summary', df_dict, present_lu)
        else:
            st.html("&nbsp &nbsp No Tax Return for this Organization from from submissions in 2023 thru July 2024")
            st.html("&nbsp &nbsp Check the Propublica External Link Below")
        # sect 3 staff and board
        st.markdown('##### Section 3: Staff and Board')  # section name
        st.markdown('''
                    [BMF](#section-1-business-master-file-bmf) | 
                    [IRS Form 990-series](#section-2-990x) | 
                    [Staff/Board](#section-3-staff-and-board)  |
                    [Census](#section-4-census) |
                    [Links](#section-5-interesting-links) | 
                    [Web](#section-6-web) 
                    ''')
        st.table(get_people(df_dict))

        st.divider()  
        # sect 4 census
        st.markdown('##### Section 4: Census')          # section name
        st.markdown('''
                    [BMF](#section-1-business-master-file-bmf) | 
                    [IRS Form 990-series](#section-2-990x) | 
                    [Staff/Board](#section-3-staff-and-board)  |
                    [Census](#section-4-census) |
                    [Links](#section-5-interesting-links) | 
                    [Web](#section-6-web) 
                    ''')
        display_section('Census', 'display_section_summary', df_dict, present_lu)

        st.divider()  

        st.markdown('##### Section 5: Interesting Links')  # section name
        st.markdown('''
                    [BMF](#section-1-business-master-file-bmf) | 
                    [IRS Form 990-series](#section-2-990x) | 
                    [Staff/Board](#section-3-staff-and-board)  |
                    [Census](#section-4-census) |
                    [Links](#section-5-interesting-links) | 
                    [Web](#section-6-web) 
                    ''')        
        display_interesting_links(df_dict)

        st.divider()  
                
        # sect 5 web
        st.markdown('##### Section 6: Web')          # section name
        st.markdown('''
                    [BMF](#section-1-business-master-file-bmf) | 
                    [IRS Form 990-series](#section-2-990x) | 
                    [Staff/Board](#section-3-staff-and-board)  |
                    [Census](#section-4-census) |
                    [Links](#section-5-interesting-links) | 
                    [Web](#section-6-web) 
                    ''')
        display_section('Web', 'display_section_summary', df_dict, present_lu)


 
    with all_tab:

        st.subheader(selected_np)
        st.write("(all data elements)")
        #st.table(org_basics(df_dict, present_lu))

        display_section('IRS Business Master File', 'display_section_all', df_dict, present_lu)
 
        #TODO: add check if tax info is in data. if not, print note and skip 
        
        if isinstance(df_dict['filename'], str):
            display_section('Form 990x', 'display_section_all', df_dict, present_lu)
            st.subheader("People listed on IRS Tax Form")
            st.table(get_people(df_dict))
        else:
            st.write("(No Tax Return for this EIN, from submissions in 2023 thru July 2024")
        
        display_section('Census', 'display_section_all', df_dict, present_lu)

        st.subheader("Web Search")
        display_section('Web', 'display_section_all', df_dict, present_lu)

    with graph_tests:
        st.subheader(selected_np)
        st.write("(Info about the geographic area)")
        show_list = ['coord_x', 'coord_y', 'cb_NAME', 'centracts_NAME', 'cb_GEOID']
        display_arbitrary_list(df_dict, present_lu, show_list)

        # build census tract geo id
        # https://www.census.gov/programs-surveys/geography/technical-documentation/naming-convention/cartographic-boundary-file/carto-boundary-summary-level.html
        # 140	State-County-Census Tract

        # https://censusreporter.org/topics/geography/
        # NNN 	Summary level (three digits)
        # 00 	Geographic component (always 00)*
        # US 	Separator (always US)

        cen_tract_summary = '14000US'
        st_fips = '36'  
        #TODO:get from df, but have to check int to str on county (023 vs 23)
        #TODO: review all loads from csv and checks to make sure geoid/cds are str
        cnty_fips = '023'
        tract_cd = str(int(df_dict['centracts_TRACT'])).strip()
        tract_geoid = cen_tract_summary + st_fips + cnty_fips + tract_cd
        tract_geoid = tract_geoid.strip()


        dc_hl = f"""
        <script src=\"https://datacommons.org/datacommons.js\"></script>
        <datacommons-highlight
            header="Census Track {tract_cd} Population"
            place=\"geoId/36023{tract_cd}\"
            variable=\"Count_Person\"
        ></datacommons-highlight> """
        components.html(dc_hl, height=200)


        # works
        dc_graph = """ 
            <script src=\"https://datacommons.org/datacommons.js\"></script>
            <datacommons-line
                header=\"Cortland County Population Over Time\"
                place=\"geoId/36023\"
                variables=\"Count_Person\"
            ></datacommons-line>  """        
        components.html(dc_graph, height=400)

        import math
        tract_list = []
        all_tracts = " "

        tracts_list = np_local_df['cb_TRACT'].unique()
        # st.write (tracts_list)
        
        #TODO:Again: all census needs to be string in all csv loads during processing
        # for now, fix it here
        # create space seperated list of geoids that data commons wants
        for tract in tracts_list:
            if not math.isnan(tract):
                tract_str = str(int(tract))
                all_tracts += "geoId/36023" + tract_str + " "
        
        dc_graph = f""" 
            <script src=\"https://datacommons.org/datacommons.js\"></script>
            <datacommons-bar
                header=\"Census Tract Population\"
                places=\"{all_tracts} \"
                variables=\"Count_Person\"
            ></datacommons-bar>  """        
        components.html(dc_graph, height=400)


        dc_graph = f""" 
            <script src=\"https://datacommons.org/datacommons.js\"></script>
            <datacommons-bar
                header=\"Median Income by Census Tract\"
                places=\"{all_tracts} \"
                variables=\"Median_Income_Household Median_Income_Person\"
            ></datacommons-bar>  """        
        components.html(dc_graph, height=400)

        # 1400000US01015001000
        # 14000US36023971200

        # https://censusreporter.org/profiles/14000US36023971200
        cr_link = "https://censusreporter.org/profiles/" + tract_geoid
        link_title = "Censusreporter Tract Reports"
    
        #writing a url 
        st.write(f"[{link_title}](%s)" % cr_link)



        # components.html(censusreport_frame, height=250)

        # make it easier to construct
        st.write ("Cenus Tract GEOID: " + tract_geoid)

        cr_f1 = "<iframe id=\"cr-embed-14000US36023970900-demographics-race\" "
        cr_f1 += "class=\"census-reporter-embed\" "
        cr_f1 += "src=\"https://s3.amazonaws.com/embed.censusreporter.org/1.0/iframe.html"
        #cr_f1 += "?geoID=14000US36023970900"
        cr_f1 += "?geoID=" + tract_geoid
        cr_f1 += "&chartDataID=demographics-race"
        cr_f1 += "&dataYear=2022"
        cr_f1 += "&releaseID=ACS_2022_5-year"
        cr_f1 += "&chartType=column"
        cr_f1 += "&chartHeight=200"
        cr_f1 += "&chartQualifier=Hispanic+includes+respondents+of+any+race.+Other+categories+are+non-Hispanic."
        cr_f1 += "&chartTitle=&initialSort="
        cr_f1 += "&statType=scaled-percentage\"" 
        cr_f1 += "    frameborder=\"0\" width=\"100%\" height=\"300\"" 
        cr_f1 += "    style=\"margin: 1em; max-width: 720px;\"></iframe>"
            
        cr_f1 += "<script src=\"https://s3.amazonaws.com/embed.censusreporter.org/1.0/js/embed.chart.make.js\">"
        cr_f1 += "</script>"

        # works, but comment for testing other things
        components.html(cr_f1, height=250)


if __name__ == "__main__":
    main()
    
