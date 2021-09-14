import scrapy 
import json
class WebscrapSpider(scrapy.Spider):
    name = 'webscrap'
    start_urls = ['https://www.kolabtree.com/find-an-expert']

    headers = {            
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en,en-US;q=0.9",
        "content-type": "application/json",
        "referer":" https://www.kolabtree.com/find-an-expert",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }


    def parse(self,response):
        num = 5*79
        url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+1)
        yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)        
        url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+2)
        yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)
        url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+3)
        yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)        
        url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+4)
        yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)    
        url = 'https://www.kolabtree.com/api/search/DoDBSearch?PageNumber='+str(num+5)
        yield scrapy.Request(url, callback = self.parse_api,headers = self.headers)        



    def parse_api(self,response):
        raw_data = response.body
       
        data = json.loads(raw_data)
        for i in data["BrowserUserDetails"]:
            yield {
                "ProfileId": i["ProfileId"],
                "SalutationName": i["SalutationName"],
                "FullName" : i["FullName"],
                "Headline": i["Headline"],
                "UserSubjectAreas": i["UserSubjectAreas"],
                "LatestEducation": i["LatestEducation"],
                "IsPhD": i["IsPhD"],
                "FreelancerStar": i["FreelancerStar"],
                "NoOfAbortedProjects":i["NoOfAbortedProjects"],
                "NoOfConfirmedProjects": i["NoOfConfirmedProjects"],
                "NoOfCompletedProjects": i["NoOfCompletedProjects"],
                "NoOfBids": i["NoOfBids"],
                "HourlyRate": i["HourlyRate"],
                "CertificationCount": i[ "CertificationCount"],
                "UserEmail": i["UserEmail"],
                "CurrentCity": i["CurrentCity"],
                "CurrentState": i["CurrentState"],
                "CurrentCountry": i["CurrentCountry"],
                "CurrentPostcode": i["CurrentPostcode"],
               
            }
            # yield row
            # print(row)


            
    
    # def parse_further_api(self,response):
    #     raw_data = response.body
    #     data = json.loads(raw_data)
                       
    #     # print(len(TotelRecordCount))



