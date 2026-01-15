from app.db.redis_session import get_redis_connection
import asyncio

async def main():
    result,redis_conn = await get_redis_connection()
    print(result)
    return result

if __name__ == "__main__":
    asyncio.run(main())