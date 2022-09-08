from typing import Dict

from vnpy.trader.engine import MainEngine, OmsEngine


class Coordinator:

    def __init__(self, ):
        self.main_engine = None
        print("!")

    def on_init(self, main_engine: MainEngine):
        print(self.__class__)
        self.main_engine = main_engine

    def query_account(self):
        oms_engine: OmsEngine = self.main_engine.get_engine("oms")
        accounts: Dict = oms_engine.accounts
        return accounts


def init():

    global coordinator
    coordinator = Coordinator()


def set_engine(main_engine: MainEngine):

    coordinator.on_init(main_engine)


def get_engine():

    return coordinator.main_engine
