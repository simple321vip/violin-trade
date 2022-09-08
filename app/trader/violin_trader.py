import multiprocessing
import sys
from time import sleep
from datetime import datetime, time
from logging import INFO
from typing import Dict, List

from vnpy.event import EventEngine
from vnpy.trader.constant import Exchange
from vnpy.trader.object import SubscribeRequest, ContractData
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine, OmsEngine

from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp, CtaEngine
from vnpy_ctastrategy.base import EVENT_CTA_LOG

from app.trader import coordinator

if __name__ == '__main__':
    print("")

SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True
SETTINGS["database.name"] = 'mongodb'
SETTINGS["database.database"] = 'violin'
SETTINGS["database.host"] = 'localhost'
SETTINGS["database.port"] = 27017
SETTINGS["datafeed.name"] = 'tushare'

ctp_setting = {
    "用户名": "205348",
    "密码": "Mb@83201048",
    "经纪商代码": "9999",
    "交易服务器": "180.168.146.187:10101",
    "行情服务器": "180.168.146.187:10111",
    "产品名称": "simnow_client_test",
    "授权编码": "0000000000000000",
    "产品信息": ""
}


# Chinese futures market trading period (day/night)
DAY_START = time(8, 45)
DAY_END = time(17, 0)

NIGHT_START = time(20, 45)
NIGHT_END = time(2, 45)


def check_trading_period():
    """"""
    current_time = datetime.now().time()

    trading = False
    if (
        (DAY_START <= current_time <= DAY_END)
        or (current_time >= NIGHT_START)
        or (current_time <= NIGHT_END)
    ):
        trading = True

    return trading


def run_parent():
    """
    Running in the parent process.
    """
    print("启动CTA策略守护父进程")

    child_process = None

    while True:
        trading = check_trading_period()

        # Start child process in trading period
        if trading and child_process is None:
            print("启动子进程")
            child_process = multiprocessing.Process(target=run_child)
            child_process.start()
            print("子进程启动成功")

        # 非记录时间则退出子进程
        if not trading and child_process is not None:
            if not child_process.is_alive():
                child_process = None
                print("子进程关闭成功")

        sleep(5)


def run_child():
    """
    Running in the child process.
    """
    SETTINGS["log.file"] = True

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    ctp_gateway: CtpGateway = main_engine.add_gateway(CtpGateway)
    cta_engine: CtaEngine = main_engine.add_app(CtaStrategyApp)
    main_engine.write_log("主引擎创建成功")

    coordinator.init()
    coordinator.set_engine(main_engine)

    # key_chart = KeyChart()

    log_engine = main_engine.get_engine("log")
    event_engine.register(EVENT_CTA_LOG, log_engine.process_log_event)
    main_engine.write_log("注册日志事件监听")

    main_engine.connect(ctp_setting, "CTP")
    main_engine.write_log("连接CTP接口")

    sleep(10)

    oms_engine: OmsEngine = main_engine.get_engine("oms")
    accounts: Dict = oms_engine.accounts
    for account in accounts.items():
        print(account)

    req: SubscribeRequest = SubscribeRequest(
        symbol='RM301', exchange=Exchange(Exchange.CZCE)
    )
    main_engine.subscribe(req, ctp_gateway.gateway_name)

    flt: str = 'RM301'

    all_contracts: List[ContractData] = main_engine.get_all_contracts()

    contracts: List[ContractData] = [
        contract for contract in all_contracts if flt in contract.vt_symbol
    ]

    for contract in contracts:
        print(contract)

    cta_engine.init_engine()
    main_engine.write_log("CTA策略初始化完成")

    # cta_engine.init_all_strategies()
    sleep(60)  # Leave enough time to complete strategy initialization
    main_engine.write_log("CTA策略全部初始化")

    # cta_engine.start_all_strategies()
    main_engine.write_log("CTA策略全部启动")

    while True:
        sleep(10)

        trading = check_trading_period()
        if not trading:
            print("关闭子进程")
            main_engine.close()
            sys.exit(0)


