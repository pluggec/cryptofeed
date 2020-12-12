'''
Copyright (C) 2017-2020  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import logging

from cryptofeed.config import Config
from cryptofeed.log import get_logger
from cryptofeed.rest.binance_futures import BinanceFutures, BinanceDelivery
from cryptofeed.rest.bitfinex import Bitfinex
from cryptofeed.rest.bitmex import Bitmex
from cryptofeed.rest.coinbase import Coinbase
from cryptofeed.rest.deribit import Deribit
from cryptofeed.rest.ftx import FTX
from cryptofeed.rest.gemini import Gemini
from cryptofeed.rest.kraken import Kraken
from cryptofeed.rest.poloniex import Poloniex
from cryptofeed.standards import load_exchange_pair_mapping


LOG = logging.getLogger('rest')


class Rest:
    """
    The rest class is a common interface for accessing the individual exchanges

    r = Rest()
    r.bitmex.trades('XBTUSD', '2018-01-01', '2018-01-01')

    The Rest class optionally takes two exchange-related parameters, config, and sandbox.
    In the config file the api key and secrets can be specified. Sandbox enables sandbox
    mode, if supported by the exchange.
    """

    def __init__(self, config=None, sandbox=False):
        self.config = Config(file_name=config)

        lfile = 'rest.log' if not self.config or not self.config.restlog.filename else self.config.restlog.filename
        level = logging.WARNING if not self.config or not self.config.restlog.level else self.config.restlog.level
        get_logger('rest', lfile, level)

        self.lookup = {
            'bitmex': Bitmex(config),
            'bitfinex': Bitfinex(config),
            'coinbase': Coinbase(config, sandbox=sandbox),
            'poloniex': Poloniex(config),
            'gemini': Gemini(config, sandbox=sandbox),
            'kraken': Kraken(config),
            'deribit': Deribit(config),
            'binance_futures': BinanceFutures(config),
            'binance_delivery': BinanceDelivery(config),
            'ftx': FTX(config)
        }

    def __getitem__(self, key):
        exch = self.lookup[key.lower()]
        if not exch.mapped:
            try:
                load_exchange_pair_mapping(exch.ID + 'REST')
            except KeyError:
                load_exchange_pair_mapping(exch.ID)
            exch.mapped = True
        return exch

    def __getattr__(self, attr):
        exch = self.lookup[attr.lower()]
        if not exch.mapped:
            try:
                load_exchange_pair_mapping(exch.ID + 'REST')
            except KeyError:
                load_exchange_pair_mapping(exch.ID)
            exch.mapped = True
        return exch
