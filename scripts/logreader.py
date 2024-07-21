import os
import json
import markdown2

def as_html(data):
    return markdown2.markdown(data, extras=["fenced-code-blocks", "tables"])

def get_log(log_path = r"..\log", last=10):
    print(log_path)
    if os.path.exists(log_path) == False:
        print(f"{log_path} doesn't exist.")
        return
    files = os.listdir(log_path)
    files = [f for f in files if f.endswith(".txt")][-last:]
    files.sort(reverse=True)
    for file in files[:10]:
        full_path = os.path.join(log_path, file)
        print(f"- {full_path}")
        # yield as_html(f"## {full_path}")
        f = open(full_path, "r")
        d = json.load(f)
        user_prompt = as_html(f"{d['user_prompt']}")
        user_prompt = f"<div id='prompt-input'>{user_prompt}</div>"
        response = as_html(d['response'])
        yield user_prompt
        yield response

def write_logs_to_html(log_path = r"..\log"):
    md = ""
    for record in get_log(log_path):
        md += record

    html = rf"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Log</title>
        <style>body{{font-family:calibri; padding: 1px 1px 1px 1px; line-height: 140%;}} code, pre{{background-color:whitesmoke; padding: 0.5em;}}</style>
    </head>
    <body>
    {md}
    </body>
    </html>
    """
    with open(os.path.join(log_path, "index.html"), "w") as f:
        f.write(html)

# write_logs_to_html(".\log")
