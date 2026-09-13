# MyCountry App

## Data Analysis Project - DS24 course, BIU

### Written by Ariel Rubanenko and Lior Sinay
### 2026/09/10
***

### 1. App Description
Allows users to select either a country, continent or region and receive useful information covering economic, demographic, social, medical, 
and environmental aspects of their selected entity. 

<u>Highlights</u>:

* Based on a CSV file created from an external API.
* Uses Streamlit to run the app on the user's localhost.
* Data is presented in both tabular and graphical formats. 
* Per the user's selection, either intra-entity (self) analysis or inter-entity (comparative) analysis can be applied. 


### 2. Running the app
To run MyCountry app, take the following steps:
* Open the PyCharm's terminal.
* Run the command : **streamlit run main.py**
* Follow the guidelines and select the desired analysis.


### 3. App results
After the app is run successfully, the following results are expected: 
* Charts - figures of the key measures for the selected analysis type. 
* Descriptive statistics table of the complete dataset - shown at the bottom of the screen, below the charts.
* Description table of the numeric variables - a short description of each numeric variable in the columns of the dataset and its units. 


#### 4.1 <u>External API</u>:
The data from two external APIs is consolidated to generate the dataset:

4.1.1 Country -
* provides the key geographic, demographic, and economic statistics about every country in the world.
* url : 'https://api.api-ninjas.com/v1/country?name={}'.format(<country name>)
* Requires an API key.

4.1.2 Country Flag - 
* provides SVG flag images for any country, territory, or area of special interest.
* url : 'https://api.api-ninjas.com/v1/countryflag?country={}'.format(<country_ISO2>)
* Requires an API key.

#### 4.2 <u>Local CSV file</u>:
* Located within the project directory.
* File name: **country_with_data.csv**

### 5. Optional types of analysis
#### 5.1 <u>intra (self)</u>
   * intra_country   - Shows the flag and ID, and charts of key measures for the selected country.
   * intra_continent - Plots charts of key measures for the selected continent.
   * intra_region    - Plots charts of key measures for the selected region.

#### 5.2 <u>inter (comparative)</u>
   * inter_country   - Plots charts of key measures and marks the value of each measure for the selected country relative to all other countries in the database.
   * inter_continent - Plots charts of key measures for all continents in the database.
   * inter_region    - Plots charts of key measures for all regions in the database.

#### 5.3 <u>Correlation matrix</u>
   * Scatter plots for pairs of variables in the database whose correlation coefficient meets a certain criterion.
   * By default,the plotted pairs are those with absolute correlation coefficient > 0.9


### 6. Project dirctory - Main Scripts and files 
#### 6.1 <u>Python scripts</u>:
* main.py                      - Main code. 
* libs_and_modules.py          - Imports all libraries and modules used in the project. All other functions refer to it via an import command.
* config_app_env.py            - Sets the background and configures the format of Streamlit's page.
* manage_app_interface.py      - Controls the app's interface to the user and creates a processed database to be used based on the user's selection.
* import_country_data.py       - Imports the data from the external APIs. Used only if the user selects to import new data.
* Units_Txt.py                 - Creates a table with a short description for each of the numeric variables used in the dataset and specifies its unit of measurement.
* Intra_country_functions.py   - Runs a self-analysis for a specific country, per the user's selection.
* Intra_continent_functions.py - Runs a self-analysis for a specific continent, per the user's selection.
* Intra_region_functions.py    - Runs a self-analysis for a specific region, per the user's selection.
* Inter_country.py             - Runs a comparative analysis for a specific country, per the user's selection.
* Inter_continent.py           - Runs a comparative analysis between continents.
* Inter_region.py              - Runs a comparative analysis between regions.
* Correlation_Matrix.py        - Creates charts of scatter plots between variables with an absolute correlation coefficient higher than a certain threshold (default is 0.9) 

#### 6.2 <u>Local CSV files</u>:
* countries.csv                - Auxiliary file with a list of countries, their codes(ISO2) and the continent in which they are located. Used for generation of the actual dataset.
* country_with_data.csv        - The complete dataset. Reflects the latest data that was read from the external API.

#### 6.3 <u>Log files (optional)</u>:
* country_data_analyze_and_process_log.txt - A log file created during the processing and analysis of the complete dataset. 
* intra_country_functions_log.txt          - A log file created while an intra-country analysis is run.
* intra_continent_functions_log.txt        - A log file created while an intra-continent analysis is run.
* intra_region_functions_log.txt           - A log file created while an intra-region analysis is run.


### 7. Project directory - Main Sub-Directories 
* .streamlit - Includes a single file named **secrets.toml** that contains the API key and is not tracked by Git.
