# TODO: There has to be a better way to do relative imports than this garbage...
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import nmap
import ipaddress

import settings
from models.host import Host
import db

scanner = nmap.PortScanner()

def is_up(scan_result):
    return int(scan_result["nmap"]["scanstats"]["uphosts"]) > 0

async def scan_and_report(host, redis_connection):
    print("scanning", host)
    result = scanner.scan(host, arguments="-sn")
    entry = Host(
        ip_address   = host,
        scanned_at   = result["nmap"]["scanstats"]["timestr"],
        scan_results = str(result),
        up           = int(is_up(result))

    )
    await entry.save(redis_connection)

def host_generator():
    yield from map(str, ipaddress.ip_network(settings.NETWORK_MASK))

async def scan_all():
    redis_connection = await db.connect()
    print(redis_connection)
    scan_tasks = [scan_and_report(host, redis_connection)
                  for host in host_generator()]
    await asyncio.wait(scan_tasks)
    redis_connection.close()
    await redis_connection.wait_closed()

loop  = asyncio.get_event_loop()
loop.run_until_complete(scan_all())
loop.close()
