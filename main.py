from flask import Flask
from flask import request
from flask import send_file

from inference import Inference


model = None
waveglow = None
inference = Inference()
model, waveglow = inference.load_model()



app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def start():

    req_data = request.get_json()
    input= req_data['sentence']
    print(req_data)

    output = inference.infer(input, waveglow, model)
    return "Hello World"
    return send_file(
        open(output, "rb"),
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="output.wav")


@app.route('/index')
def index():
    return "Send me another flask response"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug = True)