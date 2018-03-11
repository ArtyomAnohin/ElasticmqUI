from flask import Blueprint
from flask import render_template, request, redirect

from app.sqsclient import cleint_get_queues, client_delete_message, client_purge, client_get_messages, \
    client_get_queu_by_name, client_send_message

application = Blueprint('api', __name__)


@application.route('/')
@application.route('/index')
def index():
    queue_list, error = cleint_get_queues()
    return render_template("index.html", queue_list=queue_list, error=error)


@application.route('/queue/<name>', methods=['POST', 'GET'])
def queue(name=None):
    try:
        messages = client_get_messages(name)
        queue = client_get_queu_by_name(name)
    except:
        return render_template('404.html')
    return render_template("messageslist.html", name=name, message_list=messages,
                           current_queue=queue)


@application.route('/message/delete', methods=['POST', 'GET'])
def delete_message():
    if request.method == 'POST':
        result = request.form
        client_delete_message(result['queue_name'], result['message_id'])
        return redirect('queue/' + result['queue_name'])
    elif request.method == 'GET':
        return render_template('404.html')


@application.route('/queue/purge', methods=['POST', 'GET'])
def purge_queue():
    if request.method == 'POST':
        result = request.form
        name = result['queue_name']
        client_purge(name)
        return render_template("messageslist.html", name=name, message_list=client_get_messages(name),
                               current_queue=client_get_queu_by_name(name))
    elif request.method == 'GET':
        return render_template('404.html')


@application.route('/message/add', methods=['POST', 'GET'])
def add_message():
    if request.method == 'POST':
        result = request.form
        client_send_message(result['queue_name'], result['message_body'])
        return redirect('queue/' + result['queue_name'])
    elif request.method == 'GET':
        return render_template('404.html')


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
