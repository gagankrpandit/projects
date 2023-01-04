import scrapy
import json
import pandas as pd

class CovidspiderSpider(scrapy.Spider):
    name = 'covidspider'
    allowed_domains = ['www.mygov.in']
    start_urls = ['https://www.mygov.in/sites/default/files/covid/covid_state_counts_ver1.json']

    def parse(self, response):
        resp = json.loads(response.body)
        States = resp.get('Name of State / UT')
        Total_Confirmed_cases = resp.get('Total Confirmed cases')
        Active = resp.get('Active')
        Cured_Discharged_Migrated = resp.get('Cured/Discharged/Migrated')
        Death = resp.get('Death')
        last_confirmed_covid_cases = resp.get('last_confirmed_covid_cases')
        last_cured_discharged = resp.get('last_cured_discharged')
        last_death = resp.get('last_death')
        last_active_covid_cases = resp.get('last_active_covid_cases')
        as_on = resp.get('as_on')

        data_dict = {
            'Last updated': as_on,
            'States': States.values(),
            'Total Confirmed Cases': Total_Confirmed_cases.values(),
            'Active': Active.values(),
            'Cured/Discharged/Migrated': Cured_Discharged_Migrated.values(),
            'Death': Death.values(),
            'last_confirmed_covid_cases': last_confirmed_covid_cases.values(),
            'last_cured_discharged': last_cured_discharged.values(),
            'last_death': last_death.values(),
            'last_active_covid_cases': last_active_covid_cases.values()
        }

        df2 = pd.DataFrame(data_dict)
        df2['key'] = df2['Last updated'] + df2['States']

        df1 = pd.read_csv('main_output.csv')

        df3 = df1.append(df2, ignore_index=True)
        df3.drop_duplicates(subset='key', inplace=True)

        df3.to_csv('main_output.csv', index=False, mode='w')
        # df.to_csv('output.csv',mode='a',index=False, header=False)
        # print(df)
        # df.drop_duplicates(subset='key', inplace=True)
        # print(df)
        # df.to_csv('main_output.csv', index=False, mode='w')