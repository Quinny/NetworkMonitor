import aioredis
import settings

async def connect():
    conn = await aioredis.create_redis(
        address = (
            settings.REDIS_HOST,
            settings.REDIS_PORT
        ),
        #encoding = 'utf-8',
    )
    return conn
