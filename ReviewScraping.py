# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:35:38 2019

@author: Raamki007
"""
import pandas as pd
import requests
import csv
import time
import bs4
from bs4 import BeautifulSoup


url="https://www.tripadvisor.com/Hotel_Review-g60982-d86973-Reviews-Aqua_Pacific_Monarch-Honolulu_Oahu_Hawaii.html"
headers={'User-Agent':'Mozilla/5.0'}

page=requests.get(url, headers=headers)
soup=BeautifulSoup(page.text,'html.parser')

customer_name=[]
customer_review=[]
customer_review_title=[]
customer_date_of_stay=[]
customer_contribution=[]
customer_rating=[]
customer_review_date=[]
ref_list=[]

#url list for reference
url_list=[]

def hotel_name(soup1):
    for i in soup1.find('h1',class_='hotels-hotel-review-atf-info-parts-Heading__heading--2ZOcD'):
        return str(i)

def hotel_rating(soup1):
    for i in soup1.find('span',class_='hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA'):
        return str(i)

def cus_name(soup1):
    attrs={'class':'social-member-event-MemberEventOnObjectBlock__event_type--3njyv'}
    for i in soup1.find_all('div',attrs=attrs):
        customer_review_date.append((i.text[(i.text).index('review')+7:]).strip())
        customer_name.append((i.text[0:(i.text).index('wrote')-1]).strip())

def cus_review(soup1):
    attrs= {'class':'hotels-review-list-parts-ExpandableReview__reviewText--3oMkH'}    
    for i in soup1.find_all('q',attrs=attrs):
        customer_review.append(i.text)
        
def cus_review_title(soup1):
    attrs={'class':'hotels-review-list-parts-ReviewTitle__reviewTitle--2Fauz'}
    for i in soup1.find_all('div',attrs=attrs):
        customer_review_title.append(i.text)

def date_of_stay(soup1):
    attrs={'class':'hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H'}
    for i in soup1.find_all('div',attrs=attrs):
        attrs1={'class':'hotels-review-list-parts-EventDate__event_date--CRXs4'}
        flag=0
        for j in i.find_all('span',attrs=attrs1):
            flag=1
            customer_date_of_stay.append(j.text[13:].strip())
        if flag==0:
            customer_date_of_stay.append('Data Not available')

def cus_contribution(soup1):
    attrs={'class':'social-member-MemberHeaderStats__event_info--30wFs'}
    for i in soup1.find_all('div',attrs=attrs):
        for j in i.find('span',attrs={'class':'social-member-MemberHeaderStats__stat_item--34E1r'}):
            customer_contribution.append(j.text.split(" ")[0])
    
def cus_rating(soup1):
    attrs={'class':'hotels-review-list-parts-RatingLine__bubbles--1oCI4'}
    for i in soup1.find_all('div',attrs=attrs):
        ref_list.append(i.span['class'][0]+i.span['class'][1])
        if i.span['class'][0]+i.span['class'][1]=='ui_bubble_ratingbubble_50':
            customer_rating.append('5')
        elif i.span['class'][0]+i.span['class'][1]=='ui_bubble_ratingbubble_40':
            customer_rating.append('4')
        elif i.span['class'][0]+i.span['class'][1]=='ui_bubble_ratingbubble_30': 
            customer_rating.append('3')
        elif i.span['class'][0]+i.span['class'][1]=='ui_bubble_ratingbubble_20':
            customer_rating.append('2')
        else:
            customer_rating.append('1')
        

cus_name(soup)
cus_review(soup)
cus_review_title(soup)
date_of_stay(soup)
cus_contribution(soup)
cus_rating(soup)
Hotel_name=hotel_name(soup)
Hotel_rating=hotel_rating(soup)

for i in soup.findAll('a',class_="pageNum"):
    max=i.text

max=int(max)

for num in range(2,max+1):
    time.sleep(3)
    for i in soup.find('a',class_='ui_button nav next primary'):
        next_page=i.parent['href']

    next_page_url="https://www.tripadvisor.com"+next_page
    headers={'User-Agent':'Mozilla/5.0'}

    page=requests.get(next_page_url, headers=headers)
    soup=BeautifulSoup(page.text,'html.parser')
    
    cus_name(soup)
    cus_review(soup)
    cus_review_title(soup)
    date_of_stay(soup)
    cus_contribution(soup)
    cus_rating(soup)
    url_list.append(next_page_url)
    if '2016' in customer_review_date[-1]:
        break



d = {'Customer_Name':customer_name,'Customer_Contribution':customer_contribution,'Customer_Review_Date':customer_review_date,'Customer_Date_of_Stay':customer_date_of_stay,'Customer_Review_Title':customer_review_title,'Customer_Rating':customer_rating,'Customer_Review':customer_review}
df = pd.DataFrame(d)
df['Hotel_Name']=Hotel_name
df['Hotel_Rating']=Hotel_rating

bool_list=[]
#End of code 
for i in df['Customer_Date_of_Stay']:
    if '2017' in i or '2018' in i or '2019' in i:
        bool_list.append(True)
    else:
        bool_list.append(False)
Final_df=df[bool_list]

Final_df.to_excel("Aqua Pacific Monarch.xlsx")    

 
    