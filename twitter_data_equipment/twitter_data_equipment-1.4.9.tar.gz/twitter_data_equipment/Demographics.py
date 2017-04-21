"""
Adds Information on demographic data (Population, Race and Poverty) to database
"""

from urllib import request
from bs4 import BeautifulSoup
import json
import pandas as pd
import os


def _get_population(dataframe, longitude, latitude):
    """
    This function gets a dataframe and geo-coordinates and gets the FIPS-Codes and the Names of the state and the county
    the coordinates are placed in. On the basis of this information the exact population for the county in the year 2010
    can be determined.
    
    :param pd.Dataframe dataframe: Dataframe containing population information for each county
    
    :param float longitude: Longitude coordinate of tweet
    
    :param float latitude: Latitude coordinate of tweet
    
    :return dict of (str,str): In case of successfull identification of county, a dict containing names and FIPS-Codes 
    as well as population information
    
    """

    # Call to data.fcc.gov/api is made to determine county and state
    url1 = 'http://data.fcc.gov/api/block/find?latitude={0}&longitude={1}&showall=false&format=json'.format(
        str(latitude),
        str(longitude))
    with request.urlopen(url1) as response:
        try:
            html = response.read()
            b4 = BeautifulSoup(html, 'lxml')
            a = json.loads(str(b4.get_text()))

            # Api-Information is evaluated
            if a['County']['FIPS'] is not None:
                state_FIPS = a['State']['FIPS']
                county_FIPS = a['Block']['FIPS'][2:5]
                combined_FIPS = str(state_FIPS) + str(county_FIPS).zfill(3)

                # Population data gets determined
                df = dataframe[dataframe.Combined_FIPS == int(combined_FIPS)]
                pop = df['Population'].values[0]
                name = df['Name'].values[0]
                county_name, state_name = name.split(', ')
                return {'State_Name': state_name, 'County_Name': county_name, 'Population': pop,
                        'State_FIPS': state_FIPS,
                        'County_FIPS': county_FIPS}
            else:
                print('Coordinates not in the US')
                return None
        except:
            return None


def _get_racial_statistics(dataframe, state_code, county_code, population):
    """
    Calculates percentages of Hispanic, Black and White people according county using the total amount of people in the 
    county
    
    :param pd.Dataframe dataframe: Dataframe containing racial information on each county
    
    :param int state_code:
    
    :param int county_code: 
    
    :param int population: 
    
    :return dict of (str,float): 
    
    """

    # Dataframe gets narrowed down to relevant information
    df = dataframe[dataframe.STATE == int(state_code)]
    df = df[df.COUNTY == int(county_code)]

    # Percentage of hispanic people
    df_hisp = df[df.ORIGIN == 2]
    perc_hisp = float(round(pd.DataFrame(df_hisp.groupby([df.IMPRACE])['RESPOP'].sum())['RESPOP'].sum() / population * 100, 2))

    # Percentage of black people
    df_black = df[df.IMPRACE == 2]
    perc_black = float(round(pd.DataFrame(df_black.groupby([df.ORIGIN])['RESPOP'].sum())['RESPOP'].sum() / population * 100,
                       2))

    # Percentage of white people
    df_white = df[df.IMPRACE == 1]
    perc_white = float(round(pd.DataFrame(df_white.groupby([df.ORIGIN])['RESPOP'].sum())['RESPOP'].sum() / population * 100,
                       2))

    return {'Hispanic': perc_hisp, 'Black': perc_black, 'White': perc_white}


def _get_poverty_statistics(dataframe, state_code, county_code):
    """
    Calculates poverty-rate of people living below certain threshold
    
    :param dataframe: Containing poverty data
    
    :param int state_code: 
    
    :param int county_code: 
    
    :return float:
    
    """
    dataframe.columns = ['STATE', 'COUNTY', 'NAME', 'POV']
    df = dataframe[dataframe.STATE == int(state_code)]
    if len(df) > 0:
        df = df[df.COUNTY == int(county_code)]
        return float(df['POV'].values[0])
    else:
        return 0


def add_demographic_statistics(input_path, output_path):
    """
    Takes path to Csv-File after beeing processed by module 'Processing' and adds demographic information on race,
    population and poverty to it according to geo-information - if any.
    
    :param str input_path: Path to Csv-Input-File
    
    :param str output_path: Path to destination of output-file. File gets overwritten if already existing and generated if not
    
    """

    # Open input file
    df_twitter_data = pd.read_csv(open(input_path))

    # Add column headers to input Csv-file
    df_twitter_data['has_stats'] = ''
    df_twitter_data['State_FIPS'] = ''
    df_twitter_data['County_FIPS'] = ''
    df_twitter_data['State_Name'] = ''
    df_twitter_data['County_Name'] = ''
    df_twitter_data['Population'] = ''
    df_twitter_data['Perc_Hisp'] = ''
    df_twitter_data['Perc_Black'] = ''
    df_twitter_data['Perc_White'] = ''
    df_twitter_data['Perc_Poverty'] = ''

    # Open datasheets containing population, racial and poverty data
    this_dir,_ = os.path.split(__file__)

    racial_data_dir = os.path.join(this_dir,'data_sheets','race_data.csv')
    df_racial_data = pd.read_csv(open(racial_data_dir))

    poverty_data_dir = os.path.join(this_dir,'data_sheets','poverty_data.csv')
    df_poverty_data = pd.read_csv(open(poverty_data_dir),
                                  usecols=['State FIPS', 'County FIPS', 'Name', 'Poverty Percent All Ages'])

    poverty_data_dir = os.path.join(this_dir,'data_sheets','population_data.csv')
    df_population_data = pd.read_csv(open(poverty_data_dir), delimiter=';')

    # Iterate through rows of input-file
    for i, row in df_twitter_data.iterrows():

        # If tweet contains geo-information, evaluate longitude and latitude and update it in the file if necessary
        if row.is_geo == 1:
            geo_cord_dict = _get_population(df_population_data, int(row.geo_long), int(row.geo_lat))

            if geo_cord_dict is not None:
                # Get racial and poverty data
                RaceDict = _get_racial_statistics(df_racial_data, geo_cord_dict['State_FIPS'], geo_cord_dict['County_FIPS'],
                                                  geo_cord_dict['Population'])
                PovertyPerc = _get_poverty_statistics(df_poverty_data, geo_cord_dict['State_FIPS'],
                                                      geo_cord_dict['County_FIPS'])

                # Update file with new information
                df_twitter_data.set_value(i, 'has_stats', 1)
                df_twitter_data.set_value(i, 'County_Name', geo_cord_dict['County_Name'])
                df_twitter_data.set_value(i, 'County_FIPS', geo_cord_dict['County_FIPS'])
                df_twitter_data.set_value(i, 'State_Name', geo_cord_dict['State_Name'])
                df_twitter_data.set_value(i, 'State_FIPS', geo_cord_dict['State_FIPS'])
                df_twitter_data.set_value(i, 'Population', repr(geo_cord_dict['Population']))
                df_twitter_data.set_value(i, 'Perc_Hisp', repr(RaceDict['Hispanic']))
                df_twitter_data.set_value(i, 'Perc_Black', repr(RaceDict['Black']))
                df_twitter_data.set_value(i, 'Perc_White', repr(RaceDict['White']))
                df_twitter_data.set_value(i, 'Perc_Poverty', repr(PovertyPerc))


        # Write new data to output destination
    df_twitter_data.to_csv(open(output_path, 'w'), mode='w', index=False)
