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



# test 3rd party options for layout
#import streamlit.components.v1 as components
#from streamlit_card import card 
#from streamlit_extras.stylable_container import stylable_container 
#from streamlit_extras.colored_header import colored_header
#from streamlit_extras.grid import grid

#from streamlit_elements import elements, mui, html
#from streamlit_elements import dashboard


APP_TITLE = 'Mapping Nonprofits'
APP_SUB_TITLE = 'Source:  IRS Tax Returns and APS for Census, Congress, Bing '


def np_change():
    mytoggle = True

def do_sidebar(df, np_name, m):
    with st.sidebar:

        tab1, tab2, tab3, tab4 = st.tabs(["Nonprofits", "Selected", "Help", "Status"])

        with tab1:
            np_list = st.session_state.np_list
            # np_index = np_list.index
            st.header("Nonprofits")
            
            if np_name:
                np_index = np_list.index(np_name)
            else:
                np_index = 0

            #if np_name:
            #    np_index = np_list.index(np_name)
            #    selected_np = st.radio('Pick NP', np_list, index=np_index)
            #else:        
            #    selected_np = st.radio('Pick NP', np_list, index=0)
            #    st.session_state['selected_np'] = selected_np 


            #selected_np = st.radio('Pick NP', np_list, index=np_index)

            selected_np = st.radio('Pick NP', np_list, 
                                   index=np_index, 
                                   key="np_radio")
            #                       on_change=np_change)


            st.session_state['selected_np'] = selected_np 

            # xxx test
            if 'last_object_clicked_tooltip' in m:
                st.write ("last map click:  ",  m['last_object_clicked_tooltip'])
                st.write ("radio select:  ", selected_np)
            else:
                st.write("no m")

        with tab2:
            st.header("Selected")
            st.write(selected_np)
            # get detailed on selected np    
            
            filt = df['NAME'] == selected_np
            # details = df.loc[filt]
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
#def do_info_panel(df):
    # TODO: decide whether to write or just return values
    # for now, copy parts of popup def     

    return selected_np


def display_np_filter(df, np_name):
    np_list = [''] + list(df['NAME'])
    np_list.sort()
    
    np_index = np_list.index(np_name)
    return st.sidebar.selectbox('np list', np_list, np_index)


def display_np_radio(df):
  
    np_list = list(df['NAME'])
    np_list.sort()

    return st.sidebar.radio('Pick NP', np_list)

# def toggle_button():
#    st.session_state.button_clicked = not st.session_state.button_clicked

# st.button('Click me', on_click=toggle_button)

# create tabs in sidebar


def list_nonprofits (df):
    st.write(df[['NAME', 'STREET']])

def list_np_details(df, np_name):
    # change to p_org_id 
    filt = df['NAME'] == np_name
    # details = df.loc[filt]
    st.write(df.loc[filt].T)


def get_map_popup(row, df) :

    st.session_state['selected_np'] = row.NAME
    # st.write(row.NAME)
    # st.write(st_data["last_clicked"])

    return (f'<div>'
    f'<table class="table table-striped table-hover table-condensed table-responsive">'
    f'<tr> '
    f'<td> Name:</td> <td>  {row.NAME} </td> '
    f'</tr> '
    f'<tr> '
    f'<td> Post Addr:</td> <td> {row.STREET}, {row.CITY} </td> '
    f'</tr> </table>')



