from flask import Flask
from flask import request
from flask import send_file

from inference import Inference


model = None
waveglow = None
inference = Inference()
model, waveglow = inference.load_model()



app = Flask(__name__)
@app.route('/', methods=['POST'])
def start():

    req_data = request.get_json()
    input= req_data['sentence']

    output = inference.infer(input, waveglow, model)

    return "Hello world, how is it going"

    return send_file(
        output,
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="ouput.wav")


@app.route('/index')
def index():
    return "Send me another flask response"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug = True)