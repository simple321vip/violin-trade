from typing import Dict

from vnpy.trader.engine import MainEngine, OmsEngine


class Coordinator:

    def __init__(self, main_engine: MainEngine):
        self.main_engine = main_engine

    def on_init(self):
        print(self.__class__)

    def query_account(self):
        oms_engine: OmsEngine = self.main_engine.get_engine("oms")
        accounts: Dict = oms_engine.accounts
        return accounts
