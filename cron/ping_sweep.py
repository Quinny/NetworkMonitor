# Ping sweep the local network and store the results in Redis.
#
# The python-nmap package does include an AsyncPortScanner module but it is
# very slow, so I have rewritten this functionality using python3 asyncio.

# TODO: There has to be a better way to do relative imports than this garbage...
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import nmap
import ipaddress
import json
from concurrent.futures import ThreadPoolExecutor

import settings
from models.host import Host
import db

executor = ThreadPoolExecutor()
loop     = asyncio.get_event_loop()

# Check if the results point a host that is currently online.
def is_up(scan_result):
    return int(scan_result["nmap"]["scanstats"]["uphosts"]) > 0

# Scan the host and store the results in Redis.
async def scan_and_report(host, redis_connection):
    print("scanning", host)
    scanner  = nmap.PortScanner()
    # Run in executor doesn't allow for kwargs, so the arguments passed here
    # are: self, host, ports, arguments.
    result = await loop.run_in_executor(executor, nmap.PortScanner.scan,
            scanner, host, None, "-sn")
    entry = Host(
        ip_address   = host,
        scanned_at   = result["nmap"]["scanstats"]["timestr"],
        scan_results = json.dumps(result),
        up           = int(is_up(result))

    )
    await entry.save(redis_connection)

# Generate the IP addresses of all hosts within the provided network mask.
def host_generator():
    yield from map(str, ipaddress.ip_network(settings.NETWORK_MASK))

# Main worker function.
async def scan_all():
    redis_connection = await db.connect()
    scan_tasks = [scan_and_report(host, redis_connection)
                  for host in host_generator()]
    await asyncio.wait(scan_tasks)
    redis_connection.close()
    await redis_connection.wait_closed()

loop.run_until_complete(scan_all())
loop.close()
