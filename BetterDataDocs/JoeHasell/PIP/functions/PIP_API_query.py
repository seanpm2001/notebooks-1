import pandas as pd
import requests
import io

def pip_query_country(popshare_or_povline, value, country_code="all", year="all", fill_gaps="true", welfare_type="all", reporting_level="all", ppp_version=2011):

    if ppp_version == 2011:
        version = "20220909_2011_02_02_PROD"
        
    elif ppp_version == 2017:
        version = "20220909_2017_01_02_PROD"
        
    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip?{popshare_or_povline}={value}&country={country_code}&year={year}&fill_gaps={fill_gaps}&welfare_type={welfare_type}&reporting_level={reporting_level}&ppp_version={ppp_version}&version={version}&format=csv'
    status = 0
    
    while status != 200:
        #df = pd.read_csv(request_url)
        response = requests.get(request_url, timeout=500)
        content = response.content
        status = response.status_code
    
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))

    return df


# For world regions, the popshare query is not available (or rather, it returns nonsense).
def pip_query_region(povline, year="all", ppp_version=2011):

    if ppp_version == 2011:
        version = "20220909_2011_02_02_PROD"
        
    elif ppp_version == 2017:
        version = "20220909_2017_01_02_PROD"
    

    # Build query
    request_url = f'https://api.worldbank.org/pip/v1/pip-grp?country=all&povline={povline}&year={year}&ppp_version={ppp_version}&version={version}&group_by=wb&format=csv'
    status = 0
    
    while status != 200:
        #df = pd.read_csv(request_url)
        response = requests.get(request_url, timeout=500)
        content = response.content
        status = response.status_code
    
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    df = df[df['reporting_year']>=1990].reset_index(drop=True)

    return df
