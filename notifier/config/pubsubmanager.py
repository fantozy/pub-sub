import redis
from django.conf import settings

REDIS_HOSTNAME = settings.REDIS_HOSTNAME
REDIS_PORT = settings.REDIS_PORT
DEFAULT_CHANNEL = settings.DEFAULT_CHANNEL

class PubSubManager:
    def __init__(self, host: str = REDIS_HOSTNAME, port: int = REDIS_PORT):
        self.host = host
        self.port = port
        self.redis_connection = None
        self.pubsub = None

    def _get_redis_connection(self):
        return redis.Redis(
            host=self.host,
            port=self.port
        )

    def connect(self):
        self.redis_connection = self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    def _publish(self, channel: str = DEFAULT_CHANNEL, message: str = None):
        self.redis_connection.publish(channel, message)
