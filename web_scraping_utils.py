## IMPORT LIBRARIES ##

from bs4 import BeautifulSoup
import requests
import pandas as pd

## DEFINE month_dict ##

month_dict = {
    'Enero': 1,
    'Febrero': 2,
    'Marzo': 3,
    'Abril': 4,
    'Mayo': 5,
    'Junio': 6,
    'Julio': 7,
    'Agosto': 8,
    'Septiembre': 9,
    'Octubre': 10,
    'Noviembre': 11,
    'Diciembre': 12
}
    
## DEFINE FUNCTIONS ##

def extract_uf_values_from_sii(year, month):
    
    url = 'https://www.sii.cl/valores_y_fechas/uf/uf{}.htm'.format(year)
    sauce = requests.get(url).text
    soup = BeautifulSoup(sauce, features="lxml")

    month_data = soup.find('div', id='mes_{}'.format(month.lower()))

    days_list = []
    values_list = []

    table_rows = month_data.find_all('tr')[1:]
    for row in table_rows:
        days = row.find_all('th')
        for day in days:
            days_list.append(day.string)
          
        values = row.find_all('td')  
        for value in values:
            values_list.append(value.string)

    df = pd.DataFrame(list(zip(days_list, values_list)), columns=['day', 'uf_value'])
    df = df.dropna()
    df['day'] = df['day'].astype('int')
    df['uf_value'] = df['uf_value'].apply(lambda x: x.replace('.', '').replace(',', '.')).astype('float')
    df['month'] = month_dict[month]
    df['year'] = year
    df = df.sort_values(by='day').reset_index(drop=True)
    df = df[['year', 'month', 'day', 'uf_value']]

    return df


def extract_usd_values_from_sii(year, month):

    url = 'https://www.sii.cl/valores_y_fechas/dolar/dolar{}.htm'.format(year)
    sauce = requests.get(url).text
    soup = BeautifulSoup(sauce, features="lxml")

    month_data = soup.find('div', id='mes_{}'.format(month.lower()))

    days_list = []
    values_list = []

    table_rows = month_data.find_all('tr')
    for row in table_rows:
        days = row.find_all('th')
        for day in days:
            days_list.append(day.string)
          
        values = row.find_all('td')  
        for value in values:
            values_list.append(value.string)

    df = pd.DataFrame(list(zip(days_list, values_list)), columns=['day', 'usd_value'])
    df = df.dropna()
    df['day'] = df['day'].astype('int')
    df['usd_value'] = df['usd_value'].astype('float')
    df['month'] = month_dict[month]
    df['year'] = year
    df = df.sort_values(by='day').reset_index(drop=True)
    df = df[['year', 'month', 'day', 'usd_value']]

    return df
    
