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


@app.route('/schedule', methods=["GET"])
def schedule_list():
    response = {
        'schedule': WebDataHelper.get_schedule()
    }
    return jsonify(response)


@app.route('/schedule/edit', methods=["POST"])
def schedule_edit():
    data = json.loads(request.data.decode('utf8'))
    print(data)
    if 'new' in data and data['new']:
        WebDataHelper.schedule_edit(data, True)
    else:
        WebDataHelper.schedule_edit(data)
    response = {"status": "submitted"}
    return jsonify(response)


@app.route('/station/edit', methods=["POST"])
def station_edit():
    response = {}
    data = json.loads(request.data.decode('utf8'))
    WebDataHelper.station_edit(data)
    return jsonify(response)


@app.route('/station/lastruns', methods=["GET"])
def station_lastruns():
    response = {
        'lastrunlist': WebDataHelper.get_last_station_run()
    }
    return jsonify(response)


@app.route('/station/nextruns', methods=["GET"])
def station_nextruns():
    response = {
        'lastrunlist': WebDataHelper.get_next_station_run()
    }
    return jsonify(response)


@app.route('/schedule/add', methods=["POST"])
def schedule_add():
    data = json.loads(request.data.decode('utf8'))
    WebDataHelper.schedule_add(data)
    response = {"status": "submitted"}
    return jsonify(response)


@app.route('/schedule/delete', methods=["POST"])
def schedule_delete():
    data = json.loads(request.data.decode('utf8'))
    WebDataHelper.schedule_delete(data['schedule_id'])
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
    if int(request.args.get('id')) == 1:
        response['chartData'] = WebDataHelper.get_chart_stats(
            int(request.args.get('id')))
    elif int(request.args.get('id')) == 2:
        response['chartData'] = WebDataHelper.chart_stats_chrono()
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
