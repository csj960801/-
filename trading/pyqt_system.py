#####################################
######## 시스템 UI 및 제어 지원 ########
#####################################
import sys

# 윈도우 시스템 관련 모듈
from PyQt5.QtWidgets import *

#비트코인 시세 조회를 위한 모듈
import pykorbit

# 시간 경과 체크 모듈
from PyQt5.QtCore import *

# 코인 정보 가져오는 모듈 lib
import asset_trader as trader

import datetime

# qt designer로 그려낸 ui(init_window.ui) 호출
from PyQt5 import  uic
window_form = uic.loadUiType("init_window.ui")[0]

# QMainWindow 상속받아서 기본적인 window 시스템 사용하기 위함
class init_window(QMainWindow, window_form):
    def __init__(self):
        # super()는 부모클래스 생성자 호출
        super().__init__()
        self.setupUi(self)
        self.deposit_info_btn.clicked.connect(self.deposit_info) #클릭시 보유자산 정보 업데이트
        self.trade_btn.clicked.connect(self.trade_start) # 거래시작

        # 지속적으로 시간마다 비트코인 현재가, 평단가 정보 업데이트
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.present_avg_price)

    # 코인 평단가, 현재가 정보 조회
    def present_avg_price(self):
        current = QTime.currentTime()
        str_time = current.toString("hh:mm:ss")
        self.statusBar().showMessage(str_time) # 현재시간 노출

        btc_present_price = trader.get_bit_price("KRW-BTC") # 비트코인 현재가
        btc_avg_price=trader.get_average("BTC") # 비트코인 평단가

        # 비트코인 현재가격
        self.BTC_present_price.setText(str(btc_present_price))

        # 비트코인 평단가
        self.BTC_avg_price.setText(str(btc_avg_price))

    # 보유 현금 및 코인 조회
    def deposit_info(self):
        btc_deposit = trader.get_my_deposit("BTC")  # 보유 비트코인
        krw_deposit = trader.get_my_deposit("KRW")  # 보유 현금

        # 보유 현금
        self.cash_amount.setText(str(krw_deposit))

        # 보유 비트코인
        self.btc_amount.setText(str(btc_deposit))

    # 거래시작
    def trade_start(self):
        trader.trade_start()


# UI/UX Info instance
app=QApplication(sys.argv);
window = init_window()
window.show()
app.exec()