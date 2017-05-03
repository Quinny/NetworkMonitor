# TODO: There has to be a better way to do relative imports than this garbage...
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sanic import Sanic, response
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

import db
from models.host import Host

app = Sanic(__name__)

template_env = Environment(
    loader       = FileSystemLoader("templates/"),
    autoescape   = select_autoescape(['html', 'xml']),
    enable_async = True
)

def pretty_json(json_str):
    return json.dumps(json.loads(json_str), sort_keys = True,
                      indent = 4, separators=(',', ': '))

template_env.filters["pretty_json"] = pretty_json

def use_template(template):
    def dec(f):
        async def wrap(*args, **kwargs):
            context = await f(*args, **kwargs)
            rendered = await template_env.get_template(template).render_async(
                    context)
            return response.html(rendered)
        return wrap
    return dec

@app.listener('before_server_start')
async def before_server_start(app, loop):
    app.redis_connection = await db.connect(loop)

@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    app.redis_connection.close()
    await app.redis_connection.wait_closed()

@app.route("/")
@use_template("index.html")
async def index(request):
    recently_up = [host async for host in Host.filter_by(
            db = request.app.redis_connection, up = 1)]
    return {"hosts" : recently_up}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
