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
import folium  
from streamlit_folium import st_folium
import geopandas as gpd
import math
from folium.features import DivIcon  #TODO: move import


import csv
import re
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


def radio_change():
    st.sidebar.write('hit radio change ')

    np_radio_change = str(st.session_state['np_radio'])

    st.session_state['app_actions'].append("User Changed Radio Button to " + np_radio_change)
    
    st.sidebar.write (st.session_state['np_radio'])
    st.session_state['np_df_selected_index'] = np_radio_change
    # st.rerun()



def do_sidebar (np_local_df, np_df_selected_index):
    """ Build Sidebar 
    
    Parameters:
    df (dataframe):             np_local_df, all nonprofit data
    np_df_selected_index (int):   selected index of dataframe
                                (radio button is zero-indexed, 1 less then df index)

    """

    add_to_debug = "\n ##### do sidebar "

    add_to_debug += "\n (status of index, passed, session?)"

    if 'np_df_selected_index' in st.session_state:
        add_to_debug += "\n - Sidebar: Arr in sidebar session np df select ind: " + str(st.session_state['np_df_selected_index'])

    elif pd.isna(np_df_selected_index):
        add_to_debug += "\n - Arr sidebar pd null select ind passed from map -  set to 1"
        np_df_selected_index = 1
    elif math.isnan(np_df_selected_index):
        add_to_debug += "\n -Arr sidebar math isnan np select passed from map -  set to 1" 
        np_df_selected_index = 1
    else:
        add_to_debug += "\n - Arr sidebar passed " + str(np_df_selected_index)

    if not np_df_selected_index:
        add_to_debug += "\n - Arr sidebar not np select -- set to 1"
        np_df_selected_index = 1

    if np_df_selected_index == '':
        add_to_debug += "\n - Arr sidebar np select two single quotes -- set to 1"
        np_df_selected_index = 1

    add_to_debug += "\n - Arr sidebar np select passed:" + str(np_df_selected_index)
    

    np_df_selected_index = int(np_df_selected_index)

    with st.sidebar:

        nonprofits_tab, selected_tab, help_tab, status_tab = st.tabs(["Nonprofits", "Selected", "Help", "Status"])

        with nonprofits_tab:
            
            if 'np_dict' in st.session_state:
                np_dict = st.session_state['np_dict']
            else:
                st.write ("Error: no_dict not in session state")                    

            # if np_df_selected_index is 0, it means map didn't have selection
            if np_df_selected_index == 0:
                np_radio_index = 1
            else:
                np_radio_index = np_df_selected_index - 1


            np_df_selected_index = st.radio("Select a Nonprofit", options=np_dict.keys(), 
                                    format_func=lambda x: "(" + str(x) + ") " + np_dict[x],
                                    index=np_radio_index, on_change=radio_change,
                                    key='np_radio')

            
            # , help="help"

            if np_df_selected_index:
                add_to_debug += "\n - Sidebar: np_def_sel exists " # + str(np_df_selected_index)
            else:
                add_to_debug += "\n - Sidebar: np_def_sel NOT exists, set to 1"
                np_df_selected_index = 1
                                
                            #on_change=None, args=None, kwargs=None, *, 
                            # disabled=False, horizontal=False, captions=None, label_visibility="visible")

            st.session_state['np_df_selected_index'] = np_df_selected_index 

            # xxx TODO: check whether this is required
            #if 'last_object_clicked_tooltip' in m:
            #    st.write ("last map click:  ",  m['last_object_clicked_tooltip'])
            #    st.write ("radio select:  ", np_df_selected_index)
            #else:
            #    st.write("no m")

    with selected_tab:
        st.header("Selected")
        # st.write(np_df_selected_index)

        st.write (np_local_df.filter(items=[np_df_selected_index], axis=0).T)

    with help_tab:
        st.write ('help')

        st.write("Where is data from how to use, etc")

        st.write(f"Number of Nonprofits: {st.session_state.num_rows}")
        st.write(f"Data Elements for each Nonprofit: {st.session_state.num_facts}")


    with status_tab:
        st.write ('status - debugging')

    return np_df_selected_index, add_to_debug