def get_popup (row):
    # moving to get map popup...
    #TODO: put logic to skip nulls, notate which website, etc
    #TODO: use api.congress.gov to get stuff, https://www.congress.gov/help/using-data-offsite
    # key saved in secrets
    # https://api.congress.gov/v3/member/MI/10?api_key=[INSERT_KEY]
    # https://api.congress.gov/v3/member/NY/19?api_key=pYKHRuu4IQNyahFhDLEeiCGJhCILctRhjY6QdYVA

    
    # -- ny state legislature links --
    # TODO: check census to see if it can deliver link ready value
    # assumes consistency
    #senate link format: https://www.nysenate.gov/district/48
    #data format:  State (Upper): 	State Senate District 48
    legup_link_parts = row.legup_NAME.split(' ')

    #https://www.nysenate.gov/district/48
    legup_link = (f"<a href=\"https://www.nysenate.gov/district/{legup_link_parts[-1]}\" "
                f"target=\"_blank\"> {row.legup_NAME} </a>")


    # format for assembly:  https://www.assembly.state.ny.us/mem/?ad=125&sh=about
    # data format:  Assembly District 125
    leglow_link_parts = row.leglow_NAME.split(' ')
    leglow_link = (f"<a href=\"https://www.assembly.state.ny.us/mem/?ad={leglow_link_parts[-1]}&sh=about\" "
                f"target=\"_blank\"> {row.leglow_NAME} </a>")

    # get congressional distict info
    # district_dict[dist] loaded previously
    #cong_dist_url = district_dict[row.cong_NAME]['house_url']
    #cong_mbr_name = district_dict[row.cong_NAME]['name']
    #cong_dist_link = (f' <a href=\"{cong_dist_url}\" '
    #            f'target=\"_blank\"> {row.cong_NAME} - {cong_mbr_name}</a> ')
    cong_dist_link = ''
                
    # website
    if not pd.isnull(row.WebsiteAddressTxt):
        if row.WebsiteAddressTxt == 'tag_not_found':
            web_url = (f'<a href=\"{row.url}\" '
                    f' target=\"_blank\"> {row.found_name} (web search) </a>')
        else:
            web_url = (f'<a href=\"https://{row.WebsiteAddressTxt}\" '
                    f' target=\"_blank\"> {row.WebsiteAddressTxt} (IRS)</a>')
    elif not pd.isnull(row.url):
            web_url = (f'<a href=\"{row.url}\" '
                    f' target=\"_blank\"> {row.found_name} (web search) </a>')
    else:
        web_url = 'No Website Found'

    # format for guidestar 12-23456789
    ein = str(row.EIN)
    ein2 = ein[:2]
    ein7 = ein[2:9]
    return (f'<div>'
    f'<table class="table table-striped table-hover table-condensed table-responsive">'
    f'<tr> '
    f'<td> Name:</td> <td>  {row.NAME} </td> '
    f'</tr> '
    f'<tr> '
    f'<td> Post Addr:</td> <td> {row.STREET}, {row.CITY} </td> '
    f'</tr> '
    f'<tr> '
    f'<td> IRS Contact:</td> <td> {row.ICO} </td> '
    f'</tr> '

    f'<tr> '
    f'<td> EIN:</td> <td> {row.EIN} </td> '
    f'</tr> '

    f'<tr> '
    f'<td colspan=2> '
    f'<a href=https://projects.propublica.org/nonprofits/organizations/{row.EIN} '
    f' target=\"_blank\">Propublic &#8594; </a> <br>'

    f'<a href=https://www.guidestar.org/profile/{ein2}-{ein7} '
    f' target=_\"blank\"  >Guidestar &#8594;</a> <br>'

    f'<a href=https://www.causeid.com/{row.EIN}>CauseIQ </a> <br>'
    f'<a href=https://eintaxid.com/company/{row.EIN}>EIN Tax ID</a>'

    f'   </td> '
    f'</tr> '

    f'<tr> '
    f'<td> INCOME AMT:</td> <td> {row.INCOME_AMT} </td> '
    f'</tr> '
    f'</tr> '
    f'<td> NTEE:</td> <td> {row.ntee_cat} </td> '
    f'</tr> '
    f'<tr> '
    f'<td> Org Type:</td> <td> 501c({row.SUBSECTION}) {row.org_lu} </td> '
    f'</tr> '
    f'<tr> '
    f'<td> Activities:</td> <td> {row.act1_lu} </td> '
    f'</tr> '
    f'<tr> '
    f'<td> SubName:</td> <td> {row.cntysub_NAME} </td> '
    f'</tr> '

    f'<tr> '
    f'<td> Foundation Category:</td> <td> {row.found_lu} </td> '
    f'</tr> '

    f'<tr> '
    f'<td> State (Upper):</td> <td>  {legup_link} &#8594; </td> '
    f'</tr> '
    f'<tr> '
    f'<td> State (Lower):</td> <td> {leglow_link} &#8594; </td> '
    f'</tr> '
    f'<tr> '
    f'<td> Congress Dist:</td> <td> '
    f' {cong_dist_link} &#8594;'
    f'</td> '
    f'</tr> '

    f'<tr> '
    f'<td> Senate:</td> <td> '
    f' <a href=\"https://www.senate.gov/states/NY/intro.htm\" '   
    f' target=\"_blank\">Senators in NY</a> &#8594; '
    f' </td> '
    f'</tr> '

    f'<tr> '
    f'<td> Website:</td> <td> {web_url} &#8594; '
    f'  </td> '
    f'</tr> '

    f'<tr> '
    f'<td> Mission:</td> <td> {row.Mission} </td> '
    f'</tr> '
    f'<tr> '
    f'<td> Accomplishments:</td> <td> {row.ProgramSrvcAccomplishmentGrp} </td> '
    f'</tr> '
    f'<tr> '
    f'<td> Programming:</td> <td> {row.Pgm_Serv_Accomps} </td> '
    f'</tr> '

    f'</table> '
    f'</div>')


# ----- end get popup

def info_panel(np_dict):
    # st.write(np_dict)
    st.write(np_dict['NAME'])
    st.write(np_dict['STREET'])


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

