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
from datetime import datetime
import urllib.parse

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
VERS = '03_01'
VERS_DESC = 'Updating dataframes'

def radio_change():
    """ callback after list of NPs in left panel is updated """

    my_log("Sidebar: Radio Change def entered")

    np_radio_change = str(st.session_state['np_radio'])
    
    st.session_state['np_df_selected_index'] = np_radio_change
    my_log("User Change saved to session, index: " + np_radio_change)


def do_sidebar (np_local_df, np_df_selected_index):
    """ Build Sidebar 
    
    Parameters:
    df (dataframe):             np_local_df, all nonprofit data
    np_df_selected_index (int):   selected index of dataframe
                                (radio button is zero-indexed, 1 less then df index)

    """
    my_log("Sidebar: entered")

    #TODO: cleanup these dev details like controlling dtypes
    if 'np_df_selected_index' in st.session_state:
        my_log("Sidebar: Arr in sidebar session np df select ind: " + str(st.session_state['np_df_selected_index']))
    elif pd.isna(np_df_selected_index):
        np_df_selected_index = 1
    elif math.isnan(np_df_selected_index):
        np_df_selected_index = 1
    

    if not np_df_selected_index:
        np_df_selected_index = 1

    if np_df_selected_index == '':
        np_df_selected_index = 1

    my_log("Arr sidebar np select passed:" + str(np_df_selected_index))
    
    np_df_selected_index = int(np_df_selected_index)

    my_log("Sidebar: using index: " + str(np_df_selected_index))


    with st.sidebar:

        nonprofits_tab, selected_tab, help_tab, status_tab = st.tabs(["Nonprofits", "Selected", "Help", "Status"])

        with nonprofits_tab:
            my_log("Sidebar: Nonprofits tab, entered")
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
            
            if not np_df_selected_index:
                np_df_selected_index = 1

            st.session_state['np_df_selected_index'] = np_df_selected_index 

        with selected_tab:
            my_log("Sidebar: Selected tab, entered")
            st.header("Selected")

            st.write (np_local_df.filter(items=[np_df_selected_index], axis=0).T)

        with help_tab:
            my_log("Sidebar: Help tab, entered")

            help_summary_md = """
            #### About 
            This is a drafty fun project to learn about local community, especially
            the nonprofit sector.     
             
            #### How to Use
            Select a nonprofit in sidebar or on map and gets lots of data. 
            Launch explorations of other data sources, mostly via the Explore section.

            #### Data Sources 
            Data from multiple sources was processed using Google Colab.  
            - IRS BUsiness Master File
            - IRS tax returns (Form 990-series)
            - Bing web search (api) (free tier)
            - US Census (api)
            - US Congress (api)

            #### External Links
            Holy cow, there's lots of info available.
            With basic geographic info ("geocoding" from US Census), charts from other information sources
            are embedded and linked.
            
            #### Github
            All code and google colab notebooks are available on [Gitub](https://github.com/johnzelson/local-nonprofits.git)

            My original goal was just for personal learning, but it's hard to not see diverse
            possibilities from layering data sources into an easily havigable interface.  If some 
            other human comes across this:  please improve the draft :)

            One could use such a tool for grant-writing, finding collaborators, identifying
            local needs, finding places to volunteer, or just satisfying curiosity.

            #### Additional Background
            [Local Nonprofits](https://www.johnzelson.org/)

            #### Similar Projects
            - Giving Tuesday
            - IRSx

            """
            st.markdown(help_summary_md)

            st.write(f"Number of Nonprofits: {st.session_state.num_rows}")
            st.write(f"Data Elements for each Nonprofit: {st.session_state.num_facts}")


        with status_tab:
            my_log("Sidebar: Status tab, entered")
            st.write ('status - debugging')

            st.text_area("debug", value="", height=20, key="debug_info", 
                         )


    my_log("Sidebar: Ending, return index: " + str(np_df_selected_index))
    return np_df_selected_index

    