#TODO: don't need df, yes?
def get_map_popup(row, df) :
    """ Returns HTML for map popup when user clicks on a Nonprofit """

    #TODO: remove, obsolete
    # st.session_state['selected_np'] = row.NAME

    return (f'<div>'
    f'<table class="table table-striped table-hover table-condensed table-responsive">'
    f'<tr> '
    f"<td> Name:</td> <td>  {row.NAME} </td> "
    f'</tr> '
    f'<tr> '
    f"<td> Post Addr:</td> <td> {row.STREET}, {row.CITY} </td> "
    f'</tr> </table>')

# ----- end get popup

    
def number_DivIcon(color,number):
    """ Create an icon with number of marker outline with circle

    Parameters:
        color(str): 
        number(): what number

    Return:  icon

    """
    from folium.features import DivIcon
    
    html_o=f"""<span class="fa-stack " style="font-size: 12pt" >
            <!-- The icon that will wrap the number -->
            <span class="fa fa-circle-o fa-stack-2x" style="color : {color}"></span>
            <!-- a strong element with the custom content, in this case a number -->
            <strong class="fa-stack-1x">
                    {number}  
            </strong>
        </span>"""


    html_1=f"""
            <div style="border-style: solid; 
                border-width: 1px; 
                border-radius: 10px; 
                display: inline-block;
                background-color: {color};
                ">
                <span>
                <strong> {number} </strong>
                </span>
            </div>
        """


    html_2=f'''<!-- span class="fa-stack" prefix="fa" style="font-size: 12pt"-->
                    <span class="fa-stack" prefix="fa" style="border: 1px; font-size: 12pt">
                    <!-- The icon that will wrap the number -->
                    <span class="fa-circle-o fa-stack-2x" prefix="fa" style="color : {color}"></span>
                    <!-- a strong element with the custom content, in this case a number -->
                    <strong class="fa-stack-1x" prefix="fa">
                         {number}  
                    </strong>
                </span>'''

    icon = DivIcon(        
            icon_size=(30,30),
            icon_anchor=(30,30),
            html=html_1          
        )
    return icon

def update_selected_marker(np_df_selected_index):
    """ update selected marker in sessions """

    add_debug = "\n ###### In updated selected marker  "
    add_debug += "\n - passed np_df_sel..." + str(np_df_selected_index)

    

    # np_df_selected_index = 2
    
    if np_df_selected_index in st.session_state:
        np_df_selected_index = st.session_state['np_df_selected_index']
        add_debug += "\n - got from session state " + str(np_df_selected_index)
        
    elif np_df_selected_index == None:
        add_debug += "\n - um, None, so set to 1"
        np_df_selected_index = 1
    #elif math.isnan(np_df_selected_index):
    #    add_debug += "\n -not a number na by math"
    elif np_df_selected_index == '':
        add_debug += "\n - np df sel is empty, set to 1"
        np_df_selected_index = 1
    
    else:
        add_debug += "\n - " + str(np_df_selected_index)

    marker_index = np_df_selected_index - 1
    # st.write ("this one: ", marker_index)
    st.session_state["markers"][marker_index] = folium.Marker([422, -76.2],    
                icon= number_DivIcon(" #fff6f1", "HEY"),
            #popup= folium.Popup(pop_msg, max_width=300), 
            tooltip = "added one")
    
    return add_debug 

