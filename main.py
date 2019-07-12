from flask import Flask
from flask import request, render_template
from flask import send_file
import helper
import concurrent.futures
import datetime

from inference import Inference


inference = Inference()
inference.load_model()


app = Flask(__name__, template_folder='static')


@app.route('/',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        val = request.form['sentence']
        sentence_list = helper.split_sentences(val)
        result_list = []
        result = None
        start = datetime.datetime.now()
        #with concurrent.futures.ProcessPoolExecutor() as pool:
        count = 0
        for s in sentence_list:
            if s:
                print(count, " ", s)
                result_list.append(inference.infer(s))
                count += 1

            #future_result = pool.submit(inference.infer, s)
            #future_result.add_done_callback(result_list)

        if len(sentence_list) > 1:
            result = helper.merge_wav(result_list)
        else:
            if len(result_list==1):
                result = result_list[0]

        stop = datetime.datetime.now()
        time = (stop - start) /1000

        template_data = {
            'sentence': result,
            'time': str(time.microseconds)
        }
        return render_template('index.html', **template_data)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug = False)
