from subconscious.model import RedisModel, Column
import json

class Host(RedisModel):
    ip_address   = Column(type=str, primary_key=True)
    host_name    = Column(type=str, required=True)
    scanned_at   = Column(type=str, required=True)
    scan_results = Column(type=str, required=True)
    up           = Column(type=int, required=True, index=True)

    def from_nmap_scan_result(ip, result):
        return Host(
            ip_address   = ip,
            host_name    = result["scan"][ip]["hostnames"][0]["name"]\
                           if ip in result["scan"] else "",
            scanned_at   = result["nmap"]["scanstats"]["timestr"],
            scan_results = json.dumps(result),
            up           = int(int(result["nmap"]["scanstats"]["uphosts"]) > 0)
        )
