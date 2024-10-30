# Local Nonprofits (App in DRAFT)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://local-nonprofits-jzelson.streamlit.app//)

A streamlit app that collects data about nonprofits in a local area in order to learn about community.  

Data Sources:
- IRS Business Master File (BMF) of "active" nonprofits
- IRS Tax Returns (Form 990-series)
- Census
- Congress API
- Censusreporter
- Probublica

The data is processed in five google colab notebooks from [np-colab-notebooks](https://github.com/johnzelson/np-colab-notebooks)

Additional background can be found at (link)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
