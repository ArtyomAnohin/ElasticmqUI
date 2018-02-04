from flask import Flask
from flask_env import MetaFlaskEnv
from flask import render_template, request, redirect

from app.sqsclient import cleint_get_queues, client_delete_message, client_purge, client_get_messages, \
    client_get_queu_by_name, client_send_message


class Configuration(metaclass=MetaFlaskEnv):
    DEBUG = True
    PORT = 5000


app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", queue_list=cleint_get_queues())


@app.route('/queue/<name>', methods=['POST', 'GET'])
def queue(name=None):
    return render_template("messageslist.html", name=name, message_list=client_get_messages(name),
                           current_queue=client_get_queu_by_name(name))


@app.route('/message/delete', methods=['POST', 'GET'])
def delete_message():
    if request.method == 'POST':
        result = request.form
        client_delete_message(result['queue_name'], result['message_id'])
        return redirect('queue/' + result['queue_name'])


@app.route('/queue/purge', methods=['POST', 'GET'])
def purge_queue():
    if request.method == 'POST':
        result = request.form
        name = result['queue_name']
        client_purge(name)
    return render_template("messageslist.html", name=name, message_list=client_get_messages(name),
                           current_queue=client_get_queu_by_name(name))


@app.route('/message/add', methods=['POST', 'GET'])
def add_message():
    if request.method == 'POST':
        result = request.form
        client_send_message(result['queue_name'], result['message_body'])
        return redirect('queue/' + result['queue_name'])
