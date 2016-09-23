from flask import Flask, render_template, request, jsonify
import setproctitle
import config
from helpers.RedisHelper import RedisHelper
from helpers import css3colors

__author__ = 'joe'
setproctitle.setproctitle("neatlightsflask")
app = Flask(__name__)


@app.route('/', methods=["GET"])
def main():
    if request.method == "GET":
        return render_template("index.html")


@app.route('/colors', methods=["GET"])
def colors():
    response = {}
    response["colors"] = css3colors.css3colors
    return jsonify(response)


@app.route('/send', methods=["GET"])
def send():
    response = {"status": "None"}
    #  thash = request.args.get('hash')
    #  /send?count=630&brightness=50&senselight=0&style=Room%20Lighting&color=orange&method_name=room_lighting

    try:
        message = {
            'led_count': int(request.args.get('count')),  # 630,
            'brightness': int(request.args.get('brightness')),  # 10,
            'senselight': int(request.args.get('senselight')),  # 0,
            'style_name': request.args.get('style'),  # 'Room Lighting',
            'color': [request.args.get('color').lower()],  # ['blue'],
            'method_name': request.args.get('method')  # 'room_lighting'
        }
        if message['color'][0].lower() not in css3colors.css3colors or message[
                'color'][0].lower() == 'random':
            message['color'] = css3colors.rand_single_color()
            response[
                'info'] = "Random color selected or color not found.  Rancom color was used."
    except Exception as e:
        response['status'] = "error"
        response[
            'info'] = "Something went wrong when parsing message.  Please check query params."
        response['error'] = str(e)
        return jsonify(response)

    try:
        print(message)
        RedisHelper().publish(channel=config.PUBSUB_NAME, message=message)
        response["status"] = "success"
        response['message'] = message
    except:
        response["status"] = "error"

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=config.PORT, threaded=True)
