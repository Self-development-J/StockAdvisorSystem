import pandas

if __name__ == '__main__':
    print(pandas.Series)

    # series 객체 생성 방식 -> 키 값 형시그올 출력됨
    kakao = pandas.Series([1000,2000,3000,4000], index=['2016-02-19', '2016-02-18', '2016-02-17', '2016-02-16'])
    print(kakao)

    #dataFrame 생성방식 -> 
    raw_data = {'col0': [1, 2, 3, 4], 'col1': [10, 20, 30, 40], 'col2': [100, 200, 300, 400]}

    data = pandas.DataFrame(raw_data)
    print(data)
    # 칼럼, 인덱스 추가 버전 dataFrame
    date = ['2016-02-19', '2016-02-18', '2016-02-17', '2016-02-16','2016-02-28']
    daeshin = {'open':  [11650, 11100, 11200, 11100, 11000],
           'high':  [12100, 11800, 11200, 11100, 11150],
           'low' :  [11600, 11050, 10900, 10950, 10900],
           'close': [11900, 11600, 11000, 11100, 11050]}

    daeshin_day = pandas.DataFrame(daeshin, columns=['open', 'high', 'low', 'close'], index=date)
    print(daeshin_day)

    # DataFrame 칼럼과 인덱스 값 확인
    print(daeshin_day.columns)
    print(daeshin_day.index)
