# -*- coding:utf-8 -*-
from flask import request

from app.api_v1 import api
from ..trader.violin_trader import run_child
from ..trader.violin_trader import ApiService


@api.route('/strategy_file', methods=['GET'])
def get_strategy_file_list():
    """
    """
    xx = request
    api_service: ApiService = run_child.__globals__["api_service"]
    strategy_list = api_service.query_strategies()

    return strategy_list


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
        return 200
    else:
        return 500


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
    api_service: ApiService = run_child.__globals__["api_service"]
    api_service.create_strategy_instance()
    return 200


@api.route('/strategy/<strategy_name>/start', methods=['PUT'])
def start_strategy(strategy_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    api_service.start_strategy_instance(strategy_name)
    return 200


@api.route('/strategy/<strategy_name>/stop', methods=['PATCH'])
def stop_strategy(strategy_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    api_service.stop_strategy_instance(strategy_name)
    return 200


@api.route('/strategy/<strategy_name>/stop', methods=['DELETE'])
def remove_strategy(strategy_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    api_service.remove_strategy_instance(strategy_name)
    return 200


@api.route('/strategy/status/<strategy_name>', methods=['GET'])
def get_strategy_status(strategy_name):
    """
    """
    api_service: ApiService = run_child.__globals__["api_service"]
    api_service.remove_strategy_instance(strategy_name)
    return 200

#
# @api.route('/strategy')
# @auth.login_required
# def get_strategy_list():
#     posts = Post.query.all()
#     return jsonify({
#         'posts': [post.to_json() for post in posts]
#     })
#
#
# @api.route('/trader/api/v1/<int:id>', methods=['PUT'])
# @auth.login_required
# def upload_strategy():
#     post = Post.query.get_or_404(id)
#     return jsonify(post.to_json())
#
#
# @api.route('/trader/api/v1/', methods=['POST'])
# @permission_required(Permission.WRITE_ARTICLES)
# def new_post():
#     post = Post.from_json(request.json)
#     post.author = g.current_user
#     db.session.add(post)
#     db.session.commit()
#     return jsonify(post.to_json()), 201, \
#            {'Location': url_for('api.get_post', id=post.id, _external=True)}
#
#
# @api.route('/posts/<int:id>', methods=['PUT'])
# @permission_required(Permission.WRITE_ARTICLES)
# def edit_post(id):
#     post = Post.query.get_or_404(id)
#     if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
#         return forbidden('Insufficient permissions')
#     post.body = request.json.get('body', post.body)
#     db.session.add(post)
#     return jsonify(post.to_json())