def display_section(sect, df_dict, present_lu):

    sect_dict = {} # dict of list keys/fields in section

    # load a dict, key of section, to manage presentation
    for s in  present_lu:
        sect_name = present_lu[s]['display_section']
  
        if sect_name not in sect_dict:
            sect_dict[sect_name] = []

        sect_dict[sect_name].append(s)

    show_list = sect_dict[sect]

    s = ''
    tbl_html = "<hr> <table> " # class=\"my_table\">  "
    tbl_html += "<tr> "
#    tbl_html += "<tr> <td colspan=2 style=\"text-align: center; vertical-align: middle;\"> "
    tbl_html += "<tr> <td colspan=2 class=\"my_cell_section\"> "
    tbl_html +=  sect + "</td> </tr>"


    tbl_html += "<tr> "
    for s in show_list:
        
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
        if (s in df_dict 
            and df_dict[s] not in ["tag_not_found", "Tag not in file"]):  

            try:

                if present_lu[s]['format'] == 'int':   
                    tbl_html += str(int(df_dict[s])) 

                elif present_lu[s]['format'] == 'currency':    
                    val = float(df_dict[s])    
                    val_string = '${:,.0f}'.format(val)
                    tbl_html += val_string
                elif present_lu[s]['format'] == 'link':
                        tbl_html += f"<a href=\"https://{df_dict[s]}\"  target=\"_blank\" rel=\"noopener noreferrer \"> "
                        tbl_html += f"{df_dict[s]}</a> "
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
    st.html (tbl_html)



def org_basics(df_dict, present_lu):
    # tweaking to display it
    org_dict = {}
    show_list = ['NAME', 'STREET', 'CITY', 'ICO',
                    'ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT', 'GROUP',
                    'ntee_cat', 'WebsiteAddressTxt']
    
    # hm, so far can't figure an easy to way to do 
    # presentation stuff with this name-value table
    # so using html
    
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

        if present_lu[s]['format'] == 'currency':    
            val_string = '${:,.0f}'.format(df_dict[s])
            tbl_html += val_string
        elif present_lu[s]['format'] == 'link':
            tbl_html += f"<a href=\"https://{df_dict[s]}\" rel=\"noopener noreferrer dofollow\" target=\"_blank\"> "
            tbl_html += f"{df_dict[s]}</a> "
            
        else:
            tbl_html +=  str(df_dict[s])
        
        tbl_html += "</td> </tr>"
    #org_dict = df_dict.fromkeys(show_list, 0)
    # st.write(org_dict)
    
    tbl_html += "</table>"
    st.html (tbl_html)


    return org_dict

def irs_basics(df_dict):
    irs_dict = {}
    show_list = ['act1_lu', 'ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT',
                    'ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT',
                    'aff_lu', 'found_lu', 'SUBSECTION', 
                    'IRS_Form', 'Mission']
    for s in show_list:
        # st.write(df_dict[s])
        # org_dict.update(df_dict[s])  # doesn't work??
        irs_dict[s] = df_dict[s]
    #org_dict = df_dict.fromkeys(show_list, 0)
    # st.write(org_dict)
    # st.table(org_dict)
    return irs_dict


def census_basics(df_dict):
    cen_dict = {}
    show_list = ['cb_STATE', 'cb_COUNTY', 'cb_TRACT', 'cb_NAME',
                    'cong_NAME',
                    'cntysub_NAME', 'cntysub_COUSUB', 'centracts_NAME',
                    'legup_NAME', 'leglow_NAME']
    for s in show_list:
        # st.write(df_dict[s])
        # org_dict.update(df_dict[s])  # doesn't work??
        cen_dict[s] = df_dict[s]
    #org_dict = df_dict.fromkeys(show_list, 0)
    # st.write(org_dict)
    # st.table(org_dict)
    return cen_dict


def get_people(df_dict):
    
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



def get_web_srch(df_dict):
    web_dict = {}
    show_list = ['url', 'found_name', 'snippet']
    for s in show_list:
        # st.write(df_dict[s])
        # org_dict.update(df_dict[s])  # doesn't work??
        web_dict[s] = df_dict[s]
    
    return web_dict


def get_presentation_lu():
    # load present_lu used to convert data elements 
    # into human readable labels with definitions
    #TODO: merge this with processing lookup tables

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


def load_congress():
    # verify, read the json into dict
    import json
    cong_dist = open('data/congress.json') 

    # returns JSON object as  
    # a dictionary 
    cong_dict = json.load(cong_dist)
    return cong_dict



