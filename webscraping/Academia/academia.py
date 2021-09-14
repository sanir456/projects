import scrapy 
import json
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class AcademiaSpider(scrapy.Spider):
    name = 'academia'
    start_urls = ['https://www.academia.edu/Directory/People']
    
    def parse(self,response):
        url1 = "https://www.academia.edu/Directory/People/91125..182249"
        response1 = get(url1,verify = False)
        link1 = []
        print('sani')
        if response1.status_code == 200:
            html_soup = BeautifulSoup(response1.text,'html.parser')
            # print(html_soup)
            data = html_soup.find_all('li',class_ = 'text-truncate')
            # print(data)
            for i in data:
                link1.append(i.find('a')['href'])
        print(link1)
        print(len(link1))
        link2 = []
        for i in [link1[0]]:
            url2 = i
            print(url2)
            response2 = get(url2,verify = False)
            if response2.status_code == 200:
                html_soup = BeautifulSoup(response2.text,'html.parser')
                data = html_soup.find_all('li',class_ = 'text-truncate')
                for j in data:
                    link2.append(j.find('a')['href'])
        # print(len(link2))
        print(link2)
        print(len(link2))
        link3 = []
        for i in [link2[0]]:
            url3 = i
            response3 = get(url3,verify = False)
            if response3.status_code == 200:
                html_soup = BeautifulSoup(response3.text,'html.parser')
                data = html_soup.find_all('li',class_ = 'text-truncate')
                for j in data:
                    link3.append(j.find('a')['href'])
        # print(len(link3))
        print(link3)
        print(len(link3))
        link4 = []
        for i in link3:
            q = {}
            url4 = i
            driver = webdriver.Chrome('./chromedriver') 
            driver.get(url4) 
            # response4 = get(url4,verify = False)
            # time.sleep(5) 
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            data = soup.find_all('div',{'class' : 'profile-user-info'})
            q['Name'] = data[0].find('li',{'class':'InlineList-item'}).text.replace("\n","").lstrip().rstrip()
            edu = data[0].find_all('div',{'class' : 'Affiliation-text--affiliation'})
            s = ""
            
            if len(edu)>0:
                a = edu[0].find_all('a',{'class' : 'u-tcGrayDarker'})
                for j in a:
                    s = s + ', ' + j.text.replace("\n","").lstrip().rstrip()
                sp = edu[0].find_all('span',{'class' : 'u-tcGrayDarker'})
                for j in sp:
                    s = s + ', ' + j.text.replace("\n","").lstrip().rstrip()    
            q['education'] = s
        
            follow = data[0].find('a',{'class' : 'js-profile-followers'})
            q['follower'] = follow.find('span').text.replace("\n","").lstrip().rstrip()
            followee = data[0].find('a',{'class' : 'js-profile-followees'})
            q['followee'] = followee.find('span').text.replace("\n","").lstrip().rstrip()
            coaut = data[0].find('a',{'class' : 'js-profile-coauthors'})
            if coaut is not None:
                q['co-auth'] = coaut.find('span').text.replace("\n","").lstrip().rstrip()    
            else:
                q['co-auth']=""
            social = soup.find('li', {'class' : 'js-social-profiles-container'})
            
            accout = ''
            if social is not None:
                acc = social.find_all('a')
                for i in acc:
                    accout = accout + ', ' +  i.get("href")
            q['social'] = accout; 
            yield q
            driver.close()
            # if response4.status_code == 200:
            #     html_soup = BeautifulSoup(response4.text,'html.parser')
                # data = html_soup.find_all('div',class_ = 'profile-user-info')
                # # print(data)
                # q.append(data[0].find('li',class_ = 'InlineList-item').text.replace("\n","").lstrip().rstrip())
                # edu = data[0].find_all('div',class_ = 'Affiliation-text--affiliation')
                # a = edu[0].find_all('a',class_ = 'u-tcGrayDarker')
                # # print(edu)
                # for j in a:
                #     q.append(j.text.replace("\n","").lstrip().rstrip())
                # sp = edu[0].find_all('span',class_ = 'u-tcGrayDarker')
                # for j in sp:
                #     q.append(j.text.replace("\n","").lstrip().rstrip())
                
                # follow = data[0].find('a',class_ = 'js-profile-followers')
                # q.append(follow.find('span').text.replace("\n","").lstrip().rstrip())
                # followee = data[0].find('a',class_ = 'js-profile-followees')
                # q.append(followee.find('span').text.replace("\n","").lstrip().rstrip())
                # coaut = data[0].find('a',class_ = 'js-profile-coauthors')
                # q.append(coaut.find('span').text.replace("\n","").lstrip().rstrip())
                # social = html_soup.find_all('li',class_ = 'js-social-profiles-container')
                # print(social)
                # linkurl = html_soup.find_all('script')[9]
                
                # d = html_soup.find('div',{"id": "site"})
                # print(d.find_all('script')[1])
                # print(q)
                
                # print(data)
                
        # print(len(link3))
