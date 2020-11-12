# coding: utf-8
import re

import requests
import json

from bs4 import BeautifulSoup

# User custom ExceptionClass list
# custom raise Exception code is here. 
class WrongItemNumberException(Exception):
    def __init__(self):
        super().__init__("종목번호가 잘못되었습니다!")
        

def getURL(sig, item_num = "005930"):

    defineAddress = "https://navercomp.wisereport.co.kr/company/"       # online company info site
    links = {
        1:defineAddress + "c1010001.aspx?cmp_cd=" + item_num,
        2:defineAddress + "c1020001.aspx?cmp_cd=" + item_num,
        3:defineAddress + "c1030001.aspx?cmp_cd=" + item_num,
        4:defineAddress + "c1040001.aspx?cmp_cd=" + item_num,
        5:defineAddress + "c1050001.aspx?cmp_cd=" + item_num,
        6:defineAddress + "c1060001.aspx?cmp_cd=" + item_num,
        7:defineAddress + "c1090001.aspx?cmp_cd=" + item_num,
        8:defineAddress + "c1070001.aspx?cmp_cd=" + item_num,
        9:"https://finance.naver.com/item/sise.nhn?code=" + item_num,               # main page
        10:"https://m.stock.naver.com/item/main.nhn#/stocks/" + item_num + "/news"  # call to mobile page in newspeed screen
    }

    try:
        if sig == 0:
            exit(0)
        else:
            return links[sig]

    except KeyError as e:
        print("잘못된 매개인자가 전달되었다. 다시 입력." + "(전달된 인자: {})".format(sig))
        retype = int(input("처리 선택(0을 입력하면 종료됨.) : "))
        return getURL(retype, item_num)

class URLcrawlingInfoObject:                                   # object for crawling work
    __resultOfSoup = None                                      # saving result of soup

    def __init__(self, url):
        super().__init__()
        self.settingCrawlingModule(url)

    def settingCrawlingModule(self, url):                      # create soup object here
        try:
            targetURLCrawl =    requests.get(url, timeout=5)
            soup =              BeautifulSoup(targetURLCrawl.content, "html.parser")
            check = soup.find_all("title")
            for i in check:
                if i.text == "네이버 금융":             # if target site's code number is wrong
                    raise WrongItemNumberException
                else:
                    break

            self.__resultOfSoup = soup
            # targetJson =        targetURLCrawl.json()
            # print(targetJson)
        except requests.HTTPError as e:                        # I need to check the connecting network
            print("해당 사이트의 HTTP에 문제가 있음! 주소를 다시 확인해주기 바람!")
            exit(-1)
        except requests.ConnectionError as e1:
            print(e1)
            exit(-2)
        except requests.exceptions.ReadTimeout as e2:
            print(e2)
            exit(-3)
        except WrongItemNumberException as e3:
            print(e3)
            exit(-4)

    def getResultOfSoup(self):
        return self.__resultOfSoup

    # From here on we will use the soup object
    # return type of dict
    def crawlingmainStockInfo(self, bs):        # 메인테이블
        list_th =           bs.find_all("th", {'class':'title'})        # 속성명
        list_strong =       bs.find_all("strong", {'class':'tah p11'})  # 현재가
        list_span =         bs.find_all("span", {'class':'tah p11'})    # 전일대비, 등락률
        ch =                bs.find_all("span", {'class':'blind'})      # 상승, 하락에 따라 처리를 바꿔야 하기에 그에 필요한 구별용 변수 ch를 선언함
        list_span_01 =      None
        result_color =      None

        result_th =         []                                         # final list
        result_strong =     []
        result_span_01 =    []
        result_span =       []
        result_span_t =     []

        for l in ch:
            if l.get_text() == "상승":
                list_span_01 =  bs.find_all("span", {'class':'tah p11 red01'})
                result_color = "red"
                break
            elif l.get_text() == "하락":
                list_span_01 =  bs.find_all("span", {'class':'tah p11 nv01'})
                result_color = "blue"
                break

            list_span_01 =  bs.find_all("span", {'class':'tah p11'})    # 보합 처리, 개장전 등의 경우
            result_color = "grey"

        list_span_t =       bs.find_all("span",{'class':'p11'})         # 시세표 중 52주 최고 ~

        for i in list_th:                                               # 데이터 추출
            result_th.append(i.get_text().strip())

        for j in list_strong:
            result_strong.append(j.get_text().strip())

        for k in list_span_01:                                          
            result_span_01.append(k.get_text().strip())
            if len(result_span_01) == 2:                                # 인덱스[1] 뒤의 값들을 쓸 일이 없기 때문에 리스트에 포함시키지 않음
                break

        for l in list_span:
            result_span.append(l.get_text().strip())

        m = 19
        for m in range(19, len(list_span_t)):
            result_span_t.append(list_span_t[m].get_text().strip())
            if m == (19 + 3):
                break;
            m += 1

        result_th =         list(filter(None, result_th))
        result_strong =     list(filter(None, result_strong))
        result_span_01 =    list(filter(None, result_span_01))
        result_span =       list(filter(None, result_span))
        result_span_t =     list(filter(None, result_span_t))
        
        res_dict = {'r1':result_th,
                    'r2':result_strong,
                    'r3':result_span_01,
                    'r4':result_span,
                    'r5':result_span_t,
                    'r6':result_color}

        return res_dict

    def crawlingCompanyStatus(self):        # 기업현황
        pass

    def crawlingCompanyOverview():      # 기업개요
        pass

    def crawlingFinancialanalysis(self):    # 재무분석
        dict_data = []
        try:
            with open("target_result.json", "r", encoding="utf-8") as tar:
                target = json.load(tar)
                
            target2 = json.loads(target)
            js = json.dumps(target, indent="\t")

            i = 0
            for i in range(len(target2['DATA'])):
                dict_attribute = {}

                dict_attribute['ACC_NM'] = target2['DATA'][i]['ACC_NM']
                dict_attribute['DATA1'] = target2['DATA'][i]['DATA1']
                dict_attribute['DATA2'] = target2['DATA'][i]['DATA2']
                dict_attribute['DATA3'] = target2['DATA'][i]['DATA3']
                dict_attribute['DATA4'] = target2['DATA'][i]['DATA4']
                dict_attribute['DATA5'] = target2['DATA'][i]['DATA5']

                dict_data.append(dict_attribute)

            return dict_data

        except FileNotFoundError as e:
            print("파일을 찾을 수 없음. 대상파일: {}".format("target_result.json"))
            exit(-1)
        finally:
            pass

    def crawlingInvestmentIndicator():  # 투자지표
        pass

    def crawlingConsensus():            # 컨센서스
        pass

    def crawlingIndustryAnalysis():     # 업종분석
        pass

    def crawlingSectorAnalysis():       # 섹터분석
        pass

    def crawlingEquitystatus():         # 지분현황
        pass

if __name__ == '__main__':

    i = int(input("처리 선택(0을 입력하면 종료됨.) : "))
    res = getURL(i, "005930")       # 삼성전자 정보 페이지를 이용해 테스트.
    print(res)
    print(type(res))

    tester = URLcrawlingInfoObject(res)

    data_check = tester.crawlingmainStockInfo(tester.getResultOfSoup())   # 딕셔너리 받아옴

    tester.crawlingFinancialanalysis()
    print(data_check)
