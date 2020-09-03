---
images:
  - https://images.unsplash.com/photo-1421789665209-c9b2a435e3dc?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=5b1016b885e7438c4633109d77368d4d&auto=format&fit=crop&w=1651&q=80
  - https://images.unsplash.com/photo-1445962125599-30f582ac21f4?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=38c096c472ba616dc4e8e76a8069c97a&auto=format&fit=crop&w=668&q=80
  - https://images.unsplash.com/photo-1504626835342-6b01071d182e?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=975855d515c9d56352ee3bfe74287f2b&auto=format&fit=crop&w=1651&q=80
  - https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=468a8c18f5d811cf03c654b653b5089e&auto=format&fit=crop&w=1650&q=80
  - https://images.unsplash.com/photo-1506291318501-948562d765d7?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=71ad8e3b7b4bd210182ed5e5c024903b&auto=format&fit=crop&w=1650&q=80
  - https://images.unsplash.com/photo-1500370414137-9201565cf099?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=95e700b9e28eb7ed7b5769c823741126&auto=format&fit=crop&w=668&q=80
  - https://images.unsplash.com/photo-1500402448245-d49c5229c564?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=f19c590b253f803a7f9b643c59017160&auto=format&fit=crop&w=1650&q=80
---
# StockAdvisorSystem

<img src="/images/stockmain.jpg">  

&nbsp;&nbsp;본 프로그램은 주식 중개소로 운영되는, HTML로 작성된 사이트를 위주로 크롤링 기법을 적용하여 얻은 주가정보, 제무재표, 차트, 투자의견 등을 종합하여 기술적 지표를 도출해 궁극적으로 사용자의 투자 판단에 도움을 주는 조언들과 포트폴리오를 만들어 내는데 목적을 두는 프로그램을 설계한다.


세부사항  
-------
+ 사용언어 : python, MySQL
+ 참고 사이트 : [온라인 기업정보](https://navercomp.wisereport.co.kr/)
+ 주요 개발환경 : Windows7 (32bit)

>※ 업데이트 된 날짜 목록
> 1. 8월 23일 : 최초 등록
> 2. 8월 25일 : 리소스 추가
> 3. 8월 28일 : DBSetter 추가, Scrapper 파트 중 main table데이터 크롤링 코드 적용
> 4. 9월 2일 : GUI 일부 변경. + 리스트의 항목을 불러오는 기능 추가

<div class="card-columns">
    {% for img in page.images %}
    <div class="card">
        <img class="card-img-top" src="{{ img }}" />
    </div>
    {% endfor %}
</div>
