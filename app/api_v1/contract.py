# -*- coding:utf-8 -*-
from typing import Dict

from flask import jsonify, request

from app.api_v1 import api
from ..trader.violin_trader import run_child
from ..trader.violin_trader import ApiService


@api.route('/accounts', methods=['GET'])
def get_accounts():
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    account = api_service.query_account()
    if account:
        return account
    return jsonify({"code": 101, "message": "failure"})


@api.route('/contract/<symbol>', methods=['GET'])
def get_contract(symbol: str):

    api_service: ApiService = run_child.__globals__["api_service"]
    contracts = api_service.query_contract(symbol)
    if contracts:
        return contracts
    return


@api.route('/tick/<vt_symbol>', methods=['GET'])
def get_tick(vt_symbol: str):

    api_service: ApiService = run_child.__globals__["api_service"]
    tick = api_service.get_tick(vt_symbol)
    if tick:
        return tick
    return


@api.route('/ticks', methods=['GET'])
def get_ticks():

    api_service: ApiService = run_child.__globals__["api_service"]
    ticks = api_service.get_ticks()
    return {'ticks': ticks}


@api.route('/order', methods=['POST'])
def send_order():
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    vt_symbol = request.json.get('vt_symbol')
    direction = request.json.get('direction')
    offset = request.json.get('offset')
    volume: Dict = request.json.get('volume')
    price = request.json.get('price')
    order_id = api_service.send_order(
        vt_symbol=vt_symbol, direction=direction, offset=offset, volume=volume, price=price
    )
    if order_id:
        return order_id
    return jsonify({"code": 101, "message": "failure"})


@api.route('/subscribe/<vt_symbol>', methods=['GET'])
def subscribe(vt_symbol: str):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    api_service.subscribe(vt_symbol)
    return


@api.route('/subscribe/vt_symbols', methods=['GET'])
def get_subscribe_vt_symbols():
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    vt_symbols = api_service.get_subscribe_vt_symbols()
    return vt_symbols


@api.route('/vt_symbols', methods=['GET'])
def get_all_vt_symbols():
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    vt_symbols = api_service.get_all_vt_symbols()
    return vt_symbols


@api.route('/exchanges', methods=['GET'])
def get_exchanges():
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    exchanges = api_service.get_exchanges()
    return exchanges
