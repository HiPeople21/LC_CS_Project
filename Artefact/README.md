# LC_CS_Project

How to setup:
1. Install the Python dependencies:
    - pip install -r requirements.txt
2. Install the JavaScript dependencies:
    - `cd` into the `website/static` folder
    - `npm init`
    - `npm install heatmap.js`
    - `npm install leaflet`
    - `npm install bootstrap@v5.3.3`
3. Clean and filter the data:
    - Add the data into `data_filter/data/{year}`, where the file follows the naming scheme `SCATS{month}{year}.csv`, such as `data_filter/data/2020/SCATSJanuary2020.csv`
    - Create the folder `data_filter/output_data`
    - `cd` to `Artefact`'s parent folder. The rest of the instructions will take place from this folder
    - Run `python -m Artefact.data_filter.data_filter` to create the files in `data_filter/output_data`
    - Run `python -m Artefact.data_filter.secondary_filter` to create and populate `database.db`
4. Set up the website:
    - Run `waitress-serve --listen=127.0.0.1:5000 Artefact.website.app:app`