def number_DivIcon(color,number):
    """ Create an icon with number of marker outline with circle

    Parameters:
        color(str): 
        number(str): what text topresent on marker

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


#test of using @st.fragment
def display_map(np_local_df, tracts_cc_gpd, np_df_selected_index):
    """ Map with Nonprofit Markers
    
    Parameters:
        np_local_df (dataframe):  Nonprofits in dataset
        tracts_cc_gpd (geopandas dataframe):  cortland co., NY tract shapefiles from census
        np_df_selected_index (int):  index of currently selected NP
    
    Returns:
        st_m2 (map dictionary):  streamlit map output
        np_df_selected_index (int): index of NP if user selects from map
        redraw (bool): indicates user has clicked on marker, so map needs to be udpated

    """
    my_log("Disp Map: entered")
    

    redraw = False  
    # Note: setting redraw is one approach for flagging scenario where
    #       map is rendered, user clicks on a nonprofit, and map needs to be updated.
    #       It feels clunky.  
    #       
    #       https://github.com/randyzwitch/streamlit-folium.git
    #       Needs work getting smooth/dynamic map updates and updating sidebar/tabs
    
    #TODO: Review logic of passed vs session np_df_selected_index
    #TODO: then, remove debugging/logging 

    # Main should always pass np_df_selected_index, but checking 
        
    if 'np_df_selected_index' in st.session_state:
        
        if np_df_selected_index != st.session_state['np_df_selected_index']:
            my_log("Disp Map: session index different from passed")

        np_df_selected_index = st.session_state['np_df_selected_index']
        my_log("Disp Map new: np sel in session " + str(np_df_selected_index))

    # np_list is a quick list of alpha sorted nonprofits
    if 'np_list' in st.session_state:
        np_list = st.session_state['np_list']


    # TODO: review when df_dict gets created.  inefficient to recreate df_dict here, again
    df_dict = np_local_df.filter(items=[int(np_df_selected_index)], axis=0).to_dict('records')[0]


    #TODO:  review where np_df_selected_index is read from session, etc.  should always be integer
    
    # setup org num and name
    np_display_nbr = "(" + str(np_df_selected_index) + ") " 
    np_list_index = int(np_df_selected_index) - 1
    np_org_name = np_list[np_list_index]

    # setup link to a google map
    google_map_base = 'https://www.google.com/maps/search/?'
    params = {'api': '1', 
          'query': df_dict['STREET'] + ", " + df_dict['CITY'] + ", " + df_dict['STATE'] + " " + df_dict['ZIP']
          }
    g_url =  google_map_base + urllib.parse.urlencode(params)
    google_link = f"<a href=\"{g_url}\" target=\"_blank\">Google Map Search &#8594;</a>"


    # catch when there is no geocode/address, create appropriate google map search 
    if pd.isnull(df_dict['coord_x']):
        st.write (np_display_nbr + np_org_name )
        st.write ("This organization address could not be geocoded.  ")

        # Census geocoder does not recognize PO Boxes and some adresses 
        # eg. College Campus Addresses.  Google seeme to find campus addresses 
        # if address is PO Box, then only use org name in query.
        # otherwise use address. 

        if df_dict['STREET'].startswith("PO"):
           params = {'api': '1', 
                    'query': df_dict['NAME'] + ", " + df_dict['CITY'] + ", " + df_dict['STATE'] + " " + df_dict['ZIP']
          } 

        g_url =  google_map_base + urllib.parse.urlencode(params)
        google_link = f"<a href=\"{g_url}\" target=\"_blank\">Google Map Search &#8594;</a>"

        # st.write("Try a google Search: ")
        st.markdown("Try a " + google_link, unsafe_allow_html=True)

        # no address to map, so just return without drawing
        return '', np_df_selected_index, redraw
    else:
        st.markdown(np_display_nbr + np_org_name + "  (" + google_link + ")", unsafe_allow_html=True)


    colocated_markers = {}

    my_log("Disp Map: define m2  ")
    
    center = [42.54043355305221,-76.1342239379883]
    num = 0
    m2 = folium.Map(
        #location=center,
        zoom_start=11
    )


    tracts_tooltip = folium.GeoJsonTooltip(
    fields=["NAME", "GEOID"],
    aliases=["Census Tract:  ", "GEOID:  "],
    #localize=True,
    #sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=100,
    )


    ctracts = folium.FeatureGroup(name="Census Tracts", show=False)
    # census tracts
    folium.GeoJson(tracts_cc_gpd,
              fill_opacity=0.07,
               #tooltip=folium.GeoJsonTooltip(aliases=['Census Tract'], fields=['NAME']),
               tooltip=tracts_tooltip,
               name="Census Tracts").add_to(ctracts)


    nps2 = folium.FeatureGroup(name="NPs")
    # addme = folium.FeatureGroup(name="addme")
    colocated = folium.FeatureGroup(name="Colocated NPs")

    orgs_no_address = []

    #TODO: review workaround.  should not need 
    ein_to_present_num = {}  # temp workaround

    for index, row in np_local_df.sort_values('NAME').iterrows():
        
        # highlight selected nonprofit and get new map center
        # if user selected a cluster, save cluster lat lng
        # to match cluster marker creation  
        
        num = index
        present_num = "(" + str(num) + ") "
        if num == np_df_selected_index:
            color="#FF00AA"
            center = [  row['coord_y'], row['coord_x'] ]
            if row['cluster_ind'] > 0:
                center = [  row['cluster_lat'], row['cluster_lng'] ]
        else:
            color=""

        #TODO: Handle Map selection of one NP in colocated marker
        #TODO: fix this temp workaround to map each co-located ein to a NP number
        ein_str = str(row.EIN)
        ein_to_present_num[ein_str] = present_num

        if not math.isnan(row['coord_x']):  # the data has po boxes with no lat long
            if (row.cluster_ind == 0):  # it's not a cluster

                pop_msg = present_num +  row.NAME 
                pop_msg += "<br>" + row.STREET
                # pop_msg += "<br> x: " + str(row.coord_x) +  "<br>  y:  " + str(row.coord_y) 

                folium.Marker(
                    location=[  row['coord_y'], row['coord_x'] ],
                    icon= number_DivIcon(color,num),
                    # popup= folium.Popup(pop_msg, max_width=300), 
                    # tooltip = present_num + row.NAME
                    tooltip = pop_msg
                ).add_to(nps2)
            else:
                # save aside info about co-located or close orgs
                ngroup = str(int(row.cluster_ngroup))
                if ngroup not in colocated_markers:
                    colocated_markers[ngroup] = [] # first time, initialize

                colocated_markers[ngroup].append(row)                 
        else:
            orgs_no_address.append([index, row.NAME, row.STREET])

    # now, put markers for co-located or close NPs
    for mark_group in colocated_markers:        
        num_markers = str(len( colocated_markers[mark_group]))
        pop_msg = num_markers + " NPs at same or close location " 
        tool_msg = num_markers + " NPs at same or close location "

        #  lat/lng for cluster marker
        lat = colocated_markers[mark_group][0]['cluster_lat']
        lng = colocated_markers[mark_group][0]['cluster_lng']
        mark_loc = [lat, lng]

        if center == mark_loc:
            color = "#FF00AA"
        else: 
            color = "#fff6f1"

        for mark_row in colocated_markers[mark_group]:
            present_num = ein_to_present_num[str(mark_row.EIN)]
            pop_msg += f" <P> {present_num} {mark_row.NAME} <br>"
            pop_msg += f"{mark_row.STREET}  </P>"
    
            tool_msg += f" <br> {present_num} {mark_row.NAME }"

        folium.Marker(mark_loc,    
                     icon= number_DivIcon(color, "M"),
                    popup= folium.Popup(pop_msg, max_width=300), 
                    tooltip = tool_msg

                ).add_to(colocated)
        
        # """

    m2.add_child(nps2)
    #m2.add_child(addme)
    m2.add_child(colocated)
    m2.add_child(ctracts)

    
    folium.LayerControl(collapsed=False).add_to(m2)
   
    # call to render Folium map in Streamlit
    st_m2 = st_folium(m2, 
                      width=675, 
                      height=450,
                      center=center,
                    key="my_np_map",
                    zoom=12    
                      )
    my_log("Disp Map: Rendered Map")

    #  st.markdown("#### Orgs with address that didn't **geocode**")
    #  st.table(orgs_no_address)

    if 'last_object_clicked_tooltip' in st_m2:
        my_log("Disp Map: Last Obj Click TT in st m2")
        if st_m2["last_object_clicked_tooltip"]:
            my_log("Disp Map: Last Obj Click TT, st_m2: " + st_m2["last_object_clicked_tooltip"])

        else:
            my_log("Disp Map: st_m2 has tooltip has NO val ")

    #TODO: combine these two if... both conditions indicated user clicked map, yes?
    if st_m2['last_active_drawing']:
        # get the tooltip to know which NP was selected
        selected_np_option =  st_m2["last_object_clicked_tooltip"]
        
        # if census tract was clicked
        if "Census" in selected_np_option:
            #st.write ("In: ", selected_np_option, selected_np_option[0:1] )
            return st_m2, np_df_selected_index, redraw
 
        # extract the key from parantheses 
        map_selected_index = selected_np_option[selected_np_option.find("(")+1:selected_np_option.find(")")]
        my_log("Disp Map: In Map, last active drawing:  selected np in map click: " + selected_np_option)
        my_log("Disp Map: map selected np index in map click: " + str(map_selected_index))


        # did user click map
        if map_selected_index != np_df_selected_index:
            
            my_log("Disp Map: map selected (" + str(map_selected_index) + ") index " + str(np_df_selected_index))
            my_log("saving new np_df... ")
            np_df_selected_index = map_selected_index
            st.session_state['np_df_selected_index'] = np_df_selected_index

            # leaving stubs of experiments for map redraw for future fiddling  
            # my_log('rerun fragment')
            # st.rerun(scope="fragment")
            # st.rerun(scope="app")

            # when redraw true is returned
            # main will call display map again with updated selected np_df_selected_index
            redraw = True
            my_log("Disp Map: user clicked, so rerun app")


    else:
        my_log("Disp Map: st_m2 last active drawing NO val  ")


    return st_m2, np_df_selected_index, redraw



