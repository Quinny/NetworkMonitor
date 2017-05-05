import json

def register(env):
    def pretty_json(json_str):
        return json.dumps(json.loads(json_str), sort_keys = True,
                          indent = 4, separators=(',', ': '))

    env.filters["pretty_json"] = pretty_json
