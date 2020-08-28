#!/usr/bin/env python
# coding: utf-8

import sys
import requests
import socket
import time

from bs4 import BeautifulSoup

# User custom ExceptionClass list
# return Exception code
#####################################################
class NotFoundExcpetion(Exception):                 # Exception code : CASE_NOT_FOUND
    def __init__(self):                             #
        super().__init__("주소를 찾을수 없습니다. ")  #
                                                    # network connect failure : CASE_CONNECT_FAILED
                                                    #
#####################################################
def getURL(sig, code_num):
    pageNews =          "https://finance.naver.com" + "/news/"
    pageMainPrice =     "https://finance.naver.com/item/sise.nhn?code=" + code_num      # main page

    defineAddress =             "https://navercomp.wisereport.co.kr/company/"       # online company info site
    pageCompanyStatus =         defineAddress + "c1010001.aspx?cmp_cd=" + code_num
    pageCompanyOverview =       defineAddress + "c1020001.aspx?cmp_cd=" + code_num
    pageFinancialanalysis =     defineAddress + "c1030001.aspx?cmp_cd=" + code_num
    pageInvestmentIndicator =   defineAddress + "c1040001.aspx?cmp_cd=" + code_num
    pageConsensus =             defineAddress + "c1050001.aspx?cmp_cd=" + code_num
    pageIndustryAnalysis =      defineAddress + "c1060001.aspx?cmp_cd=" + code_num
    pageSectorAnalysis =        defineAddress + "c1090001.aspx?cmp_cd=" + code_num
    pageEquitystatus =          defineAddress + "c1070001.aspx?cmp_cd=" + code_num

    try:
        if (sig == 1):
            return pageCompanyStatus
        elif (sig == 2):
            return pageCompanyOverview
        elif (sig == 3):
            return pageFinancialanalysis
        elif (sig == 4):
            return pageInvestmentIndicator
        elif (sig == 5):
            return pageConsensus
        elif (sig == 6):
            return pageIndustryAnalysis
        elif (sig == 7):
            return pageSectorAnalysis
        elif (sig == 8):
            return pageEquitystatus
        elif (sig == 9):
            return pageMainPrice
        elif (sig == 10):
            return pageNews
        else:
            raise NotFoundExcpetion

    except NotFoundExcpetion as e:
        send = "CASE_NOT_FOUND"
        print("오류 발생.", e)
        return send

class URLcrawlingInfoObject:                                   # object for crawling work
    def __init__(self, url):
        super().__init__()
        self.settingCrawlingModule(url)

    def settingCrawlingModule(self, url):                      # create soup object here
        try:
            targetURLCrawl =    requests.get(url, timeout=5)
            soup =              BeautifulSoup(targetURLCrawl.content, "html.parser")
            self.code = soup
        except requests.HTTPError as e:                        # I need to check the connecting network
            print("오류 발생", e)
            self.code = "CASE_CONNECT_FAILED"                  # when the newtwork connection failed, return use database load signal

    # 딕셔너리 형식으로 리턴
    def crawlingmainStockInfo(self, bs):                       # 메인테이블
        list_th =           bs.find_all("th", {'class':'title'})
        list_strong =       bs.find_all("strong", {'class':'tah p11'})
        list_span =         bs.find_all("span", {'class':'tah p11'})
        ch = bs.find_all("span", {'class':'blind'})            # 상승, 하락에 따라 처리를 바꿔야 하기에 그에 필요한 구별용 변수 ch를 선언함
        if ch[22].get_text() == "상승":
            list_span_01 =  bs.find_all("span", {'class':'tah p11 red01'})
        elif ch[22].get_text() == "하락":
            list_span_01 =  bs.find_all("span", {'class':'tah p11 nv01'})
        list_span_t =       bs.find_all("span",{'class':'p11'})

        result_th = []                                         # final list
        result_strong = []
        result_span_01 = []
        result_span = []
        result_span_t = []

        for i in list_th:                                      # 데이터 추출
            result_th.append(i.get_text().strip())

        for j in list_strong:
            result_strong.append(j.get_text().strip())

        for k in list_span_01:
            result_span_01.append(k.get_text().strip())
            if len(result_span_01) == 2:  # 인덱스[1] 뒤의 값들을 쓸 일이 없기 때문에 리스트에 포함시키지 않음
                break;

        for l in list_span:
            result_span.append(l.get_text().strip())

        m = 19
        for m in range(19, len(list_span_t)):
            result_span_t.append(list_span_t[m].get_text().strip())
            if m == (19 + 3):
                break;
            m += 1

        result_th = list(filter(None, result_th))
        result_strong = list(filter(None, result_strong))
        result_span_01 = list(filter(None, result_span_01))
        result_span = list(filter(None, result_span))
        result_span_t = list(filter(None, result_span_t))

        res_dict = {'r1':result_th,
                    'r2':result_strong,
                    'r3':result_span_01,
                    'r4':result_span,
                    'r5':result_span_t}

        return res_dict

    def crawlingCompanyStatus(self, bs):        # 기업현황
        pass

    def crawlingCompanyOverview(self, bs):      # 기업개요
        pass

    def crawlingFinancialanalysis(self, bs):    # 재무분석
        pass

    def crawlingInvestmentIndicator(self, bs):  # 투자지표
        pass

    def crawlingConsensus(self, bs):            # 컨센서스
        pass

    def crawlingIndustryAnalysis(self, bs):     # 업종분석
        pass

    def crawlingSectorAnalysis(self, bs):       # 섹터분석
        pass

    def crawlingEquitystatus(self, bs):         # 지분현황
        pass

if __name__ == '__main__':
    print("처리 선택 : (0을 입력하면 종료됨.)")
    i = input()

    if i == '0':
        exit(0)
    elif i == '1':
        res = getURL(1, "005930")       # 삼성전자 정보 페이지를 이용해 테스트
    elif i == '2':
        res = getURL(2, "005930")
    elif i == '3':
        res = getURL(3, "005930")
    elif i == '4':
        res = getURL(4, "005930")
    elif i == '5':
        res = getURL(5, "005930")
    elif i == '6':
        res = getURL(6, "005930")
    elif i == '7':
        res = getURL(7, "005930")
    elif i == '8':
        res = getURL(8, "005930")
    elif i == '9':
        res = getURL(9, "005930")
    elif i == '10':
        res = getURL(10, "005930")

    if res == "CASE_NOT_FOUND":
        exit(-1)

    tester = URLcrawlingInfoObject(res)
    if tester.code == "CASE_CONNECT_FAILED":
        exit(-1)

    data_check = tester.crawlingmainStockInfo(tester.code)   # 딕셔너리 받아옴

    print(type(data_check), len(data_check))
    print(data_check)