def load_markers(np_local_df, tracts_cc_gpd, np_df_selected_index):
    """ loading markers into session """

    add_to_debug = "\n ##### in Load Markers "

    st.session_state['app_actions'].append("load markers")

    # Initialize markers inside of session state
    if "markers" not in st.session_state:
        st.session_state["markers"] = []

    if 'np_df_selected_index' in st.session_state:
        np_df_selected_index = st.session_state['np_df_selected_index']


    colocated_markers = {}
    
    num = 0
    
    #nps2 = folium.FeatureGroup(name="NPs")
    #addme = folium.FeatureGroup(name="addme")
    #colocated = folium.FeatureGroup(name="Colocated")

    orgs_no_address = []

    #TODO: no longer need this work around
    ein_to_present_num = {}  # temp workaround

    for index, row in np_local_df.sort_values('NAME').iterrows():
        num = index
        present_num = "(" + str(num) + ") "
        
        #if num == np_df_selected_index:
        if num == 5:
            color="#FF00AA"
        else:
            color=""


        #TODO: ugh, temp workaround to map each co-located ein to a NP number
        ein_str = str(row.EIN)
        ein_to_present_num[ein_str] = present_num

        if not math.isnan(row['coord_x']):  # the data has po boxes with no lat long
            if (row.cluster_ind == 0):  # it's not a cluster

                pop_msg = present_num +  row.NAME 
                pop_msg += "<br>" + row.STREET
                pop_msg += "<br> x: " + str(row.coord_x) +  "<br>  y:  " + str(row.coord_y) 

                st.session_state["markers"].append(folium.Marker(
                    location=[  row['coord_y'], row['coord_x'] ],
                    icon= number_DivIcon(color,num),
                    popup= folium.Popup(pop_msg, max_width=300), 
                    tooltip = present_num + row.NAME
                ))
            else:
                # save aside info about co-located or close orgs
                ngroup = str(int(row.cluster_ngroup))
                if ngroup not in colocated_markers:
                    colocated_markers[ngroup] = [] 

                #TODO: investigate this data structure 
                colocated_markers[ngroup].append(row) 
                
        else:
            orgs_no_address.append([index, row.NAME, row.STREET])

    #"""
    for mark_group in colocated_markers:        
        num_markers = str(len( colocated_markers[mark_group]))
        pop_msg = num_markers + " NPs at same or close location " 
        tool_msg = num_markers + " NPs at same or close location "

        #  lat/lng for cluster marker
        lat = colocated_markers[mark_group][0]['cluster_lat']
        lng = colocated_markers[mark_group][0]['cluster_lng']
        mark_loc = [lat, lng]

        for mark_row in colocated_markers[mark_group]:
            present_num = ein_to_present_num[str(mark_row.EIN)]
            pop_msg += f" <P> {present_num} {mark_row.NAME} <br>"
            pop_msg += f"{mark_row.STREET}  </P>"
    
            tool_msg += f" <br> {present_num} {mark_row.NAME }"

            st.session_state["markers"].append(folium.Marker(mark_loc,    
                     icon= number_DivIcon(" #fff6f1", "M"),
                    popup= folium.Popup(pop_msg, max_width=300), 
                    tooltip = tool_msg
                ))
        
        # """

    return  add_to_debug

def do_map(np_df_selected_index):
    add_debug = "\n ##### Arr do map " 
    add_debug += "\n - np_df_sel passed " + str(np_df_selected_index)

    m2 = folium.Map(
        location=[42.54043355305221,-76.1342239379883],
        zoom_start=11,
        key="my_np_map"
    )
    if 'np_df_selected_index' in st.session_state:
        np_df_selected_index = int(st.session_state['np_df_selected_index'])
        add_debug += "\n - np_sel_ is session " + str(st.session_state['np_df_selected_index'])
    else:
        add_debug += "\n - Um, not in session so setting to 1"
        np_df_selected_index = 1

    fg = folium.FeatureGroup(name="Markers")
    t_fg = folium.FeatureGroup(name="Test Add")

    for marker in st.session_state["markers"]:
        fg.add_child(marker)

    #for marker_index, marker in enumerate(st.session_state["markers"]):
    #    fg.add_child(marker)

    # render map, save data to st_m2    
    st_m2 = st_folium(
        m2,
        # center=st.session_state["center"],
        zoom=11,
        key="new",
        feature_group_to_add=fg,
        height=550,
        width=700
    )



    st.session_state['app_actions'].append("Rendered Map from session")

    if st_m2['last_object_clicked_tooltip']:
        add_debug += "\n - do_map:  st_m2 tooltip returned " + st_m2['last_object_clicked_tooltip']

        # get the tooltip to know which NP was selected
        #add_debug += "\n - Do Map Session Toolip " + st.session_state["last_object_clicked_tooltip"]
        selected_np_tooltip =  st_m2["last_object_clicked_tooltip"]
        
        # extract the key from parantheses 
        np_df_selected_index = selected_np_tooltip[selected_np_tooltip.find("(")+1:selected_np_tooltip.find(")")]
        add_debug += "\n - Do Map: Toolip  map click: " + selected_np_tooltip
        add_debug += "\n - Do Map: Extracted Index: " + str(np_df_selected_index)


    return st_m2, np_df_selected_index, add_debug


