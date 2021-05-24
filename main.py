from web_scraping_utils import *
from postgresql_login import postgresql_login
from sqlalchemy import create_engine


year = '2021'
month ='Abril'
table_name = 'usd_values'


def load_data_into_postgresql_table(df):
    # Prepare login info
    postgresql_str = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'\
    .format(**postgresql_login)
    # Establish connection to postgresql database
    engine = create_engine(postgresql_str)
    conn = engine.connect()
    # Load dataframe to postgresql table
    df.to_sql(table_name, conn, if_exists='append', index=False)
    print('Data loaded to {} table in {} database...'.format(table_name, postgresql_login['dbname']))
    conn.close()


if __name__ == "__main__":
    
    if table_name == "usd_values":
        data = extract_usd_values_from_sii(year, month)
    elif table_name == "uf_values":
        data = extract_uf_values_from_sii(year, month)
        
    load_data_into_postgresql_table(data)
    