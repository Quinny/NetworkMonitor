import json

def register(env):
    def pretty_json(json_str):
        return json.dumps(json.loads(json_str), sort_keys = True,
                          indent = 4, separators=(',', ': '))

    def primary_id(host):
        if len(host.host_name) > 0:
            return host.host_name
        return host.ip_address

    def secondary_id(host):
        if len(host.host_name) > 0:
            return "(" + host.ip_address + ")"
        return ""

    env.filters["pretty_json"]  = pretty_json
    env.filters["primary_id"]   = primary_id
    env.filters["secondary_id"] = secondary_id
