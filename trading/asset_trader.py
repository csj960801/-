#########################################
######## 업비트 API 연동 및 거래지원 ########
#########################################

# 자산 매수, 손절 정보 로드
import time

import trade_lib as asset

# 매수 및 손절한 시간
import datetime

# BeautifulSoup 모듈은 html 파일에서 원하는 데이터를 파싱하는데 사용
# from bs4 import BeautifulSoup

# 정보 담고있는 웹 페이지 url 스크래핑
# 200 : 정상접속, 404 : 존재하지않는 페이지, 500 : 서버에러
# import requests

# 거래소 정보 정보 로드
import pyupbit as upbit

from IPython.display import clear_output

# 업비트 계정연동(업비트 로그인 -> 고객센터 -> open api안내 -> open api사용하기)
access=""
secret=""
upbit_access = upbit.Upbit(access, secret)

# 비트코인 현재가 정보 가져오기
def get_bit_price(ticker):
    present_price = upbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
    # print("비트코인 현재가: {0}".format(present_price))
    return present_price

# 업비트 잔고 조회
def get_my_deposit(ticker):
    deposit = upbit_access.get_balances()
    print(deposit)

    result = 0
    for d in deposit:
        print("잔고: {0}".format(d))  # api 사용허가 떨어지는 대로 분석 시작.
        if d["currency"] == ticker:
            if d["balance"] is not None:
                result = float(d["balance"])
            else:
                result = 0
    return result

# 업비트 평단가
def get_average(currency):
    balance = upbit_access.get_balances()
    print(balance)

    result = 0
    for b in balance:
        print("평단가: {0}".format(b))  # api 사용허가 떨어지는 대로 분석 시작.
        if b["currency"] == currency:
            if b["avg_buy_price"] is not None:
                result = float(b["avg_buy_price"])
            else:
                result = 0
    return result

# 거래시작
def trade_start():
    current_price = get_bit_price("KRW-BTC")  # 비트코인 현재가
    amount_btc = get_my_deposit("BTC")  # 비트코유 보유량
    btc_krw = current_price * amount_btc  # 비트코인 구입 평가 금액
    min_price = current_price  # 최소금액
    max_price = current_price  # 최대금액

    # +-5% 기준으로 거래
    while True:  # 프로그램 실행시키는대로 바로 루프 run

        # 비트코인 미보유시 시장가로 구매
        if get_average("BTC") <= 0:
            upbit_access.buy_market_order(ticker="KRW-BTC", price=current_price)  # 매수

        # 현재가보다 보유하고 있는 평균가가 높고, 잔고가 10000원 이상일 경우 추가 매수
        if current_price <= get_average("BTC") and int(get_my_deposit("KRW")) > 10000:  # 현재가 보다 매수한 코인 가격이 클 경우 매수상태로 변환
            print("매수 평균가: {0}".format(get_average("BTC")))

            # buy_market_order(ticker='KRW-BTC', price=100000)
            # KRW-BTC를 시장가에 100000원어치 매수
            upbit_access.buy_market_order(ticker="KRW-BTC", price=current_price)  # 매수
            min_price = current_price # 최저가 갱신

        else:
            if current_price > max_price * 5.01:
                print("매도되었습니다 매도금액:{0}".format(max_price * 5.01))

                # sell_market_order(ticker='KRW-BTC', volume=1)
                # KRW-BTC를 시장가에 전량매도
                upbit_access.sell_market_order(ticker="KRW-BTC", volume=amount_btc)  # 전량매도
                max_price = current_price # 최고가 갱신

# 필드	                            설명	                        타입
# currency	             화폐를 의미하는 영문 대문자 코드	      String
# balance	             주문가능 금액/수량	                NumberString
# locked    	            주문 중 묶여있는 금액/수량	        NumberString
# avg_buy_price	            매수평균가	                    NumberString
# avg_buy_price_modified	매수평균가 수정 여부                Boolean
# unit_currency	            평단가 기준 화폐	                 String
#####################################################################################################################
################################################ 빗썸 전용 ###########################################################
# 이더리움 정보 가져오기
# def get_ether_price():
# url = "https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=eth_krw"
# timestamp	최종 체결 시각
# last	최종 체결 가격
# bid	최우선 매수호가 (매수 수문 중 가장 높은 가격)
# ask	최우선 매도 호가 (매도 주문 중 가장 낮은 가격)
# low	최근 24시간 저가
# high	최근 24시간 고가
# volumn	거래량
# req = requests.get(url)
# ether = req.json()
# print(type(ether))

# timestamp = ether['timestamp']
# date = (datetime.datetime.fromtimestamp(timestamp / 1000))
# low_price = ether['low']

# soup = BeautifulSoup(req, "html5lib")
# tags = soup.select("p.no_exday") # css selector로 데이터 습득
# tag = tags[0]
# for i in range(0, len(tickers)):
#   if "ETH" in tickers[i]:
#      present_price = upbit.get_current_price(tickers[i]) # 코인 현재가
#      detail_price = upbit.get_market_detail(tickers[i]) # 코인 전체 가격 정보(저가, 고가, 평균거래, 거래량)
#      orderbook = upbit.get_orderbook(tickers[i])  # 코인의 호가 정보
#
#      print("ETH present_price {0}".format(present_price))
#      print("ETH detail_price {0}".format(detail_price))
#      print("ETH low_price {0}".format(detail_price[0]))
#      # print("ETH orderbook {0}".format(orderbook))
#
#      #for order in orderbook:
#      #    print("ETH orderbook {0}".format(order))
#      #print(orderbook['bids'])
# return present_price, detail_price[0]
