import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import logging.handlers
import time
from pandas import DataFrame

is_64bits = sys.maxsize > 2**32
if is_64bits:
    print('64bit 환경입니다.')
else:
    print('32bit 환경입니다.')

formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
logger = logging.getLogger("crumbs")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


TR_REQ_TIME_INTERVAL = 0.2
class Openapi(QAxWidget):
    def __init__(self):
        print("openapi __name__:", __name__)
        super().__init__()
        self._create_open_api_instance()
        self._set_signal_slots()
        self.comm_connect()
        self.account_info()

    def _create_open_api_instance(self):
        try:
            self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        except Exception as e:
            logger.critical(e)

    def _set_signal_slots(self):
        try:
            self.OnEventConnect.connect(self._event_connect)

        except Exception as e:
            is_64bits = sys.maxsize > 2**32
            if is_64bits:
                logger.critical('현재 Anaconda는 64bit 환경입니다. 32bit 환경으로 실행하여 주시기 바랍니다.')
            else:
                logger.critical(e)

    def comm_connect(self):
        try:
            self.dynamicCall("CommConnect()")
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.login_event_loop = QEventLoop()
            self.login_event_loop.exec_()
        except Exception as e:
            logger.critical(e)

    def _event_connect(self, err_code):
        try:
            if err_code == 0:
                logger.debug("connected")
            else:
                logger.debug(f"disconnected. err_code : {err_code}")
            self.login_event_loop.exit()
        except Exception as e:
            logger.critical(e)

    def account_info(self):
        account_number = self.get_login_info("ACCNO")
        self.account_number = account_number.split(';')[0]
        logger.debug("계좌번호: " + self.account_number)

    def get_login_info(self, tag):
        try:
            ret = self.dynamicCall("GetLoginInfo(QString)", tag)
            time.sleep(TR_REQ_TIME_INTERVAL)
            return ret
        except Exception as e:
            logger.critical(e)


    # get_total_data : 특정 종목의 일자별 거래 데이터 조회 함수

    # 사용방법
    # code: 종목코드(ex. '005930' )
    # start : 기준일자. (ex. '20200424') => 20200424 일자 까지의 모든 open, high, low, close, volume 데이터 출력
    def get_total_data(self, code, start):

        self.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
        self.set_input_value("종목코드", code)
        self.set_input_value("기준일자", start)
        self.set_input_value("수정주가구분", 1)
        self.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

        # 이 밑에는 한번만 가져오는게 아니고 싹다 가져오는거다.

        while self.remained_data == True:
            # time.sleep(TR_REQ_TIME_INTERVAL)
            self.set_input_value("종목코드", code)
            self.set_input_value("기준일자", start)
            self.set_input_value("수정주가구분", 1)
            self.comm_rq_data("opt10081_req", "opt10081", 2, "0101")

        time.sleep(0.2)
        # data 비어있는 경우
        if len(self.ohlcv) == 0:
            return []

        if self.ohlcv['date'] == '':
            return []

        df = DataFrame(self.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], index=self.ohlcv['date'])

        return df

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Openapi()