def display_map_new(np_local_df, tracts_cc_gpd, np_df_selected_index):
    """ redoing map 
    
    adding numbers for markers
    dealing with close and co-located orgs

    Returns:
        st_m2, np_df_selected_index
    """
    
    add_debug = "\n ##### display map new "

    # is there a selected nonprofit?
    
    add_debug += "\n - Disp Map: passed np df... " + str(np_df_selected_index)
    
    # check session state 
    if 'np_df_selected_index' in st.session_state:
        if np_df_selected_index != st.session_state['np_df_selected_index']:
            add_debug += "\n - Disp Map: session index different from passed"

        np_df_selected_index = st.session_state['np_df_selected_index']
        add_debug += "\n - map new: np sel in session " + str(np_df_selected_index)


    colocated_markers = {}
    
    num = 0
    m2 = folium.Map(
        location=[42.54043355305221,-76.1342239379883],
        zoom_start=11,
        key="my_np_map"
    )
    
    nps2 = folium.FeatureGroup(name="NPs")
    addme = folium.FeatureGroup(name="addme")
    colocated = folium.FeatureGroup(name="Colocated")

    orgs_no_address = []

    #TODO: no longer need this work around
    ein_to_present_num = {}  # temp workaround

    for index, row in np_local_df.sort_values('NAME').iterrows():
        num = index
        present_num = "(" + str(num) + ") "
        if num == np_df_selected_index:
            color="#FF00AA"
        else:
            color=""

        #TODO: ugh, temp workaround to map each co-located ein to a NP number
        ein_str = str(row.EIN)
        ein_to_present_num[ein_str] = present_num

        if not math.isnan(row['coord_x']):  # the data has po boxes with no lat long
            if (row.cluster_ind == 0):  # it's not a cluster

                pop_msg = present_num +  row.NAME 
                pop_msg += "<br>" + row.STREET
                pop_msg += "<br> x: " + str(row.coord_x) +  "<br>  y:  " + str(row.coord_y) 

                folium.Marker(
                    location=[  row['coord_y'], row['coord_x'] ],
                    icon= number_DivIcon(color,num),
                    popup= folium.Popup(pop_msg, max_width=300), 
                    tooltip = present_num + row.NAME
                ).add_to(nps2)
            else:
                # save aside info about co-located or close orgs
                ngroup = str(int(row.cluster_ngroup))
                if ngroup not in colocated_markers:
                    colocated_markers[ngroup] = [] 

                #TODO: investigate this data structure 
                colocated_markers[ngroup].append(row) 
                
        else:
            orgs_no_address.append([index, row.NAME, row.STREET])

    #"""
    for mark_group in colocated_markers:        
        num_markers = str(len( colocated_markers[mark_group]))
        pop_msg = num_markers + " NPs at same or close location " 
        tool_msg = num_markers + " NPs at same or close location "

        #  lat/lng for cluster marker
        lat = colocated_markers[mark_group][0]['cluster_lat']
        lng = colocated_markers[mark_group][0]['cluster_lng']
        mark_loc = [lat, lng]


        for mark_row in colocated_markers[mark_group]:
            present_num = ein_to_present_num[str(mark_row.EIN)]
            pop_msg += f" <P> {present_num} {mark_row.NAME} <br>"
            pop_msg += f"{mark_row.STREET}  </P>"
    
            tool_msg += f" <br> {present_num} {mark_row.NAME }"

        folium.Marker(mark_loc,    
                     icon= number_DivIcon(" #fff6f1", "M"),
                    popup= folium.Popup(pop_msg, max_width=300), 
                    tooltip = tool_msg

                ).add_to(colocated)
        
        # """

    m2.add_child(nps2)
    m2.add_child(addme)
    m2.add_child(colocated)

    folium.LayerControl(collapsed=False).add_to(m2)
   
    # call to render Folium map in Streamlit
    st_m2 = st_folium(m2, width=725)
    st.session_state['app_actions'].append("Rendered Map")

    #  st.markdown("#### Orgs with address that didn't **geocode**")
    #  st.table(orgs_no_address)

    if 'last_object_clicked_tooltip' in st_m2:
        add_debug += "\n - last obj tt in st_mt"
        if st_m2["last_object_clicked_tooltip"]:
            add_debug += "\n - st_m2 has tooltip has val:  " +  st_m2["last_object_clicked_tooltip"]
        else:
            add_debug += "\n - st_m2 has tooltip has NO val "

    # selected_np_index = 0
    if st_m2['last_active_drawing']:
        # get the tooltip to know which NP was selected
        add_debug += "\n - Disp Map: st_m2 has last active drawing"
        selected_np_option =  st_m2["last_object_clicked_tooltip"]
        
        # extract the key from parantheses 
        map_selected_index = selected_np_option[selected_np_option.find("(")+1:selected_np_option.find(")")]
        add_debug += "\n - Disp Map: In Map, last active drawing:  selected np in map click: " + selected_np_option
        add_debug += "\n - Disp Map: map selected np index in map click: " + str(map_selected_index)


        # did user click map
        if map_selected_index != np_df_selected_index:
            add_debug += "\n - Disp Map: Map selected different"
            add_debug += "\n - REDRAW here..."
            
            
            add_debug += "\n - saving new np_df... "
            np_df_selected_index = map_selected_index
            st.session_state['np_df_selected_index'] = np_df_selected_index
            #st_m2 = st_folium(m2, zoom=9, width=725)

            #st_m2 = st_folium(m2,
            #    center=[42.55856083073203, -76.2084771200659],
            #    zoom=8
            #)


            st.rerun()


    else:
        add_debug += "\n - st_m2 last active drawing NO val  "
        # but did user click radio button 


        #if st.session_state['np_radio'] != np_df_selected_index:
        #    add_debug += "\n - Disp Map:  radio does not equal map received index"



        # when user clicks on map value is passed to radio and tabs updated
        # but map doesn't update -- not sure what triggers a rerun
        # if user simply moves map, a rerun is triggered, adding the highlight to selected marker
        # experiment to force rerun on clicking on map...
        
        #st.rerun(*, scope="app")
        # st.rerun(scope="fragment")

        # st.session_state['selected_np'] = selected_np #hm, just in case

    return st_m2, np_df_selected_index, add_debug


