# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 15:52:14 2022

@author: DE001E02544
"""
import pandas as pd
import time
import requests
import logging
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from msedge.selenium_tools import Edge
from msedge.selenium_tools import EdgeOptions


class stadium_Scraper():
    
    
    
    def __init__(self):
        ###Set logger###
        self.logger = logging.Logger('stadium scraper')
        self.fh = logging.FileHandler("../log/stadiums.log")
        self.fh.setLevel(logging.INFO)
        self.fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        
        
    def get_data(self):
        link_list = open("../data/link_list.txt", "r")
        urls = link_list.read()
        url_list = urls.split(",")
        link_list.close()
        result_list = []
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument('disable-gpu')
        driver = Edge(executable_path="..\webdriver\msedgedriver.exe",options=edge_options)
        driver.maximize_window()
        url_list = list(dict.fromkeys(url_list))
        for url in url_list:
            try:
                driver.get("https://www.transfermarkt.de"+url)
                time.sleep(3)
                name = driver.find_elements_by_class_name("profilheader")[1].find_elements_by_tag_name("tr")[0].find_element_by_tag_name("td").get_attribute('innerHTML').lower()
                street = driver.find_elements_by_class_name("profilheader")[1].find_elements_by_tag_name("tr")[1].find_element_by_tag_name("td").get_attribute('innerHTML').lower()
                zip_code = driver.find_elements_by_class_name("profilheader")[1].find_elements_by_tag_name("tr")[2].find_element_by_tag_name("td").get_attribute('innerHTML').lower().split("&nbsp;")[0]
                city = driver.find_elements_by_class_name("profilheader")[1].find_elements_by_tag_name("tr")[2].find_element_by_tag_name("td").get_attribute('innerHTML').lower().split("&nbsp;")[1]
                result_list.append({'name':name,'street':street,'zip_code':zip_code,'city':city})
                result_frame = pd.DataFrame(result_list)
                result_frame.to_csv(path_or_buf='../result/stadium_list.csv',index=False,encoding='utf-8')
            except Exception as e:
                self.logger.error("Error getting data from " + url)
                self.logger.error(traceback.format_exc())

stad_scraper = stadium_Scraper()
links = stad_scraper.get_data()