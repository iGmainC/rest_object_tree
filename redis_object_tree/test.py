import pickle
import zlib

import redis

pool = redis.ConnectionPool(host='127.0.0.1', max_connections=128)


class ObjectTree:
    type_of = None
    data = None

    def __init__(self, obj):
        from collections.abc import Iterable
        # 可迭代 和 不可迭代，dict除外
        not_iterable_types = [
            type(int()),
            type(str()),
            type(float())
        ]
        iterable_types = [
            type(list()),
            type(tuple()),
            type(set())
        ]
        if type(obj) in not_iterable_types:
            # 如果 不是 原生的可迭代类型
            self.data = obj
            self.type_of = type(obj)
        elif type(obj) in iterable_types:
            # 如果 是 原生的可迭代类型
            self.data = []
            self.type_of = type(list())
            for v in obj:
                self.data.append(ObjectTree(v))
        elif type(obj) == type(dict()):
            self.type_of = type(dict())
            self.data = {}
            for k in obj:
                self.data[k] = ObjectTree(obj[k])
        else:
            # 如果都不是，则序列化，并压缩
            self.type_of = type(type)
            self.data = pickle.dumps(obj)
            self.data = zlib.compress(self.data, zlib.Z_DEFAULT_COMPRESSION)


class RedisTree:
    r = redis.Redis(connection_pool=pool)
    r.set()

    def __init__(self, key, obj):
        pass


if __name__ == "__main__":
    a = ObjectTree({'a': 1, 'b': [1, 2, 3]})
    print('aaa')
