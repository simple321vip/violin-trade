# -*- coding:utf-8 -*-
from typing import Dict

from app.api_v1 import api
from ..trader.violin_trader import run_child
from ..trader.violin_trader import ApiService


@api.route('/contracts', methods=['GET'])
def get_contract_list():

    api_service: ApiService = run_child.__globals__["api_service"]

    accounts: Dict = api_service.query_account()

    return

def close_contract(contract_id: str):
    api_service: ApiService = run_child.__globals__["api_service"]

    api_service