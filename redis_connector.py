# @Date:   2020-10-16T19:19:48+05:30
# @Last modified time: 2020-10-16T20:08:35+05:30

import redis
import logging

class Cache:
    def __init__(self):

        redis_server  = "127.0.0.1"
        redis_port    = 6379
        redis_passwd  = None
        redis_db      = 3

        self.ttl      = 300
        self.redis    = redis.Redis(
                            host     = redis_server,
                            port     = redis_port,
                            password = redis_passwd,
                            db       = redis_db
                        )
        self.pipe   = self.redis.pipeline()
        self.logger = logging.getLogger()
        self.logger.debug(f"Redis: Server {redis_server}, DB: {redis_db}")

    def cache(self, k, v, ttl = None):
        if k is None:
            self.logger.debug("key is None, nothing to cache, returning")
            return
        expire = ttl or self.ttl
        self.logger.debug(f"Caching: k:{k} v:{v}, expiring after {expire}")
        self.pipe.set(k, v)
        self.pipe.expire(k, expire)
        self.pipe.execute()

    def remove_cache(self, k):
        self.logger.debug(f"Removing index {k}")
        self.pipe.delete(k)
        self.pipe.execute()

    def get(self, k):
        return self.redis.get(k)
