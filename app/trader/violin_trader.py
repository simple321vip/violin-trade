import importlib
import os
import platform
import traceback
from datetime import datetime, time
from glob import glob
from logging import INFO
from pathlib import Path
from time import sleep
from types import MethodType, ModuleType
from typing import Dict, List, Optional

from pymongo.collection import Collection
from pymongo.database import Database
from vnpy.event import EventEngine
from vnpy.trader.constant import Exchange, OrderType, Offset, Direction
from vnpy.trader.engine import MainEngine, OmsEngine
from vnpy.trader.object import ContractData, AccountData, OrderRequest, TickData, SubscribeRequest, PositionData, \
    OrderData, TradeData
from vnpy.trader.setting import SETTINGS
from vnpy_ctastrategy import CtaStrategyApp, CtaEngine, CtaTemplate
from vnpy_ctastrategy.base import EVENT_CTA_LOG
from vnpy_ctp import CtpGateway
from werkzeug.utils import secure_filename

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
    main_engine.add_gateway(CtpGateway)
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
    to load strategy_class remain in the t_strategy_class
    to start strategy remain in the t_strategy where status is started.
    """
    main_engine.write_log("CTA策略 加载开始")
    database_client: Database = api_service.database_client
    t_strategy_class: Collection = database_client.get_collection("t_strategy_class")

    # 读取本地文件
    files: list[str] = os.listdir(api_service.strategy_path)

    """
    as a method added to cta_engine outside.
    """

    def load_strategy_class_from_web(self, strategy_module_name: str) -> str:
        try:
            module: ModuleType = importlib.import_module(strategy_module_name)

            # 重载模块，确保如果策略文件中有任何修改，能够立即生效。
            importlib.reload(module)

            for name in dir(module):
                value = getattr(module, name)
                if isinstance(value, type) and issubclass(value, CtaTemplate) and value is not CtaTemplate:
                    self.classes[value.__name__] = value
                    return value.__name__
        except:  # noqa
            msg: str = f"策略文件{module_name}加载失败，触发异常：\n{traceback.format_exc()}"
            self.write_log(msg)

    cta_engine.load_strategy_class_from_web = MethodType(load_strategy_class_from_web, cta_engine)

    def delete_strategy_class_from_classes(self, class_name: str) -> str:
        return self.classes.pop(class_name)

    cta_engine.delete_strategy_class_from_classes = MethodType(delete_strategy_class_from_classes, cta_engine)

    # 读取数据库保存的文件
    for strategy_class in t_strategy_class.find():
        if files.count(strategy_class.get('file_name') + '.py') == 0:
            t_strategy_class.delete_one({"file_name": strategy_class.get("file_name")})
        else:
            module_name: str = f"strategies." + strategy_class.get("file_name")
            cta_engine.load_strategy_class_from_web(module_name)

    # cta_engine.load_strategy_class_from_folder(api_service.strategy_path, 'strategies')
    current_strategy_class = database_client.get_collection("t_strategy_class").find()
    strategy_class_list: list[str] = []
    for strategy_class in current_strategy_class:
        strategy_class_list.append(strategy_class.get("class_name"))

    t_strategy: Collection = database_client.get_collection("t_strategy")
    for strategy in t_strategy.find():
        if strategy_class_list.count(strategy.get('class_name')) == 0:
            main_engine.write_log("strategy_class_name is not found, skip!")
            continue
        else:
            cta_engine.add_strategy(
                class_name=strategy.get("class_name"),
                strategy_name=strategy.get("strategy_name"),
                vt_symbol=strategy.get("vt_symbol"),
                setting=strategy.get("setting")
            )

            if strategy.get("status") == 1:
                cta_engine.init_strategy(strategy.get("strategy_name"))
                cta_engine.start_strategy(strategy.get("strategy_name"))

    """
    subscribe vt_symbol
    """
    results = database_client.get_collection("t_subscribe").find()
    for result in results:
        symbol, exchange = result.get("vt_symbol").split(".")
        req: SubscribeRequest = SubscribeRequest(
            symbol=symbol, exchange=Exchange(exchange)
        )
        main_engine.subscribe(req, "CTP")

    sleep(6)  # Leave enough time to complete strategy initialization
    main_engine.write_log("CTA策略全部启动")


class ApiService:
    main_engine: MainEngine
    cta_engine: CtaEngine
    oms_engine: OmsEngine
    strategy_path: Path
    database_client: Database

    def __init__(self, main_engine: MainEngine, cta_engine: CtaEngine):
        """
        """
        self.main_engine = main_engine
        self.cta_engine = cta_engine
        self.oms_engine = main_engine.get_engine("oms")
        self.database_client = self.cta_engine.database.db

        if platform.system().lower() == 'windows':
            self.strategy_path = Path("C:\\Users\\simpl\\strategies")
        elif platform.system().lower() == 'linux':
            self.strategy_path = Path("/violin/strategy")

    def query_strategy_files(self):
        """
        query strategies with strategy file's extension equals '.py' from strategy folder
        """
        pathname: str = str(self.strategy_path.joinpath(f"*.py"))
        strategy_files: list = []
        collection = self.database_client.get_collection("t_strategy_class")
        results = list(collection.find())
        for filepath in glob(pathname):
            file_name = Path(filepath).stem
            strategy_file: Dict = {
                "file_name": file_name,
                "class_name": "",
                "status": 0
            }
            for row in results:
                if row.get("file_name") == file_name:
                    strategy_file['class_name'] = row.get("class_name")
                    strategy_file['status'] = 1
            strategy_files.append(strategy_file)
        return strategy_files

    def query_strategy_load_files(self) -> Dict:
        """
        query strategies with strategy file's extension equals '.py' from strategy folder
        """
        pathname: str = str(self.strategy_path.joinpath(f"*.py"))
        strategy_files: list = []
        for filepath in glob(pathname):
            filename = Path(filepath).stem
            strategy_files.append(filename)

        strategy_file_list: list[str] = []

        collection = self.database_client.get_collection("t_strategy_class")
        for row in collection.find():
            file_name = row.get("file_name")
            if strategy_files.count(file_name) != 0:
                strategy_file_list.append(row.get('class_name'))

        return {'class_names': strategy_file_list}

    def load_strategy(self, strategy_file_name: str):
        """
        load a strategy from strategy folder into system and add it into t_strategy_class collection.
        if the strategy_file_name exits in the t_strategy_class collection, skip this process, and return exist message.
        """
        t_strategy_class: Collection = self.database_client.get_collection("t_strategy_class")
        if t_strategy_class.find_one({"file_name": strategy_file_name}):
            return

        name: str = f"strategies." + strategy_file_name
        strategy_class_name: str = self.cta_engine.load_strategy_class_from_web(name)

        t_strategy_class.insert_one(
            {
                "file_name": strategy_file_name,
                "class_name": strategy_class_name,
                "status": 1
            }
        )

        return strategy_class_name

    def unload_strategy(self, strategy_class_name: str):
        """
        pop the strategy_class_name from classes in the cta_engine
        delete a document in the collection t_strategy_class by filter
        """
        t_strategy_class: Collection = self.database_client.get_collection("t_strategy_class")
        if t_strategy_class.find_one({"class_name": strategy_class_name}):
            t_strategy_class.delete_one({"class_name": strategy_class_name})
            self.cta_engine.delete_strategy_class_from_classes(strategy_class_name)
            return strategy_class_name

        return

    def remove_strategy(self, strategy_file_name: str):
        """
        to remove a strategy file
        """
        file_path: str = str(self.strategy_path) + os.sep + strategy_file_name + ".py"
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                return strategy_file_name
            except BaseException as e:
                print(e)
        return

    def upload_strategy(self, strategy_file) -> str:
        """
        to save a strategy file
        """
        upload_path = os.path.join(self.strategy_path, secure_filename(strategy_file.filename))
        if os.path.exists(upload_path):
            return
        strategy_file.save(upload_path)

        return strategy_file.filename

    def get_strategy_instances(self):
        """
        query all the strategy instances from db.
        """
        collection = self.database_client.get_collection("t_strategy")
        strategy_instances: list[Dict] = []
        for document in collection.find():

            strategy_instances.append(
                {
                    'class_name': document.get('class_name'),
                    'strategy_name': document.get('strategy_name'),
                    'vt_symbol': document.get('vt_symbol'),
                    'setting': document.get('setting'),
                    'status': document.get('status')
                }
            )

        return strategy_instances

    def create_strategy_instance(self, class_name: str, strategy_name: str, vt_symbol: str, setting: dict):
        """
        create a strategy instance for vt_symbol with setting
        """
        self.cta_engine.add_strategy(class_name, strategy_name, vt_symbol, setting)
        collection = self.database_client.get_collection("t_strategy")

        collection.insert_one(
            {
                'class_name': class_name,
                'strategy_name': strategy_name,
                'vt_symbol': vt_symbol,
                'setting': setting,
                'status': 0
            }
        )

        return class_name

    def init_strategy_instance(self, strategy_name: str):
        """
        to start a strategy instance
        """
        self.cta_engine.init_strategy(strategy_name)
        collection = self.database_client.get_collection("t_strategy")
        collection.find_one_and_update(
            filter={
                'strategy_name': strategy_name
            },
            update={
                '$set': {
                    'status': 1
                }
            }
        )

        return strategy_name

    def start_strategy_instance(self, strategy_name: str):
        """
        to start a strategy instance
        """
        self.cta_engine.start_strategy(strategy_name)
        collection = self.database_client.get_collection("t_strategy")
        collection.find_one_and_update(
            filter={
                'strategy_name': strategy_name
            },
            update={
                '$set': {
                    'status': 2
                }
            }
        )

        return strategy_name

    def stop_strategy_instance(self, strategy_name: str):
        """
        to stop a strategy instance
        """
        self.cta_engine.stop_strategy(strategy_name)
        collection = self.database_client.get_collection("t_strategy")
        collection.find_one_and_update(
            filter={
                'strategy_name': strategy_name
            },
            update={
                '$set': {
                    'status': 3
                }
            }
        )
        return strategy_name

    def remove_strategy_instance(self, strategy_name: str):
        """
        to remove a strategy instance
        """
        self.cta_engine.remove_strategy(strategy_name)
        collection = self.database_client.get_collection("t_strategy")
        collection.delete_one(
            {
                'strategy_name': strategy_name
            }
        )
        return strategy_name

    def get_strategy_status(self, strategy_name: str):
        """
        to get a strategy status by strategy_name
        """
        collection = self.database_client.get_collection("t_strategy")
        t_strategy = collection.find_one(
            {
                'strategy_name': strategy_name
            }
        )
        return t_strategy.get("status")

    def query_contract(self, symbol: str):
        symbol, _ = symbol.split(".")
        flt = symbol

        all_contracts: List[ContractData] = self.oms_engine.get_all_contracts()
        contracts: List[ContractData] = [
            contract for contract in all_contracts if flt in contract.vt_symbol
        ]
        if contracts:
            contract_data: ContractData = contracts.pop()
            contract = {
                'vt_symbol': contract_data.vt_symbol,
                'name': contract_data.name,
                'pricetick': contract_data.pricetick,
                'size': contract_data.size
            }
            return contract

        return

    def send_order(self, vt_symbol: str, direction, offset, volume, price) -> str:
        """
        Send new order manually.
        """
        symbol, exchange = vt_symbol.split(".")

        req: OrderRequest = OrderRequest(
            symbol=symbol,
            exchange=Exchange(exchange),
            direction=Direction(direction),
            type=OrderType.MARKET,
            volume=float(volume),
            price=float(price),
            offset=Offset(offset),
            reference="ManualTrading"
        )

        order_id = self.main_engine.send_order(req, "CTP")
        return order_id

    def query_account(self) -> Dict:
        """
        query accounts
        """
        accounts_data: Dict = self.oms_engine.accounts
        accounts = []
        if accounts_data:
            account_key = list(accounts_data.keys()).pop()
            account_value: AccountData = accounts_data.get(account_key)
            account = {
                'gateway_name': account_value.gateway_name,
                'account_id': account_value.accountid,
                'balance': account_value.balance,
                'frozen': account_value.frozen
            }
            accounts.append(account)

        positions_data: Dict = self.oms_engine.positions
        positions = []
        if positions_data:
            for position_key in list(positions_data.keys()):
                position_value: PositionData = positions_data.get(position_key)
                position = {
                    'symbol': position_value.symbol,
                    'exchange': position_value.exchange.value,
                    'direction': position_value.direction.value,
                    'volume': position_value.volume,
                    'frozen': position_value.frozen,
                    'price': position_value.price,
                    'pnl': position_value.pnl,
                    'yd_volume': position_value.yd_volume
                }
                positions.append(position)

        orders_data: Dict = self.oms_engine.orders
        orders = []
        if orders_data:
            for order_key in orders_data:
                order_value: OrderData = orders_data.get(order_key)
                order = {
                    'symbol': order_value.symbol,
                    'exchange': order_value.exchange.value,
                    'direction': order_value.direction.value,
                    'volume': order_value.volume,
                    'price': order_value.price,
                    'orderid': order_value.orderid,
                    'type': order_value.type.value,
                    'offset': order_value.offset.value,
                    'traded': order_value.traded,
                    'status': order_value.status.value,
                    'datetime': order_value.datetime,
                    'reference': order_value.reference
                }
                orders.append(order)

        trades_data: Dict = self.oms_engine.trades
        trades = []
        if trades_data:
            for trade_key in trades_data:
                trade_value: TradeData = trades_data.get(trade_key)
                trade = {
                    'symbol': trade_value.symbol,
                    'exchange': trade_value.exchange.value,
                    'direction': trade_value.direction.value,
                    'volume': trade_value.volume,
                    'price': trade_value.price,
                    'orderid': trade_value.vt_orderid,
                    'tradeid': trade_value.tradeid,
                    'offset': trade_value.offset.value,
                    'datetime': trade_value.datetime,
                }
                trades.append(trade)

        result = {
            'accounts': accounts,
            'positions': positions,
            'orders': orders,
            'trades': trades
        }
        return result

    def get_tick(self, vt_symbol: str) -> Dict:
        """
        """
        optional: Optional[TickData] = self.oms_engine.get_tick(vt_symbol)
        if optional:

            tick = {
                'symbol': optional.symbol,
                'exchange': optional.exchange.value,
                'name': optional.name,
                'volume': optional.volume,
                'turnover': optional.turnover,
                'open_interest': optional.open_interest,
                'last_price': optional.last_price,
                'last_volume': optional.last_volume,
                'limit_up': optional.limit_up,
                'limit_down': optional.limit_down,
                'open_price': optional.open_price,
                'high_price': optional.high_price,
                'low_price': optional.low_price,
                'pre_close': optional.pre_close,
                'bid_price_1': optional.bid_price_1,
                'bid_price_2': optional.bid_price_2,
                'bid_price_3': optional.bid_price_3,
                'bid_price_4': optional.bid_price_4,
                'bid_price_5': optional.bid_price_5,
                'ask_price_1': optional.ask_price_1,
                'ask_price_2': optional.ask_price_2,
                'ask_price_3': optional.ask_price_3,
                'ask_price_4': optional.ask_price_4,
                'ask_price_5': optional.ask_price_5
            }

            return {'tick': tick}
        return {'tick': None}

    def get_ticks(self) -> []:
        """
        """
        collection = self.database_client.get_collection("t_subscribe").find()
        ticks = []
        for doc in collection:
            vt_symbol = doc.get('vt_symbol')
            optional: Optional[TickData] = self.oms_engine.get_tick(vt_symbol)
            if optional:
                tick = {
                    'symbol': optional.symbol,
                    'exchange': optional.exchange.value,
                    'name': optional.name,
                    'volume': optional.volume,
                    'turnover': optional.turnover,
                    'open_interest': optional.open_interest,
                    'last_price': optional.last_price,
                    'last_volume': optional.last_volume,
                    'limit_up': optional.limit_up,
                    'limit_down': optional.limit_down,
                    'open_price': optional.open_price,
                    'high_price': optional.high_price,
                    'low_price': optional.low_price,
                    'pre_close': optional.pre_close,
                    'bid_price_1': optional.bid_price_1,
                    'bid_price_2': optional.bid_price_2,
                    'bid_price_3': optional.bid_price_3,
                    'bid_price_4': optional.bid_price_4,
                    'bid_price_5': optional.bid_price_5,
                    'ask_price_1': optional.ask_price_1,
                    'ask_price_2': optional.ask_price_2,
                    'ask_price_3': optional.ask_price_3,
                    'ask_price_4': optional.ask_price_4,
                    'ask_price_5': optional.ask_price_5
                }
                ticks.append(tick)
        return ticks

    def subscribe(self, vt_symbol: str):
        """
        """
        symbol, exchange = vt_symbol.split(".")
        req: SubscribeRequest = SubscribeRequest(
            symbol=symbol, exchange=Exchange(exchange)
        )
        self.main_engine.subscribe(req, "CTP")
        t_subscribe = self.database_client.get_collection("t_subscribe")
        result = t_subscribe.insert_one({
                'vt_symbol': vt_symbol
            })
        if result:
            return result
        return

    def cancel_subscribe(self, vt_symbol: str):
        """
        """
        symbol, exchange = vt_symbol.split(".")
        # req: SubscribeRequest = SubscribeRequest(
        #     symbol=symbol, exchange=Exchange(exchange)
        # )
        # self.main_engine.subscribe(req, "CTP")
        t_subscribe = self.database_client.get_collection("t_subscribe")
        result = t_subscribe.delete_one({
                'vt_symbol': vt_symbol
            })
        if result:
            return result
        return

    def get_subscribe_vt_symbols(self) -> Dict:
        """
        to query available symbols.
        """
        collection = self.database_client.get_collection("t_subscribe").find()
        vt_symbols = []
        for doc in collection:
            vt_symbol = doc.get('vt_symbol')
            vt_symbols.append(vt_symbol)

        return {'vt_symbols': vt_symbols}

    def get_all_vt_symbols(self) -> Dict:
        """
        to query available symbols.
        """
        exchanges = self.get_exchanges()
        vt_symbols: Dict = {}
        for exchange in exchanges.get('exchanges'):
            vt_symbols[exchange] = []

        all_contracts: List[ContractData] = self.oms_engine.get_all_contracts()
        for contract_data in all_contracts:
            symbol, exchange = contract_data.vt_symbol.split(".")
            dict_tmp: list = vt_symbols.get(exchange)
            dict_tmp.append(contract_data.vt_symbol)

        return {'vt_symbols': vt_symbols}

    def get_exchanges(self) -> Dict:
        """
        to query exchanges.
        """
        exchanges = []
        for exchange in self.main_engine.exchanges:
            exchanges.append(exchange.value)
        return {'exchanges': exchanges}
