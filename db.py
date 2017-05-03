import aioredis
import settings

async def connect(loop = None):
    conn = await aioredis.create_redis(
        address = (
            settings.REDIS_HOST,
            settings.REDIS_PORT
        ),
        encoding = 'utf-8',
    )
    return conn
