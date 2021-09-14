import scrapy
from scrapy.http import FormRequests 
import json
from requests import get
from bs4 import BeautifulSoup
class LinkedinSpider(scrapy.Spider):
    name = "Linkedin"
    start_urls = ['https://www.linkedin.com/search/']
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en,en-US;q=0.9',
        'cache-control': 'no-cache',
        'csrf-token': 'ajax:3163218234532302923',
        'pragma': 'no-cache',
        'referer': 'https://www.linkedin.com/mwlite/search/results/all?keywords=researcher',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Mobile Safari/537.36',
        'x-effective-connection-type': '4g',
        'x-li-page-instance': 'urn:li:page:p_mwlite_search_srp;473dd745-e495-4273-8cc4-92744f174472',
        'x-referer-pagekey': 'p_mwlite_search_srp',
        'x-requested-with': 'XMLHttpRequest',
        'x-tracking-id': '473dd745-e495-4273-8cc4-92744f174472',
    }

    def start_requests(self):
        return [ FormRequests('https://www.linkedin.com/login?fromSignIn=true',
                               formdata={'username':'saniranpariya@gmail.com',
                                         'password':'*s4a5n6i#'
                                        },
                               callback=self.parse )]

    def parse(self,response):
        url = 'https://www.linkedin.com/mwlite/search/results/all?keywords=researcher&amp;origin=GLOBAL_SEARCH_HEADER&pageNumber=101'
        response = get(url,verify = False)
        if response.status_code == 200:
            # html_soup = BeautifulSoup(response.text,'html.parser')
            print(response.text)