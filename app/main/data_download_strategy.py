from vnpy.trader.object import TickData
from vnpy_ctastrategy import CtaTemplate


class CollectionDownload(CtaTemplate):

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

    def on_tick(self, tick: TickData) -> None:

        self.cta_engine.database.save_tick_data(tick)
