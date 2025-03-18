> Report to be transposed to a HTML file

# Report

## 1. Meeting the Brief
Below is how my project deals with the requirements in the brief.

### BRs:
1. I selected multiple datasets about traffic congestion from [Smart Dublin](https://data.smartdublin.ie/), such as [this one](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jan-jun-2023), which is only for January to June 2023. Using these datasets, I eventually ended up with data from 2020-2024. I also used [this dataset](https://data.gov.ie/dataset/traffic-signals-and-scats-sites-locations-dcc) from https://data.gov.ie/ as the congestion data has site IDs, and these IDs link up to this dataset which has the longitudes and latitudes. I filtered this data to store them in an SQL file with 2 tables, one with the congestion data, and the other with the site data. The files used to do this can be found in the `data_filter` folder.
2. 

### ARs:
1. 

## 2. Investigation
I researched 3 scenarios to complete this project around. The first one was a nutrition calculator, where you could input certain conditions you would want (e.g. x grams or less of salt). The second idea was an NBA stat predictor. The last idea was a traffic congestion analyser. The nutrition calculator would have been made for people who would like to find meals that suit their conditions. The NBA stat predictor would have been made for people who bet on NBA games, such as overs and unders for certain players. The traffic idea would have been made for people who drive or just commute in general.

I decided to eliminate the nutrition calculator as one of my ideas first, as it was not a topic which I had any particular interest. Next, I eliminated the NBA stat predictor, as I thought the idea would be too computationally complex. This is because my idea for this project would be to analyse players' performances with and against other players and teams, but also including trends from previous games. However, in this idea, I would have to compute the performances of said other players, as they would affect the original player. This left me with the traffic idea. This idea appealed to me as I had worked on geographical data in the past (population within Dublin) and I had to create a visualisation for that, so I knew I would be more able to do this idea. I did research into existing solutions and provided on example for each of my ideas in the references. Datasets I researched for each idea are also listed in the references.

After looking into the SDCC traffic congestion database, I found the SCATS traffic congestion database, which has much more sites. However, faced with the large amount of data, I decided to restrict my project to the 10 public holidays only, the holidays being:
- New Year's Day
- St Brigid's Day
- St Patrick's Day
- Easter Monday
- May Bank Holiday
- June Bank Holiday
- August Bank Holiday
- October Bank Holiday
- Christmas Day
- St Stephen's Day

This now meant that my target demographic shifted a bit, to people who would commute during holidays, which targets tourists more as well. However the data I had is still just a portion of Dublin, mostly within the M50.

## 3. Plan and Design


## 4. Create
### Log
Week 1:
- Looked through and analysed project brief for requirements
  
Week 2:
- Created report document
- Brainstormed 3 ideas

Week 3:
- Looked at dataset
- Chose new dataset
- Filtered data

Week 4:
- Created wireframe
- Researched data visualisation options

Week 5:
- Finished second data cleaning (approx 650k rows now)

Week 6:
- Worked on website

Week 7:
- Worked on website

Week 8:
- Worked on barchart

Week 9:
- Worked on heatmap

Week 10:
- Rewrote visuals in plotly
- Worked on pathfinding

Week 11:
- Finished website


## 5. Evaluation

## 6. References
Technologies:
- [Python](https://www.python.org/): Main programming language I used
- [HTML](https://en.wikipedia.org/wiki/HTML), [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets), [JavaScript](https://en.wikipedia.org/wiki/JavaScript): Used to build website frontend
- [GitHub](https://github.com/): Hosts git repositories
- [Git](https://git-scm.com/): Version control tool
- [pip](https://pypi.org/project/pip/): Used to download Python modules/libraries/frameworks
- [npm](https://www.npmjs.com/): Used to download JS modules/libraries/frameworks
- [SQLite](https://www.sqlite.org/): Database used
- [VsCode](https://code.visualstudio.com/): Code editor
- [Figma](https://www.figma.com/): Used for wireframes and flowcharts

Python modules/libraries/frameworks:
- [Flask](https://flask.palletsprojects.com/en/stable/): Server
- [Plotly](https://plotly.com/): Visualisations
- [Matplotlib](https://matplotlib.org/): Originally used for visualisations
- [Aiosqlite](https://pypi.org/project/aiosqlite/): Asynchronous version of sqlite3
- [Numpy](https://numpy.org/): Mathematical analysis
- [Scipy](https://scipy.org/): Histogram and other mathematical tools
- [Waitress](https://pypi.org/project/waitress/): Used to run server

HTML, CSS, JavaScript modules/libraries/frameworks:
- [Bootstrap](https://getbootstrap.com/): Frontend components/styling tools
- [Leaflet](https://leafletjs.com/): Map to be used in pathfinding
- [Heatmap.js](https://www.patrick-wied.at/static/heatmapjs/): Heatmap to be overlayed on Leaflet map
- [Kode Mono](https://fonts.google.com/specimen/Kode+Mono): Font used in navbar

Other:
- [Google](https://www.google.ie/): Search engine used
- [Stackoverflow](https://stackoverflow.com/): Problems to issues I had
- [Python Docs](https://docs.python.org/3/): Standard library docs
- [Mozilla Docs](https://developer.mozilla.org/en-US/): CSS, JS docs
- [W3 Schools](https://www.w3schools.com/): Code examples
- [GeeksForGeeks](https://www.geeksforgeeks.org/): Code examples
- [Citizens Information](https://www.citizensinformation.ie/en/employment/employment-rights-and-conditions/leave-and-holidays/public-holidays/): Dates for public holidays

Existing Solutions:
- [Nutrition Value](https://www.nutritionvalue.org/nutritioncalculator.php)
- [BettingPros](https://www.bettingpros.com/nba/picks/prop-bets/)
- [Google Maps](https://www.google.com/maps)

Datasets:
- [SCATS Traffic Sites](https://data.smartdublin.ie/dataset/traffic-signals-and-scats-sites-locations-dcc)
- Various biannual datasets:
  - [Jan-Jun 2020](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jan-jun-2020)
  - [Jul-Dec 2020](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jul-dec-2020)
  - [Jan-Jun 2021](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jan-jun-2021)
  - [Jul-Dec 2021](https://data.smartdublin.ie/dataset/traffic-volumes-from-scats-traffic-management-system-jul-dec-2021-dcc)
  - [Jan-Jun 2022](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jan-jun-2022)
  - [Jul-Dec 2022](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jul-dec-2022)
  - [Jan-Jun 2023](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jan-jun-2023)
  - [Jul-Dec 2023](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jul-dec-2023)
  - [Jan-Jun 2024](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jan-jun-2024)
  - [Jul-Dec 2024](https://data.smartdublin.ie/dataset/dcc-scats-detector-volume-jul-dec-2024)
- [Traffic Flow Data Jan to June 2022 SDCC](https://data.gov.ie/dataset/traffic-flow-data-jan-to-june-2022-sdcc1): One of the original datasets that I found for traffic
- [Nutrition Dataset](https://www.kaggle.com/datasets/gokulprasantht/nutrition-dataset): Dataset for nutrition
- [Food.com Recipes](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions): Recipies dataset
- [NBA Database](https://www.kaggle.com/datasets/wyattowalsh/basketball): Database of player stats
    
## 7. Summary Word Count

| Section                | Word Count |
| ---------------------- | ---------- |
| 1. Meeting the brief   | 0          |
| 2. Investigation       | 0          |
| 3. Plan and Design     | 0          |
| 4. Create              | 0          |
| 5. Evaluation          | 0          |
| **Total:**             | 0          |
