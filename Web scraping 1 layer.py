#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


# In[6]:


def lastpagenum():
    r = requests.get(r'https://www.tratencongty.com/')
    soup = BeautifulSoup(r.content, 'html.parser')
    lastpage=soup.find("ul",{"class":"pagination"}).find_all("a")[-1]
    href = lastpage.get("href")
    t = re.findall('[0-9]+', href)
    return int(t[0]) + 1
lastpagenum = lastpagenum()


# In[7]:


Ten_cong_ty = []
Ma_so_thue = []
Dai_dien_phap_luat = []
Dia_chi = []
def scrapeweb():
    with requests.Session() as req:
        for pagenum in range(1,lastpagenum):
            #print(f"Extracting Page# {pagenum}")
            r = requests.get(f'https://www.tratencongty.com/?page={pagenum}')
            soup = BeautifulSoup(r.content, 'html.parser')
            s = soup.find_all('div', class_="search-results")
            pageps = soup.find_all('p')
            for result in s:
                Tencongty = result.find('a', text = re.compile('[A-Z]')).text
                #print(Tencongty)
                Ten_cong_ty.append(Tencongty)
                Masothue = result.find('a', text = re.compile('^[0-9]')).text
                #print(Masothue)
                Ma_so_thue.append(Masothue)
            for page in pageps:
                x = page.text.split(':') #split at : to get values of each category
                y = [re.sub(r"[\n\r]*", "", itemx) for itemx in x] #get rid of newline
                z = [j.strip() for j in y] #remove trailing and leading spaces
                Daidienphapluat = z[2].replace(' Địa chỉ',"")
                Dai_dien_phap_luat.append(Daidienphapluat)
                Diachi = z[3]
                Dia_chi.append(Diachi)

scrapeweb()


# In[10]:


data = pd.DataFrame({'Tên công ty':Ten_cong_ty,
                        'Mã số thuế': Ma_so_thue,
                        'Đại diện pháp luật':Dai_dien_phap_luat,
                        'Địa chỉ':Dia_chi})


# In[ ]:




