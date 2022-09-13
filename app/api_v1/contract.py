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
def get_contracts(symbol: str):

    api_service: ApiService = run_child.__globals__["api_service"]
    contracts = api_service.query_contract(symbol)
    if contracts:
        return contracts
    return


@api.route('/order', methods=['POST'])
def send_order():
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
