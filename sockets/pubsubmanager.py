import redis.asyncio as aioredis
from settings import REDIS_HOSTNAME, REDIS_PORT, DEFAULT_CHANNEL

class PubSubManager:
    def __init__(self, host: str = REDIS_HOSTNAME, port: int = REDIS_PORT):
        self.host = host
        self.port = port

        self.pubsub = None

    async def _get_redis_connection(self):
        return aioredis.Redis(
            host=self.host,
            port=self.port,
            auto_close_connection_pool=False
        )

    async def connect(self):
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def _publish(self, channel: str = DEFAULT_CHANNEL, message: str = None):
        await self.redis_connection.publish(channel, message)

    async def subscribe(self, channel: str = DEFAULT_CHANNEL):
        await self.pubsub.subscribe(channel)
        return self.pubsub
    
    
    async def unsubscribe(self, channel = DEFAULT_CHANNEL):
        await self.pubsub.unsubscribe(channel)