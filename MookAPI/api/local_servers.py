import datetime

from flask import Blueprint, jsonify, request

from MookAPI.services import local_servers

from ._security import basic_auth_required, basic_auth_user
from . import route

bp = Blueprint("local_servers", __name__, url_prefix="/local_servers")

@route(bp, "/reset")
@basic_auth_required
def reset_local_server():
    user = basic_auth_user._get_current_object()
    # FIXME: Check if user has role "local_server"

    local_server = local_servers.first(user=user)

    local_server.reset()

    local_server.save()

    return jsonify(data=local_server)

@route(bp, "/sync")
@basic_auth_required
def get_local_server_sync_list():
    user = basic_auth_user._get_current_object()
    #FIXME: Check if user has role "local_server"

    local_server = local_servers.first(user=user)
    now = datetime.datetime.now
    sync_list = local_server.get_sync_list()

    local_server.set_last_sync(now)
    local_server.save()

    return jsonify(data=sync_list)

@route(bp, "/register", methods=['POST'])
@basic_auth_required
def register_local_server():

    user = basic_auth_user._get_current_object()
    #FIXME: Check if user has role "local_server"

    local_server = local_servers.create(user=user)

    return jsonify(data=local_server)

@route(bp, "/subscribe", methods=['POST'])
@basic_auth_required
def subscribe_item_to_sync():

    user = basic_auth_user._get_current_object()
    #FIXME: Check if user has role "local_server"

    local_server = local_servers.first(user=user)

    try:
        data = request.get_json()
    except:
        return jsonify(error="Invalid data", code=1), 400
    service_name = data.get('service', None)
    document_id = data.get('document_id', None)

    local_server.append_syncable_item(service_name, document_id)

    try:
        local_server.save()
    except Exception as e:
        return jsonify(error=e.message), 400
    else:
        return jsonify(data=local_server)