def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # can i insert css here??
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

    cong_dist = load_congress()

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
    

    present_lu = get_presentation_lu()


    # main content area
    tab1, tab2, testtab = st.tabs(["Map", "Data", "TestTabs"])


    with tab1:
        #  ----------- map -----------------------
        selected_np = ''
        (selected_np, st_map) = display_map(np_local_df, tracts_cc_gpd)
        selected_np = do_sidebar(np_local_df, selected_np, st_map)
        #TODO: when user selects from radio buttons, want to adjust map dynamically
        # https://folium.streamlit.app/dynamic_map_vs_rerender

        
        #st.write(st_map['last_object_clicked']['lat'])
        #st.write(st_map['last_object_clicked']['lon'])
        
        # update_marker(st_map, [-42, 76])

        st.write(st_map)
        
        # st_folium(st_map, center=[-42, 76])
        # st_folium(st_map, location=[42.5,-76])

        # "center":{
        # "lat":42.500453028125584
        # "lng":-76.03500366210939



    with tab2:
        # ----- info -----------------------------
        st.write("Info Panel")
        st.write(selected_np)

        # get detailed on selected np, lookup by name for now    
        filt = np_local_df['NAME'] == selected_np

        # st.write(np_local_df.loc[filt].T)

        # convert to dict 
        # https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
        df_dict = np_local_df.loc[filt].to_dict('records')[0]


        org, cat1, cat2 = st.columns(3)
        with org:
            st.header('Org Basics')
            st.subheader('subheader')
            st.write ('-- using st table with dict')
            
            st.table(df_dict)

        with cat1:
            st.header('cat1')
            st.subheader('subheader ')
            st.write("---using write dict --- ")
            st.write(df_dict)

        with cat2:
            st.header('cat2')
            st.subheader('subheader')
            
            show_list = ['NAME', 'STREET', 'CITY', 'ICO',
                         'ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT',
                         'ntee_cat', 'GROUP', 'SUBSECTION']
            for s in show_list:
                #disp_title = present_lu[fld]
                #st.write(df_dict[s])

                #TODO: could use tags for datasource, present_lu[s][0]                
                h = "Definition: " + present_lu[s]['help'] + "(data source: " + present_lu[s]['source'] + ")"
                st.markdown(present_lu[s]['display_name'], help=h)   
                 
                st.write (df_dict[s])
                #st.write (help=present_lu[s][5])


        st.divider()
        st.write ("now two columns")


        left_column, right_column = st.columns(2, gap="small", 
                                               vertical_alignment="top")
        
        
        with left_column:
            left_content = "<table border=1> "
            left_content += "<tr> <td colspan=2> using html </td> </tr>"
            left_content += "<tr>  "
            left_content += "    <td> street: </td> "
            left_content += f"    <td> {df_dict['STREET']} </td>"
            left_content += "</tr> "
            left_content += "<tr> <td> city </td> "
            left_content += f"<td> {df_dict['CITY']}</td>"
            left_content += "</tr> "
            left_content += "</table> "
            # st.write(left_content)
            st.html(left_content)
        


        with right_column:
            right_content = (
                f'<!-- table class="table table-striped table-hover table-condensed table-responsive"-->'
                f'<table class="table table-striped table-hover table-condensed table-responsive">'
                f'<tr> '
                f"<td> Name:</td> <td>  {df_dict['NAME']} </td> "
                f"</tr> "
                f"<tr> "
                f"<td> Post Addr:</td> <td> {df_dict['STREET']}, {df_dict['CITY']} {df_dict['ZIP']}</td> "
                f"</tr> "
                f'<tr> '
                f'<td> IRS Contact:</td> <td> {df_dict['ICO']} </td> '
                f'</tr> '

                f'<tr> '
                f'<td> EIN:</td> <td> {df_dict['EIN']} </td> '
                f'</tr> '
                f'<tr> '
                f'<td> Subsection </td>'
                f'<td> 501c({df_dict['SUBSECTION']}) </td>'
                f'</tr> ' 
                              
                f'</table>'
                )
        
                #ASSET_AMT	438205.0
                #INCOME_AMT	74274.0
                #REVENUE_AMT	74274.0


        
            st.html(right_content)
                
        st.write(df_dict['NAME'] )

        url = "https://www.streamlit.io"
        link_title = df_dict['NAME']

        #writing a url 
        st.write(f"[{link_title}](%s)" % url)

 
    with testtab:
        st.write("test tab")
        st.subheader("Org Basics")
        #st.table(org_basics(df_dict, present_lu))
        
        # have org basics display it
        org_basics(df_dict, present_lu)
        
        # general approach to printed by section from presentation lookup
        display_section('Form 990x', df_dict, present_lu)

        # general approach to printed by section from presentation lookup
        display_section('Census', df_dict, present_lu)



        st.subheader("Data from IRS Tax Form (990, 990EZ)")
        st.table(irs_basics(df_dict))

        st.subheader("Census Geocoding")
        st.table(census_basics(df_dict))


        st.subheader("People listed on IRS Tax Form")
        st.table(get_people(df_dict))

        st.subheader("Web Search")
        st.table(get_web_srch(df_dict))


if __name__ == "__main__":
    main()
    