def display_interesting_links(df_dict):
    """ Formats and writes External Links to more data about an Org 

    Paramters: df_dict(dict): dictionary with all data for selected nonprofit

    Return:  
        link_list (list of dicts):  external links, useful explorations
        Note: currently not using the return value.  
    
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
        return {'status' : 'Directors and Board Members not listed on Tax Documents'}


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
def get_np_dict(df):
    """  
    Creates dictionary with org index number and org name.

    Parameters: 
        np_local_df (dataframe): dataframe with all the NP Info

    Returns: 
        np_dict(dict):  key is the index, value is the org name
    
    """
    
    options = df.index.values.tolist()
    np_names = df['NAME'].values.tolist()
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

def my_log(log_msg):
    """ For debugging, save key moments and variables into st.session 
    
    this is a temp hack as the streamlit -- config.toml stuff seems to be broken?

    Parameters:
        log_msg (str): info to save 

    Returns:  None

    """

    now = datetime.now()
    ds = now.strftime("%H:%M:%S%f")
    st.session_state['app_actions'].append(ds + " - " + log_msg)


def mult_select_change():

    mult_change = st.session_state['np_mult_lov']
    
    st.session_state['np_df_selected_index'] = mult_change
    my_log("User Muli marker change saved to session, index: " + str(mult_change))



def main():
    st.set_page_config(APP_TITLE) #, layout="wide")
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)
    
    # setup debugging 
    # Note: streamlit logging needs fiddling. seems to just stop. 
    # https://docs.streamlit.io/develop/api-reference/configuration/config.toml#set-configuration-options
    # --logger.level=debug 2>logs.txt

    if 'app_actions' not in st.session_state:
        st.session_state['app_actions'] = []
        my_log('Create app_actions')

    my_log("starting Main(T1)")

    # setup styles for used in HTML tables of data and tooltips
    css_table = get_css_style()
    st.markdown (css_table, unsafe_allow_html=True)
    
    # load data
    
    # pre-processed in google colab
    # doesn't change, so put into streamlit cache

    my_log("Main: load cache")
    # populate dataframe of local NPs and put into streamlit cache
    np_local_df = get_np_local_df()

    #TODO: check whether np_list would suffice
    # create dictionary with index and org name as convenience for radio selection 
    np_dict = get_np_dict(np_local_df)

    # tracts for new york, filter to cortland county
    tracts_cc_gpd = get_tracts_shape()

    # Load presentation dictionary with human-readable labels, definitions
    # and control groupings/collections to present
    present_lu = get_present_lu()


    # Setup Session data

    # Arriving with selected nonprofit in session?    
    if 'np_df_selected_index' in st.session_state:
        np_df_selected_index = int(st.session_state['np_df_selected_index'])
        my_log("Main: Index is in Session with val " + str(np_df_selected_index) )

    else:
        np_df_selected_index = 1
        st.session_state['np_df_selected_index'] = np_df_selected_index
        my_log("Main: Index NOT in Session, set to 1 "  )

    #TODO: review - probably doesn't need session state 
    st.session_state['np_dict'] = np_dict

    #TODO: check-why put in session state? just put in sidebar?
    # np_list:alphabetized/ordered list of nonprofits
    if 'np_list' not in st.session_state:
        np_list = list(np_local_df['NAME'])
        np_list.sort()
        st.session_state['np_list'] = np_list

    if 'num_rows' not in st.session_state:
        (num_rows, num_facts) = np_local_df.shape
        st.session_state['num_rows'] = num_rows
        st.session_state['num_facts'] = num_facts
    
    my_log("Main: after session init "  )

    # Note: previously implement as tabs, but replaced with expanders
    # With tabs, the Map did not get updated when it's not in the active/viewed tab
    #TODO: make a stripped down example to validate


    # Note: bug with including markdown in expander title 
    with st.expander("Map"):
        #  ----------- map -----------------------
        
        my_log("Main: Map Tab, start" )
    
        if 'np_radio' in st.session_state:
            my_log("Main: Map tab, np_radio is in session " + str(st.session_state ['np_radio']))
        
        my_log("Main: Map Tab, go do Map with index: " + str(np_df_selected_index))


        # Render Map of NP Markers. 
        (st_m2, np_df_selected_index, redraw ) = display_map(np_local_df, tracts_cc_gpd, np_df_selected_index)
        my_log("Main: Map Tab, returned from Map, index: " + str(np_df_selected_index))

        # If user has clicked on map, redraw with new np_df_selected_index
        if redraw is True:
            (st_m2, np_df_selected_index, redraw ) = display_map(np_local_df, tracts_cc_gpd, np_df_selected_index)
                
        my_log("Main: Map Tab, go do side bar, index: " + str(np_df_selected_index))

        (np_df_selected_index) = do_sidebar(np_local_df, np_df_selected_index)
        my_log("Main: Map Tab, returned from sidebar, index: " + str(np_df_selected_index))

        # convert the selected nonprofit to dict 
        # https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
        #df_dict = np_local_df.loc[filt].to_dict('records')[0]

        my_log("Main: Sum Tab, create df_dict, index: " + str(np_df_selected_index))
        
        df_dict = np_local_df.filter(items=[np_df_selected_index], axis=0).to_dict('records')[0]


    with st.expander("Organization Details"):
        # ----- Organization Details -----------------------------
        my_log("Main: Sum Tab,  index: " + str(np_df_selected_index))

        st.subheader("(" + str(np_df_selected_index) + ") "  + df_dict['NAME'])

        #TODO: find if marker has multiple and list here, maybe lov..
        if df_dict['cluster_ind'] > 0:
            #st.write ("This marker part of cluster:  ", df_dict['cluster_ngroup'] ) 
            msg = """
            This organization is co-located or very close to others on Map.
            Use this selectbox to see details about those orgs.
            """
            st.markdown(msg)

            filt = np_local_df['cluster_ngroup'] == df_dict['cluster_ngroup']
            np_mult = get_np_dict(np_local_df[filt])
            
            options = np_local_df[filt].index.values.tolist()
            sel_index = options.index(np_df_selected_index)
            np_df_selected_mult = st.selectbox("Select Nonprofit from this location", options=options, 
                                    format_func=lambda x: "(" + str(x) + ") " + np_mult[x],
                                    on_change=mult_select_change,
                                    index=sel_index,
                                    key='np_mult_lov')
            
        #TODO: Could streamline by creating list of sections and iterating 
        
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


    with st.expander("Org Data (for debugging)"):
    #with all_tab:
        my_log("Main:, All Tab, entered")

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

    #with explore:

    with st.expander("Explore"):    
    #with explore:
        my_log("Main:, Explore Tab, entered")
        
        tab_summary_md = """
                ##### Explore related info and demographics from other sources               
                - The [Google Data Commons](https://datacommons.org/) project aggregates many datasources
                - [Census Reporter](https://censusreporter.org/) is a remarkable presentation of Census Data
        """
        st.markdown(tab_summary_md)

        st.write ("Links to external sources created using these data elements")
        show_list = ['NAME', 'STREET', 'coord_x', 'coord_y', 'cb_NAME', 'centracts_NAME', 'cb_GEOID']
        display_arbitrary_list(df_dict, present_lu, show_list)

        # if no usable address exists
        if pd.isnull(df_dict['coord_x']):
            st.write ("This NP address could not be geocoded ")
        else:  

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
        # get the tooltip to know which NP was selected
        selected_np_tooltip =  st_m2["last_object_clicked_tooltip"]
        
        # extract the key from parantheses 
        np_df_selected_index = selected_np_tooltip[selected_np_tooltip.find("(")+1:selected_np_tooltip.find(")")]
        my_log("Main: Toolip  map click: " + selected_np_tooltip)
        my_log("Main: Extracted Index: " + str(np_df_selected_index))

    
    #debugging info
    if 1 == 0:
        #st.markdown('##### App Actions')
        #st.write(st.session_state['app_actions'])

        st.markdown('##### All Session Vars')
        st.write(st.session_state)


if __name__ == "__main__":
    main()
    