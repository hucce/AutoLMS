import pandas as pd
import numpy as np
import re
import csv
import time
import os
import requests
import datetime

#브라우저 제어
from selenium import webdriver
#페이지 로드
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

def AutoLMS(iD, passWord, classNames):
    driver = webdriver.Chrome('./chromedriver')

    #기본 LMS
    loadUrl = 'https://learn.hoseo.ac.kr/'
    driver.get(loadUrl)

    time.sleep(0.5)
    # ID
    input_box = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/div/div[1]/div[2]/div[1]/form/div[1]/input')
    input_box.send_keys(iD)

    # Password
    input_box = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/div/div[1]/div[2]/div[1]/form/div[2]/input')
    input_box.send_keys(passWord)
    
    # 버튼
    btn = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/div/div[1]/div[2]/div[1]/form/div[3]/button')
    btn.send_keys(Keys.RETURN)
    time.sleep(2) 
    
    linkList = []

    datas = driver.find_elements_by_class_name('course_box')

    # 수업 리스트
    for data in datas:
        for className in classNames:
            if className in data.text:
                linkList.append(data)
                
    btn = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/button')
    btn.click()
    time.sleep(1)

    for link in linkList:
        link.click()
        time.sleep(2)
        # Vod 리스트 확인
        vods = driver.find_elements_by_class_name('mod-indent-outer')
        for vod in vods:
            vodCom = vod.find_elements_by_css_selector("img.smallicon")
            if len(vodCom) > 0:
                src = vodCom[0].get_attribute("src")
                check = src[len(src) - 1]
                if 'n' in check:
                    vodClick = vod.find_elements_by_css_selector("img.activityicon")
                    playTime = vod.find_elements_by_css_selector("span.text-info")
                    playTime = playTime[0].text.split(', ')[1]
                    x = time.strptime(playTime,'%M:%S')
                    wait = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
                    wait += 10

                    vodClick[0].click()
                    time.sleep(2)

                    # 이제 영상을 클릭한다.
                    print(driver)
                    main = driver.window_handles
                    for handle in main: 
                        if handle != main[0]:
                            driver.switch_to_window(handle)
                            #driver.close()

                    video = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/video')
                    video.click();

                    time.sleep(wait)
                    # 팝업창 끄기
                    driver.close()
                    time.sleep(2)
                    driver.switch_to_window(driver.window_handles[0])
                    print("교육 하나 완료")
        driver.back()
        time.sleep(2)

AutoLMS('20215349', 'gjals9wkd!3', ['폭력예방', '안전교육'])