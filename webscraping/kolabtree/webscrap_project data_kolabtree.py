import scrapy 
import json
from requests import get
from bs4 import BeautifulSoup
class WebscrapSpider(scrapy.Spider):
    name = 'webscrap'

    # profile data form kolabtree
    # start_urls = ['https://www.kolabtree.com/find-an-expert']
    # headers = {            
    #     "accept": "*/*",
    #     "accept-encoding": "gzip, deflate, br",
    #     "accept-language": "en,en-US;q=0.9",
    #     "content-type": "application/json",
    #     "referer":" https://www.kolabtree.com/find-an-expert",
    #     "sec-fetch-dest": "empty",
    #     "sec-fetch-mode": "cors",
    #     "sec-fetch-site": "same-origin",
    #     "sec-gpc": "1",
    #     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36",
    #     "x-requested-with": "XMLHttpRequest",
    # }
    # def parse(self,response):
    #     num = 5*79
    #     url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+1)
    #     yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)        
    #     url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+2)
    #     yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)
    #     url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+3)
    #     yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)        
    #     url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+4)
    #     yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)    
    #     url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+5)
    #     yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)        



    # def parse_api(self,response):
    #     raw_data = response.body
       
    #     data = json.loads(raw_data)
    #     for i in data["BrowserUserDetails"]:
    #         yield {
    #             "ProfileId": i["ProfileId"],
    #             "SalutationName": i["SalutationName"],
    #             "FullName" : i["FullName"],
    #             "Headline": i["Headline"],
    #             "UserSubjectAreas": i["UserSubjectAreas"],
    #             "LatestEducation": i["LatestEducation"],
    #             "IsPhD": i["IsPhD"],
    #             "FreelancerStar": i["FreelancerStar"],
    #             "NoOfAbortedProjects":i["NoOfAbortedProjects"],
    #             "NoOfConfirmedProjects": i["NoOfConfirmedProjects"],
    #             "NoOfCompletedProjects": i["NoOfCompletedProjects"],
    #             "NoOfBids": i["NoOfBids"],
    #             "HourlyRate": i["HourlyRate"],
    #             "CertificationCount": i[ "CertificationCount"],
    #             "UserEmail": i["UserEmail"],
    #             "CurrentCity": i["CurrentCity"],
    #             "CurrentState": i["CurrentState"],
    #             "CurrentCountry": i["CurrentCountry"],
    #             "CurrentPostcode": i["CurrentPostcode"],               
    #         }


    #project data from kolabtree
    start_urls = ['https://www.kolabtree.com/project']
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en,en-US;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.kolabtree.com",
        "pragma": "no-cache",
        "referer": "https://www.kolabtree.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    def parse(self,response):
        for i in range(1,118):
            url = "https://www.kolabtree.com/projects/?page="+str(i)
            response = get(url,verify = False)
            # projectID = []
            if response.status_code == 200:
                html_soup = BeautifulSoup(response.text,'html.parser')
                data = html_soup.find_all('div',class_ = 'ProjectCard')

                for j in data:
                    d={
                        "ServiceName": j.find('div',class_ = "service-name").text.replace("\n","").lstrip().rstrip(),
                        "ProjectName": j.find('div',class_ = "browse-title").text.replace("\n","").lstrip().rstrip(),
                        "ProposedFee": j.find('span',class_ = "budg-cur-text").text.replace("\n","").lstrip().rstrip(),
                        "Label": j.find('span',class_ = "badge").text.replace("\n","").lstrip().rstrip(),
                        "PostedOn": j.find('span',class_ = "postedonvalue").text.replace("\n","").lstrip().rstrip(),
                        # "HiringTimeline": j.find('div',class_ = "").text,
                       
                    }
                    
                    SubArea = j.find('div',class_ = "subject-area")
                    if SubArea:
                        link = SubArea.find_all('a')
                        value = ""
                        for k in link:
                            value =value + k.text.replace("\n","").lstrip().rstrip() + ", "
                        d["SubjectArea"] = value
                    else:    
                        d["SubjectArea"] = ""
                    url = "https://api.kolabtree.com/project/TaskAndSubcategoryDetails?projectUUID="+str(j['data-projectuuid'])
                    yield scrapy.Request(url, callback = self.parse_api,headers = self.headers,meta={"item":d}) 

    
    def parse_api(self,response):
        raw_data = response.body
        data = json.loads(raw_data)
        item = response.meta['item']
        item["Subcategory"]=data["Payload"]["SubServiceNames"]
        item["Task&Deliverables"]=data["Payload"]["TaskName"]
        item["Length"]=data["Payload"]["TaskUnitValue"]
        yield item