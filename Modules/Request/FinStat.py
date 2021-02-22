import pprint
from xml.etree import ElementTree
from urllib import request
from io import BytesIO
from zipfile import ZipFile
import json
from bs4 import BeautifulSoup

# 사용 API : Opendart API

# dataRequest methods
# get_data :        공시대상 회사의 재무제표를 가져옴
# get_corp_code :   공시대상 회사 번호 8자리를 가져옴

class dataRequest:
    CRTFC_KEY="1ff61ab354720a47c4f0c10f8335f2f1241b8129"

    def __init__(self):
        super().__init__()
        print("생성완료")
        print("인증 키"+self.CRTFC_KEY)

    def get_data(self, code):
        # CRTFC_KEY :   인증키
        # corp_code :   공시대상 회사 번호 8자리
        # bsns_year :   사업연도
        # reprt_code :  보고서 코드 (11013:1분기보고서, 11012:반기보고서, 11014:3분기보고서, 11011:사업보고서)
        # fs_div :      개별/연결 구분(CFS:연결재무제표, OFS:재무제표)
        
        corp_code=code
        bsns_year="2019"
        reprt_code="11011"
        fs_div="CFS"

        url="https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key={}&corp_code={}&bsns_year={}&reprt_code={}&fs_div={}".format(self.CRTFC_KEY, corp_code, bsns_year, reprt_code, fs_div)

        req=request.urlopen(url)

        path=json.loads(req.read())

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(path)

        print(pp)

    def get_corp_code(self, code):
        url = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={}".format(self.CRTFC_KEY)
        data = request.urlopen(url)

        with ZipFile(BytesIO(data.read())) as zipfile:
            zipfile.extractall('c:\\corpCode')

        xmlTree = ElementTree.parse('c:\\corpCode\corpCode.xml')

        root = xmlTree.getroot()
        list = root.findall('list')

        for i in range(0, len(list)):
            if list[i].findtext('stock_code') == code:
                print(list[i].findtext('corp_code'))
                print(list[i].findtext('corp_name'))
                print(list[i].findtext('stock_code'))
                print(list[i].findtext('modify_date'))

                return list[i].findtext('corp_code')


if __name__=='__main__':
    res = dataRequest()
    code = res.get_corp_code("007070")
    res.get_data(code)