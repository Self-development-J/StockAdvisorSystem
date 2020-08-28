import sys
import pymysql

def get_sqlsig(sig):
    sig_createDB = "CREATE DATABASE stockadvisor_b;"
    sig_createTB = '''CREATE TABLE sise (
    name string(20) NOT NULL, price int(20) NOT NULL, previousday int(20) NOT NULL
    );'''
    sig_createTB_test = '''
    CREATE TABLE sise_test name string(20) NOT NULL, Code int(6) NOT NULL,
    Price int(10) NOT NULL, Previous_day int(10) NOT NULL, Return double(10) NOT NULL, 52Weeks_Highest int(10) NOT NULL,
    52Weeks_Lowest int(10) NOT NULL, Face_value int(10) NOT NULL, Volume int(10) NOT NULL, Transaction_price int(10) NOT NULL,
    Market_cap int(10) NOT NULL, 52-week beta double(10) NOT NULL, Number_of_shares_issued double(5) NOT NULL,
    Current_ratio double(10) NOT NULL, Foreign_ownership_ratio double(10) NOT NULL, Yield_1M double(10) NOT NULL,
    Yield_3M double(10) NOT NULL, Yield_6M double(10) NOT NULL, Yield_1Y double(10) NOT NULL, PRIMARY KEY(name);
    '''
    #
    # 순서대로 주가, 전일대비, 수익룰, 52주 최고, 52주 최저, 액면가, 거래량, 거래대금, 시가총액, 52주 베타, 발행주식수, 유동비율, 외국인 지분율, 수익률(1달, 3달, 6달, 1년)
    #
    sig_selectTB_test = "SELECT * FROM sise_test;"

    if sig == '1':
        return sig_createTB_test
    elif sig == '2':
        return sig_selectTB_test

if __name__ =='__main__':

    try:
        db=pymysql.connect( host = "localhost",
                            user="StockAdvisor_tester",
                            password="darksouls3",
                            db="stockadvisor_b",
                            charset="utf8")      # changed mysql) password => authentication_string
    except pymysql.err.OperationalError as e:
        print("연결이 거부되었습니다.", e)
        exit(-1)

    cur = db.cursor()
    cur.execute(get_sqlsig(1))
    cur.execute(get_sqlsig(2))
