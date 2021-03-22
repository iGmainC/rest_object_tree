from pprint import pprint

import redis
import json

HOST = '127.0.0.1'
PORT = 6379
PASSWORD = 'qq1224731137'

pool = redis.ConnectionPool(host=HOST, password=PASSWORD, port=PORT, max_connections=128)


class ObjectTree:
    types = [
        type(int()),
        type(str()),
        type(list()),
        type(dict()),
        type(set()),
        type(tuple())
    ]
    tree = None
    value_raw = None

    def __init__(self, value):
        self.value_raw = value
        self.gen_tree()

    def gen_tree(self):
        general_type = [
            type(int()),
            type(str())
        ]
        set_type = [
            type(list()),
            type(set()),
            type(tuple())
        ]

        def test(obj):
            if type(obj) in general_type:
                return type(obj)
            else:
                if type(obj) in set_type:
                    tree = []
                    for son in obj:
                        tree.append(test(son))
                elif type(obj) == type(dict()):
                    tree = {}
                    for key in obj:
                        tree[key] = test(obj[key])
                return tree

        self.tree = test(self.value_raw)


def redis_set(key: str, value: object, tree: ObjectTree, **param):
    r = redis.Redis(connection_pool=pool)
    if type(value) is type(str()):
        return r.set(key, value, **param)
    elif type(value) is type(list()):
        pass


if __name__ == "__main__":
    # set('aaa', 'bbb', ex=10)
    ObjectTree([{},{}])
