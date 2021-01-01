import sys
import pymysql
from pymysql import Connection
#####################################################
# 미완성 모듈입니다! 아직 사용할 수 없어요
#####################################################

def get_NameOftable(sig):       # 테이블 이름을 반환하는 용도
    sise = "sise"               # 테스트용


    t_main = "Stocks"                 # 메인 테이블
    t_sise = ""                 # 시세표
    t_fi_report = ""            # 재무제표
    t_companyInfo = ""          # 기업개요 (3)
    t_InvestmentIndicator = ""  # 투자지표 (4)

    if sig == 1:
        return t_sise
    elif sig == 2:
        return t_fi_report
    elif sig == 3:
        return t_companyInfo
    elif sig == 4:
        return t_InvestmentIndicator
    elif sig == 5:
        return t_main
    elif sig == 5882:
        return sise

def set_sqlConnect(sig):            # DB에 연결
    if sig == 1:
        base = "stockadvisor_b"
    elif sig == 2:
        base = "stockadvisor"

    res = pymysql.connect( host = "localhost",
                        user="StockAdvisor_tester",
                        password="darksouls3",
                        db=base,
                        charset="utf8")
    return res

def set_cursor(DBConnetion):
    cur = DBConnetion.cursor()
    return cur

def set_Stocks(DBConnetion, cursor, list):        # 인수로 넘겨받은 DB의 커넥션을 넘겨받으면 해당 종목의 메인 정보를 DB에 세팅
    cursor.execute("SHOW TABLES LIKE '{table}'".format(table = get_NameOftable(5)))
    res = cursor.fetchall()

    if len(res) == 0:               # table이 없는 경우 새로 생성
        cursor.execute('''
        CREATE TABLE {table} (name VARCHAR(15) NOT NULL, code VARCHAR(10), Present_price VARCHAR(10),
        Compared_to_the_previous_day VARCHAR(10), Fluctuation_rate VARCHAR(10), Volume VARCHAR(10),
        Transaction_price VARCHAR(10), Face_value VARCHAR(10), Asking_price VARCHAR(10),
        Bid_price VARCHAR(10), Full_family VARCHAR(10), Market_price VARCHAR(10),
        High_price VARCHAR(10), Low_price VARCHAR(10), Transaction_price VARCHAR(10),
        Upper_limit VARCHAR(10), Full-time_upper_limit VARCHAR(10), Lower_limit VARCHAR(10),
        Full-time_lower_limit VARCHAR(10), PER VARCHAR(10), EPS VARCHAR(10),
        52-week_high VARCHAR(10), 52_weeks_min VARCHAR(10), Market_cap VARCHAR(10),
        Number_of_listed_shares VARCHAR(10), Foreigners VARCHAR(10), Capital VARCHAR(10),
        PRIMARY KEY(name));
         '''.format(table=get_NameOftable(5)))

    cur.execute('''INSERT INTO {table} (name, code, Present_price, Compared_to_the_previous_day, Fluctuation_rate, Volume,
    Transaction_price, Face_value, Asking_price, Bid_price, Full_family, Market_price, High_price, Low_price, Transaction_price,
    Upper_limit, Full-time_upper_limit, Lower_limit, Full-time_lower_limit, PER, EPS, 52-week_high, 52_weeks_min,
    Market_cap, Number_of_listed_shares, Foreigners, Capital) VALUES('기아차','42750','550')'''.format(table=get_NameOftable(5)))

    Connection.commit()   #
    Connection.close()

if __name__ == '__main__':

    try:
        db= set_sqlConnect(1)

        cur = set_cursor(db)
        cur.execute("SHOW TABLES LIKE '{table}'".format(table = get_NameOftable(5882))) # sql: 테이블의 존재여부 확인
        res = cur.fetchall()

        if len(res) == 0:           # table이 없는 경우 새로 생성
            cur.execute("CREATE TABLE {table} (name VARCHAR(15) NOT NULL, price INT(10) previousday INT(10)), PRIMARY KEY(name));")
        else:
            cur.execute("INSERT INTO {table} (name, price, previousday) VALUES('기아차','42750','550')".format(table=get_NameOftable(5882)))
            cur.execute("SELECT * FROM {table}".format(table=get_NameOftable(5882)))
            chk = cur.fetchone()
            print(chk)

        db.commit()

    except pymysql.err.OperationalError as e:
        print("연결이 거부되었습니다.", e)
        exit(-1)

    db.close()
