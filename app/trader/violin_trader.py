import os
import platform
from time import sleep
from datetime import datetime, time
from logging import INFO
from typing import Dict, List

from pymongo.cursor import Cursor
from pymongo.database import Database
from vnpy.event import EventEngine
from vnpy.trader.constant import Exchange
from vnpy.trader.object import SubscribeRequest, ContractData
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine, OmsEngine

from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp, CtaEngine
from vnpy_ctastrategy.base import EVENT_CTA_LOG
from vnpy_mongodb.mongodb_database import MongodbDatabase

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

NIGHT_START = time(18, 45)
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


global api_service


def run_child():
    """
    Running in the child process.
    """
    SETTINGS["log.file"] = True

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    ctp_gateway = main_engine.add_gateway(CtpGateway)
    cta_engine: CtaEngine = main_engine.add_app(CtaStrategyApp)
    main_engine.write_log("主引擎创建成功")

    log_engine = main_engine.get_engine("log")
    event_engine.register(EVENT_CTA_LOG, log_engine.process_log_event)
    main_engine.write_log("注册日志事件监听")

    main_engine.connect(ctp_setting, "CTP")
    main_engine.write_log("连接CTP接口")

    sleep(10)

    cta_engine.init_engine()

    global api_service
    api_service = ApiService(main_engine, cta_engine)

    """
    init strategies.
    """
    main_engine.write_log("CTA策略 加载开始")
    database_client: Database = api_service.database_client
    files: list[str] = os.listdir(api_service.strategy_path)
    for strategy in database_client.get_collection("t_strategy").find():
        if files.count(strategy) == 0:
            database_client.get_collection("t_strategy").delete_one()
        else:
            cta_engine.load_strategy_class_from_folder(api_service.strategy_path + strategy)
            if strategy.get("status") == "start":
                cta_engine.stop_strategy(strategy)

    sleep(60)  # Leave enough time to complete strategy initialization
    main_engine.write_log("CTA策略全部启动")


class ApiService:
    main_engine: MainEngine
    cta_engine: CtaEngine
    strategy_path: str
    database_client: Database

    def __init__(self, main_engine: MainEngine, cta_engine: CtaEngine):
        """
        """
        self.main_engine = main_engine
        self.cta_engine = cta_engine
        self.database_client = self.cta_engine.database.db

        if platform.system().lower() == 'windows':
            self.strategy_path = "C:\\violin\\strategy"
        elif platform.system().lower() == 'linux':
            self.strategy_path = "/violin/strategy"

    def query_strategies(self):
        """
        query strategies from strategy folder
        """
        strategy_files: list = os.listdir(self.strategy_path)
        strategy_list: list[Dict] = []

        collection = self.database_client.get_collection("t_strategy")
        result: Cursor = collection.find()
        for strategy_file in strategy_files:
            strategy: Dict = {
                "strategy_name": strategy_file,
                "strategy_alise_name": strategy_file,
                "status": "unload"
            }
            if result.get(strategy_file):
                strategy['strategy_alise_name'] = ""
                strategy['status'] = ""

            strategy_list.append(strategy)

        return strategy_list

    def load_strategy(self, strategy_id: str):
        """
        query strategies from strategy folder
        """
        strategy_files: list = os.listdir(self.strategy_path)
        self.cta_engine.load_strategy_class_from_folder(self.strategy_path)
        collection = self.database_client.get_collection("t_strategy")
        result: Cursor = collection.insert_one()

        return

    def unload_strategy(self, strategy_id: str):
        """
        query strategies from strategy folder
        """
        strategy_files: list = os.listdir(self.strategy_path)
        # self.cta_engine.(strategy_id)

        return

    def start_strategy(self, strategy_id: str):
        """
        query strategies from strategy folder
        """
        strategy_files: list = os.listdir(self.strategy_path)
        self.cta_engine.start_strategy(strategy_id)

        return

    def start_strategy(self, strategy_id: str):
        """
        query strategies from strategy folder
        """
        strategy_files: list = os.listdir(self.strategy_path)
        self.cta_engine.stop_strategy(strategy_id)

        return

    def remove_strategy(self, strategy_id: str):
        """
        query strategies from strategy folder
        """
        strategy_files: list = os.listdir(self.strategy_path)
        self.cta_engine.remove_strategy(strategy_id)

        return

    def query_contracts(self):

        # req: SubscribeRequest = SubscribeRequest(
        #     symbol='RM301', exchange=Exchange(Exchange.CZCE)
        # )
        # main_engine.subscribe(req, ctp_gateway.gateway_name)

        flt: str = 'RM301'

        all_contracts: List[ContractData] = self.main_engine.get_all_contracts()

        contracts: List[ContractData] = [
            contract for contract in all_contracts if flt in contract.vt_symbol
        ]

        for contract in contracts:
            print(contract)
        pass

    def close_contract(self, contract_id: str):
        """
        """
        pass

    def query_account(self):
        """
        query accounts
        """
        oms_engine = self.main_engine.get_engine("oms")
        accounts: Dict = oms_engine.accounts
        return accounts