#TODO: remove after salvage
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
                fill=True,
                # color = '#4cdc7c',
                highlight= True,                
                popup=folium.Popup(get_map_popup(row, np_local_df), max_width=300),
                tooltip = row.NAME,
                #radius=15,
                # fill_color="#3db7e4"
                ).add_to(nps)

    folium.LayerControl().add_to(m)


    st_map  = st_folium(m, 
                        width=700) #, returned_objects=["last_object_clicked"])
    
        
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
    url = f"https://projects.propublica.org/nonprofits/organizations/{df_dict['EIN']}"
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
    #TODO: fix people json during data processing 
    # um, irs xml seems to have non-compliant json 
         
    import json

    # the irs data uses single quote in json
    # and in person name
    # "KATHLEEN O'CONNELL"
    # import re

    ppl = df_dict['people']
        
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


@st.cache_data
def get_present_lu():
    """ load present_lu, presentation lookups dict, used to present consistent labels 
    
    Returns:
        present_lu(dict): presentation lookup

    """
    #TODO: merge this with processing lookup tables?

    #TODO: Move import statements
    #import csv

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


@st.cache_data
def get_np_local_df():
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

    # get nonprofit data, then setup incremental index
    np_local_df = pd.read_csv('data/np_local_df.csv')
    np_local_df.sort_values(by=['NAME'], inplace=True)
    np_local_df.reset_index(drop=True, inplace=True)

    # start index at 1 for humans, when matching org to map number
    np_local_df.index += 1

    return np_local_df

