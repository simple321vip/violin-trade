# -*- coding:utf-8 -*-
from typing import Dict

from flask import request
from flask import jsonify

from app.api_v1 import api
from ..trader.violin_trader import run_child
from ..trader.violin_trader import ApiService


@api.route('/strategy_file', methods=['GET'])
def get_strategy_file_list():
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    strategy_files = api_service.query_strategy_files()

    return strategy_files


@api.route('/strategy_file/load', methods=['GET'])
def get_strategy_load_file_list():
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    class_names = api_service.query_strategy_load_files()

    return class_names


@api.route('/strategy_file', methods=['POST'])
def upload_strategy_file():
    """
    """
    file = request.files.get("file")
    if file.filename.endswith(".py"):

        api_service: ApiService = run_child.__globals__["api_service"]
        file_name = api_service.upload_strategy(file)
        if file_name:
            return {
                'file_name': file_name
                   }, 200
        else:
            return {
                       'error_message': '该文件已经存'
                   }, 500

    else:
        return {
            'error_message': '上传的策略文件只能py文件'
        }, 500


@api.route('/strategy_file/<file_name>', methods=['PUT'])
def load_strategy_file(file_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    if api_service.load_strategy(file_name):
        return {}, 200
    else:
        return {
                   'error_message': '策略文件加载失败'
               }, 500


@api.route('/strategy_file/<class_name>', methods=['PATCH'])
def unload_strategy_file(class_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    if api_service.unload_strategy(class_name):
        return {}, 200
    else:
        return {}, 500


@api.route('/strategy_file/<file_name>', methods=['DELETE'])
def remove_strategy_file(file_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    if api_service.remove_strategy(file_name):
        return {}, 200

    return {
               'error_message': '策略文件移除失败'
           }, 500


@api.route('/strategies', methods=['GET'])
def get_strategy_list():
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    strategy_list = api_service.get_strategy_instances()

    return strategy_list


@api.route('/strategy/<strategy_name>', methods=['POST'])
def create_strategy(strategy_name):
    """
    """
    class_name = request.json.get('class_name')
    vt_symbol = request.json.get('vt_symbol')
    setting: Dict = request.json.get('setting')
    api_service: ApiService = run_child.__globals__["api_service"]
    strategy_name = api_service.create_strategy_instance(class_name, strategy_name, vt_symbol, setting)
    if strategy_name:
        return jsonify({"code": 100, "message": "success"})
    return jsonify({"code": 101, "message": "failure"})


@api.route('/strategy/init/<strategy_name>', methods=['PUT'])
def init_strategy(strategy_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    strategy_name = api_service.init_strategy_instance(strategy_name)
    if strategy_name:
        return jsonify({"code": 100, "message": "success"})
    return jsonify({"code": 101, "message": "failure"})


@api.route('/strategy/<strategy_name>', methods=['PUT'])
def start_strategy(strategy_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    strategy_name = api_service.start_strategy_instance(strategy_name)
    if strategy_name:
        return jsonify({"code": 100, "message": "success"})
    return jsonify({"code": 101, "message": "failure"})


@api.route('/strategy/<strategy_name>', methods=['PATCH'])
def stop_strategy(strategy_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    strategy_name = api_service.stop_strategy_instance(strategy_name)
    if strategy_name:
        return jsonify({"code": 100, "message": "success"})
    return jsonify({"code": 101, "message": "failure"})


@api.route('/strategy/<strategy_name>', methods=['DELETE'])
def remove_strategy(strategy_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    strategy_name = api_service.remove_strategy_instance(strategy_name)
    if strategy_name:
        return jsonify({"code": 100, "message": "success"})
    return jsonify({"code": 101, "message": "failure"})


@api.route('/strategy/status/<strategy_name>', methods=['GET'])
def get_strategy_status(strategy_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    status = api_service.get_strategy_status(strategy_name)
    return {'status': status}
