# TODO: There has to be a better way to do relative imports than this garbage...
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from concurrent.futures import ThreadPoolExecutor
from jinja2             import Environment, FileSystemLoader, select_autoescape
from sanic              import Sanic, response
import asyncio
import json
import nmap

from models.host import Host
import db
import filters
import settings

app = Sanic(__name__)
app.static('/static', './static')
background_scan_executor = ThreadPoolExecutor()

template_env = Environment(
    loader       = FileSystemLoader("templates/"),
    autoescape   = select_autoescape(['html', 'xml']),
    enable_async = True
)
filters.register(template_env)

def use_template(template):
    def dec(f):
        async def wrap(*args, **kwargs):
            context = await f(*args, **kwargs)
            rendered = await template_env.get_template(template).render_async(
                    context)
            return response.html(rendered)
        return wrap
    return dec

async def poll_scan_queue():
    while app.is_running:
        maybe_host = await app.redis_connection.lpop("scan_queue")
        if maybe_host is not None:
            scanner = nmap.PortScanner()
            print("performing full scan on", maybe_host)
            result = await app.loop.run_in_executor(background_scan_executor, nmap.PortScanner.scan,
                    scanner, maybe_host, None, "-A --dns-servers " + settings.LOCAL_DNS_ADDR, False)
            entry = Host.from_nmap_scan_result(maybe_host, result)
            await entry.save(app.redis_connection)
            print(maybe_host, "scan complete")
        await asyncio.sleep(5)

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

@app.route("/scan/<host>")
async def scan(request, host):
    await app.redis_connection.lpush("scan_queue", host)
    return response.json({"status": "ok"})

if __name__ == '__main__':
    app.add_task(poll_scan_queue())
    app.run(host="0.0.0.0", port=settings.WEB_UI_PORT)