@st.cache_data
def get_np_dict(np_local_df):
    """  
    Creates dictionary with org index number and org name.

    Parameters: 
        np_local_df (dataframe): dataframe with all the NP Info

    Returns: 
        np_dict(dict):  
    
    """
    
    options = np_local_df.index.values.tolist()
    np_names = np_local_df['NAME'].values.tolist()
    #np_dict = dict(zip(options, np_names))

    return dict(zip(options, np_names))

@st.cache_data
def get_tracts_shape():
    # tracts for new york, filter to cortland county
    tracts_gpd = gpd.read_file('data/tl_2022_36_tract.shp')
    tracts_cc_gpd = tracts_gpd[tracts_gpd['COUNTYFP'] == '023']

    return tracts_cc_gpd

def get_css_style():
    my_css = ''' 
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

    return my_css

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # setup styles for used in HTML tables of data and tooltips
    
    debug_msg = "#### starting main"
    css_table = get_css_style()
    st.markdown (css_table, unsafe_allow_html=True)
    debug_msg += "\n - Main: got and printed css"
    
    # load data
    
    # pre-processed in google colab
    # doesn't change, so put into streamlit cache

    debug_msg += "\n - Main: load cache data"
    # populate dataframe of local NPs and put into streamlit cache
    np_local_df = get_np_local_df()

    # create dictionary with index and org name for radio selection 
    np_dict = get_np_dict(np_local_df)

    # tracts for new york, filter to cortland county
    tracts_cc_gpd = get_tracts_shape()

    # Load presentation dictionary with human-readable labels, definitions
    # and control groupings/collections to present
    present_lu = get_present_lu()


    # Initialize session data

    if 'np_df_selected_index' in st.session_state:
        np_df_selected_index = int(st.session_state['np_df_selected_index'])
        debug_msg += "\n - Main:  Init, index in session: " + str(np_df_selected_index)
    else:
        np_df_selected_index = 1
        debug_msg += "\n - Main: Init, index NOT in session, set to 1, saved to session"
        st.session_state['np_df_selected_index'] = np_df_selected_index
    

    debug_msg += "\n - Main: confirm index in Session: " + str(st.session_state['np_df_selected_index'])


    #TODO: review - probably doesn't need session state 
    st.session_state['np_dict'] = np_dict

    #TODO: remove this, new plumbing
    #TODO: check-why put in session state? just put in sidebar?
    if 'np_list' not in st.session_state:
        np_list = list(np_local_df['NAME'])
        np_list.sort()
        st.session_state['np_list'] = np_list

    if 'num_nps' not in st.session_state:
        (num_rows, num_facts) = np_local_df.shape
        st.session_state['num_rows'] = num_rows
        st.session_state['num_facts'] = num_facts

    
    if 'app_actions' not in st.session_state:
        st.session_state['app_actions'] = []
        st.session_state['app_actions'].append('Create app_actions')

    st.session_state['app_actions'].append('Running_main')


    # ----- was the map just clicked?

    if "last_object_clicked" not in st.session_state:
        st.session_state["last_object_clicked"] = None
        debug_msg += "\n - Main: last object clicked set to None in session"



    # ---- main content area, tabs ----------------
    map_tab, sum_tab, all_tab, graph_tests = st.tabs(["Map", "Organization Info", 
                                                        "All Data Elements", "Graph Tests"]
                                                        )

    with map_tab:
        #  ----------- map -----------------------
        
        debug_msg += "\n - Main: map tab, start"        
        
      
        if 'np_radio' in st.session_state:
            debug_msg += "\n - Main: map tab, Radio in session " + str(st.session_state ['np_radio'])

        #if 'markers' not in st.session_state:
        #    add_debug = load_markers(np_local_df, tracts_cc_gpd, 4)
        #    debug_msg += "\n - loaded markers into session"
        #else:
        #    debug_msg += "\n - markers in session "
        #    add_debug = update_selected_marker(np_df_selected_index)
        #    debug_msg += add_debug

        debug_msg += "\n - Main: map tab, index: " + str(np_df_selected_index)

        debug_msg += "\n - Main: map tab, go do map"
        #(st_m2, np_df_selected_index, add_debug) = do_map(np_df_selected_index)
        #debug_msg += add_debug

        (st_m2, np_df_selected_index, add_debug ) = display_map_new(np_local_df, tracts_cc_gpd, np_df_selected_index)
        debug_msg += add_debug
        debug_msg += "\n - Main: map new returned index "+ str(np_df_selected_index)

        # (st_m2, np_df_selected_index, add_debug ) = display_map_new(np_local_df, tracts_cc_gpd, np_df_selected_index)
        
        
        #if st_m2['last_object_clicked_tooltip']:
        #    debug_msg += "\n - HEY tooltip returned " + st_m2['last_object_clicked_tooltip']

        debug_msg += "\n - Main: map tab, now go do sidebar"
        # selected_np = do_sidebar(np_local_df, selected_np, st_map)
        (np_df_selected_index, add_debug) = do_sidebar(np_local_df, np_df_selected_index)
        debug_msg += add_debug

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
        debug_msg += "\n - Main: sum_tab, start with index: " + str(np_df_selected_index)
        # get detailed on selected np by index 

        # convert the selected nonprofit to dict 
        # https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
        #df_dict = np_local_df.loc[filt].to_dict('records')[0]

        df_dict = np_local_df.filter(items=[np_df_selected_index], axis=0).to_dict('records')[0]
        #st.table(df_dict)

        st.subheader("(" + str(np_df_selected_index) + ") "  + df_dict['NAME'])


        #TODO: Could Add iteration - list of sections 
        #eg sects_to_show = ['IRS Business Master File', 'Form 990x', 'Staff and Board']
        
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

        #st.subheader(selected_np)
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
        # st.subheader(selected_np)
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

    # -------------  end of tabs of main content area --------------

    # test check for click as it would have to redraw map??
    
    
    if 'last_object_clicked_tooltip' in st.session_state:
        # st_m2: #  and st_m2['last_active_drawing']:
        debug_msg += "\n - Main:  last_object_clicked_tooltip in session"
        # get the tooltip to know which NP was selected
        debug_msg += "\n - " + st.session_state["last_object_clicked_tooltip"]
        selected_np_tooltip =  st_m2["last_object_clicked_tooltip"]
        
        # extract the key from parantheses 
        np_df_selected_index = selected_np_tooltip[selected_np_tooltip.find("(")+1:selected_np_tooltip.find(")")]
        debug_msg += "\n - Main: Toolip  map click: " + selected_np_tooltip
        debug_msg += "\n - Main: Extracted Index: " + str(np_df_selected_index)

        # end test


    if 1 == 0:
        debug_msg += "\n ##### end main  "
        st.markdown(debug_msg)

        # see session state at end of application
        st.write("-- Selected session state at main end -- ")
        sess_vars=['np_radio', 'np_df_selected_index']
        for sess_var in sess_vars:
            if sess_var in st.session_state:
                st.write(sess_var, st.session_state[sess_var])
            else:
                st.write(sess_var + " : Not in Session")


        st.write(st.session_state['app_actions'])

        st.write ("--- Bottom of main, writing out st_m2 --- ")
        if st_m2:
            st.write ("st_m2, map exists")
            if 'last_object_clicked' in st_m2:
                st.write ('last_object_clicked', st_m2['last_object_clicked'])
                st.write ('last_object_clicked_tooltip', st_m2['last_object_clicked_tooltip'])


        st.write("-- all session state at main end -- ")
        for ss in st.session_state:
            st.write(ss, st.session_state[ss])




if __name__ == "__main__":
    main()
    
