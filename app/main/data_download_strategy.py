from vnpy.trader.object import TickData, BarData, OrderData, TradeData
from vnpy_ctastrategy import CtaTemplate, StopOrder


class CollectionDownload(CtaTemplate):

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        pass

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")

    def on_tick(self, tick: TickData) -> None:
        """
        Callback of new tick data update.
        """
        ticks = []
        self.cta_engine.database.save_tick_data([tick])

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        pass

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
