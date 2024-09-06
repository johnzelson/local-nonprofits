# installs
# py -m pip install streamlit
# py -m pip install pandas
# py -m pip install folium
# py -m pip install streamlit_folium
# py -m pip install geopandas
# py -m pip install streamlit-card
# py -m pip install streamlit_extras
# py -m pip install streamlit-elements==0.1.*



import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import math
import streamlit.components.v1 as components

# test 3rd party options for layout
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

def do_sidebar(df, np_name):
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
                                   index=np_index )
            #                       key="np_radio")
            #                       on_change=np_change)


            st.session_state['selected_np'] = selected_np 

            #st.session_state['selected_np'] = selected_np

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


def display_map(cortland_geotaxweb_df, tracts_cc_gpd):
    import math

    m = folium.Map(
        location=[42.5,-76],
        zoom_start=10
    )

    # you can pass gdf to geojson
    folium.GeoJson(tracts_cc_gpd,
                fill_opacity=0.1,
                popup=folium.GeoJsonPopup(fields=['NAME']),
                name="Census Tracts").add_to(m)
    group_1 = folium.FeatureGroup("NPs").add_to(m)

    for index, row in cortland_geotaxweb_df.iterrows():

        if not math.isnan(row['coord_x']):  # the data has po boxes with no lat long

            folium.CircleMarker(
                location=[  row['coord_y'], row['coord_x'] ],
                #folium.Marker(location=[ row['coord_x'], row['coord_y'] ],
                fill=True,
                Highlight=True,
                # Highlight= True,
                #highlight_function= lambda feat: {'fillColor': 'blue'},
                #popup=row['NAME'],
                #popup=folium.Popup(row['NAME']),
                #popup=folium.Popup(html),
                #popup=folium.Popup(get_popup(row), max_width=300),
                #popup=folium.Popup(get_map_popup(row), max_width=300),
                popup=folium.Popup(get_map_popup(row, cortland_geotaxweb_df), max_width=300),
                #tooltip=row['NAME'],
                tooltip = row.NAME,
                #radius=15,
            # fill_color="#3db7e4"
                ).add_to(group_1)

    folium.LayerControl().add_to(m)

    st_map  = st_folium(m, width=700) #, returned_objects=["last_object_clicked"])
    
    selected_np = ''
    if st_map['last_active_drawing']:
        #state_name = st_map['last_active_drawing']['properties']['name']
        selected_np =  st_map["last_object_clicked_tooltip"]
        st.write ("selected np in map click: " + selected_np)
        st.session_state['selected_np'] = selected_np #hm, just in case
 
    return selected_np


def org_basics(df_dict):
    org_dict = {}
    show_list = ['NAME', 'STREET', 'CITY', 'ICO',
                    'ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT',
                    'ntee_cat', 'WebsiteAddressTxt']
    for s in show_list:
        # st.write(df_dict[s])
        # org_dict.update(df_dict[s])  # doesn't work??
        org_dict[s] = df_dict[s]
    #org_dict = df_dict.fromkeys(show_list, 0)
    # st.write(org_dict)
    # st.table(org_dict)
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


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # load data
    # pre-processed in google colab
    cortland_geotaxweb_df = pd.read_csv('data/cortland_geotaxweb_df.csv')

    # tracts for new york, filter to cortland county
    tracts_gpd = gpd.read_file('data//tl_2022_36_tract.shp')
    tracts_cc_gpd = tracts_gpd[tracts_gpd['COUNTYFP'] == '023']

    # Initialize session data
    
    #TODO: check-why put in session state? just put in sidebar?
    if 'np_list' not in st.session_state:
        np_list = list(cortland_geotaxweb_df['NAME'])
        np_list.sort()
        st.session_state['np_list'] = np_list

    if 'num_nps' not in st.session_state:
        (num_rows, num_facts) = cortland_geotaxweb_df.shape
        st.session_state['num_rows'] = num_rows
        st.session_state['num_facts'] = num_facts

    #  sidebar
    #do_sidebar(cortland_geotaxweb_df)
    #selected_np = st.session_state['selected_np']

    # does it matter when i do sidebar?
    #  sidebar

    #if 'selected_np' in st.session_state:
    #    selected_np = st.session_state['selected_np']
    #else:
    #    selected_np = np_list[0]

    #selected_np = do_sidebar(cortland_geotaxweb_df, selected_np)
    


    # main content area
    tab1, tab2, testtab = st.tabs(["Map", "Data", "TestTabs"])


    with tab1:
        #  ----------- map -----------------------
        selected_np = ''
        selected_np = display_map(cortland_geotaxweb_df, tracts_cc_gpd)
        selected_np = do_sidebar(cortland_geotaxweb_df, selected_np)
        #TODO: when user selects from radio buttons, want to adjust map dynamically
        # https://folium.streamlit.app/dynamic_map_vs_rerender

    with tab2:
        # ----- info -----------------------------
        st.write("Info Panel")
        st.write(selected_np)

        # get detailed on selected np, lookup by name for now    
        filt = cortland_geotaxweb_df['NAME'] == selected_np

        # st.write(cortland_geotaxweb_df.loc[filt].T)

        # convert to dict 
        # https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
        df_dict = cortland_geotaxweb_df.loc[filt].to_dict('records')[0]


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
                         'ntee_cat']
            for s in show_list:
                st.write(df_dict[s])

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
                f'<td> Name:</td> <td>  {df_dict["NAME"]} </td> '
                f'</tr> '
                f'<tr> '
                f'<td> Post Addr:</td> <td> {df_dict["STREET"]}, {df_dict["CITY"]} {df_dict["ZIP"]}</td> '
                f'</tr> '
                f'<tr> '
                f'<td> IRS Contact:</td> <td> {df_dict["ICO"]} </td> '
                f'</tr> '

                f'<tr> '
                f'<td> EIN:</td> <td> {df_dict["EIN"]} </td> '
                f'</tr> '
                f'<tr> '
                f'<td> Subsection </td>'
                f'<td> 501c({df_dict["SUBSECTION"]}) </td>'
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

        card_container = st.container()

        with card_container:
            # Title within the card
            st.header("Choose an option:")

            st.write(" blah blah")
        
        with st.container():
            st.header('Dashboard Card Title')
            st.text('Some interesting insights')

    with testtab:
        st.write("test tab")
        st.subheader("Org Basics")
        st.table(org_basics(df_dict))

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
    
