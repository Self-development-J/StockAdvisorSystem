#!/usr/bin/env python
# coding: utf-8

import sys
import requests
from bs4 import BeautifulSoup

def getURL(sig, code_num):

    naver_main =    "https://finance.naver.com"                             # main page
    naver_news =    naver_main + "/news/"
    
    defineAddress = "https://navercomp.wisereport.co.kr/company/"           # online company info site
    page1 =         defineAddress + "c1010001.aspx?cmp_cd=" + code_num      
    page2 =         defineAddress + "c1020002.aspx?cmp_cd=" + code_num
    page3 =         defineAddress + "c1030002.aspx?cmp_cd=" + code_num
    page4 =         defineAddress + "c1040002.aspx?cmp_cd=" + code_num
    page5 =         defineAddress + "c1050002.aspx?cmp_cd=" + code_num
    page6 =         defineAddress + "c1060002.aspx?cmp_cd=" + code_num
    page7 =         defineAddress + "c1070002.aspx?cmp_cd=" + code_num
    
    try:
        if (sig == 1):
            return naver_item
        elif (sig == 2):
            return naver_item
        elif (sig == 3):
            return naver_item
        elif (sig == 4):
            return naver_item
        elif (sig == 5):
            return naver_item
        elif (sig == 6):
            return naver_item
        elif (sig == 11):
            return naver_news
        else:
            raise NotFoundExcpetion("주소를 가져오는데 실패했습니다. 에러처리를 시작합니다..")
    except NotFoundExcpetion as e:
        send = "CASE_NOT_FOUND"
        print("오류 발생.", e)
        return send
        
class crawling():
    def __init__(self, url):
        super().__init__()
        targetURLCrawl = requests.get(url)
        soup = BeautifulSoup(targetURLCrawl.content, "html.parser")
            
    def crawlingmainStockInfo(url):
        pass
    
    def crawlingCompanyStatus(url):
        pass
    
    def crawlingCompanyOverview(url):
        pass
    
    def crawlingFinancialanalysis(url):
        pass
    
    def crawlingInvestmentIndicator(url):
        pass
    
    def crawlingConsensus(url):
        pass
    
    def crawlingIndustryAnalysis(url):
        pass
    
    def crawlingSectorAnalysis(url):
        pass
    
    def crawlingItem(url):
        pass
    

if __name__ == '__main__':
    i = 0
    
    while True:
        print("디버그 코드 입력 : ", end = " ")
        sig = input()
        
        if(sig != "6ATZTGMS8"):
            print("코드가 틀렸습니다. 다시 확인해 주세요.")
            continue;
        elif(sig == "exit" or sig == "EXIT" or sig == "Exit"):
            print("프로그램 종료")
            sys.exit(0)
        
        break;
        
    print("1. 네이버 금융 뉴스, 2. 네이버 금융 시세, 3. 코스피 지수, 4. 코스닥 지수, 5. 종목정보(GS리테일)")
    print("URL 연결을 확인합니다. 시그널을 입력해 주세요 : ", end = " ")
    
    i = input()
    
    fi_main = requests.get(getURL(int(i)))
    soup = BeautifulSoup(fi_main.content, "html.parser")

    if (int(i) == 1):
        news = soup.find_all(["a", "href"])
        n = 0
        for n in range(n, len(news)):
            print(news[n].text)
    elif (int(i) == 2):
        sise = soup.find_all(["a", "span", "img"])
        result = []
        n = 0
        
        for n in range(n, len(sise)):
            if(sise[n].text == "인기 검색 종목"):
                n += 2
                flag = n + 30
                for n in range(n, flag):
                    result.append(sise[n].text)
                    
                break
                
        #print(soup)
        print(result)
        
    elif (int(i) == 3):
        KOSPI = soup.find_all(["a", "span", "img"])
        n = 0
        for n in range(n, len(KOSPI)):
            print(KOSPI[n].text)
    elif (int(i) == 4):
        KOSDAQ = soup.find_all(["a", "href"])
        n = 0
        for n in range(n, len(KOSDAQ)):
            print(news[n].text)
    elif (int(i) == 5):
        pass
    elif (int(i) == 6):
        main = soup.find_all(["a", "href"])
        n = 0
        for n in range(n, len(main)):
            print(main[n].text)