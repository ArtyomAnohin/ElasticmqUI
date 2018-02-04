from flask import Flask
from flask import render_template, request, redirect

from app.sqsclient import cleint_get_queues, client_delete_message, client_purge, client_get_messages, \
    client_get_queu_by_name, client_send_message

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", queue_list=cleint_get_queues())


@app.route('/queue/<name>', methods=['POST', 'GET'])
def queue(name=None):
    try:
        messages = client_get_messages(name)
        queue = client_get_queu_by_name(name)
    except:
        return render_template('404.html')
    return render_template("messageslist.html", name=name, message_list=messages,
                           current_queue=queue)


@app.route('/message/delete', methods=['POST', 'GET'])
def delete_message():
    if request.method == 'POST':
        result = request.form
        client_delete_message(result['queue_name'], result['message_id'])
        return redirect('queue/' + result['queue_name'])
    elif request.method == 'GET':
        return render_template('404.html')

@app.route('/queue/purge', methods=['POST', 'GET'])
def purge_queue():
    if request.method == 'POST':
        result = request.form
        name = result['queue_name']
        client_purge(name)
        return render_template("messageslist.html", name=name, message_list=client_get_messages(name),
                           current_queue=client_get_queu_by_name(name))
    elif request.method == 'GET':
        return render_template('404.html')

@app.route('/message/add', methods=['POST', 'GET'])
def add_message():
    if request.method == 'POST':
        result = request.form
        client_send_message(result['queue_name'], result['message_body'])
        return redirect('queue/' + result['queue_name'])
    elif request.method == 'GET':
        return render_template('404.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404