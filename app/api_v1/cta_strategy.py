# -*- coding:utf-8 -*-

from app.api_v1 import api


@api.route('/strategies')
def get_strategy_list():
    print("1")
    return {
        'strategy_id': 'id_1',
        'strategy_name': 'name_1'
    }

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
