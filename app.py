from flask import Flask, render_template, request, Response
from scripts.wrapper import gptwrapper as gw
import scripts.logreader as lr
from markdown2 import markdown
from datetime import datetime
import json
import markdown2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listlogs')
def listlogs():
    return render_template('listlogs.html')


@app.route('/', methods=['POST'])
def process():
    prompt_text = request.form["input_text"]
    system_prompt = "Start the response with a title."
    g = gw(system_prompt=system_prompt)
    g.request_text(prompt_text)

    g.dump(request.remote_addr)

    return render_template('index.html', prompt_text=markdown(g.user_prompt, extras=["fenced-code-blocks"]),
                           gpt_response_text=markdown(g.response, extras=["fenced-code-blocks", "tables"]))

def d():
    yield from lr.get_log(".\log", last=50)


@app.route('/stream')
def stream():
    def generate():
        yield f"data: Task is complete\n\n"
        for i in d():
            print(i)
            data = markdown2.markdown(i, extras=["fenced-code-blocks", "tables"])
            # data = data.replace('\n', '')
            data = json.dumps({"d": data})
            yield f"data: {data}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host="njbedw2", port=80, debug=True)
