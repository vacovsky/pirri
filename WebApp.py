from flask import Flask, render_template, request, jsonify
import setproctitle
import config
from helpers import WebDataHelper
from helpers.MessageHelper import RMQ
import json


__author__ = 'Joe Vacovsky Jr.'
setproctitle.setproctitle("pirriweb")
app = Flask(__name__)


@app.route('/', methods=["GET"])
def main():
    if request.method == "GET":
        return render_template("index.html")


@app.route('/gpio/list', methods=["GET"])
def gpio_list():
    response = {
        "gpio_pins": WebDataHelper.list_gpio()
    }
    return jsonify(response)


@app.route('/schedule', methods=["GET", "POST"])
def station_schedule():
    if request.method == "GET":
        response = {
            'schedule': WebDataHelper.get_schedule()
        }
    elif request.method == "POST":
        data = json.loads(request.data.decode('utf8'))
        response = {"status": "submitted"}
    return jsonify(response)


@app.route('/history', methods=["GET"])
def station_history():
    response = None
    response = WebDataHelper.station_history()
    return jsonify(response)


@app.route('/station/add', methods=["GET", "POST"])
def station_add():
    response = {}
    return jsonify(response)


@app.route('/stats', methods=["GET"])
def stats():
    response = {}
    print(request.args.get('id'))
    response['chartData'] = WebDataHelper.get_chart_stats(
        int(request.args.get('id')))
    return jsonify(response)


@app.route('/station/run', methods=["POST"])
def station_run():
    data = json.loads(request.data.decode('utf8'))
    RMQ().publish_message(json.dumps({
        "sid": data['sid'],
        "duration": data['duration']
    }))
    response = {"status": "submitted"}
    return jsonify(response)


@app.route('/station/list', methods=["GET"])
def station_list():
    response = {}
    response['stations'] = WebDataHelper.list_stations()
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=config.PORT, threaded=True)
