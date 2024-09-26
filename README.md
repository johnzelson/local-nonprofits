# Local Nonprofits (App in DRAFT)

This app collects data about nonprofits in a local area in order to learn about community. The data is collected from multiple sources and has links to other resources that seemed interesting.  

Data Sources:
- IRS Business Master File (BMF) of "active" nonprofits
- IRS Tax Returns (Form 990-series)
- Census
- Congress API

With external links to the amazing Censusreporter, Probublica, and...

The data is processed in five google colab notebooks (link)

[Open Local Nonrofits in Streamlit](https://local-nonprofits-jzelson.streamlit.app/)

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
