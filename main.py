import time
from datetime import datetime
import asyncio

from timer import timer


async def say(delay, message):
    await asyncio.sleep(delay)
    print(f"{message} ({delay}s)")
    return message


async def block_say(delay, message):
    """ブロックしてしまう場合はrun_in_evecutorを使えばよい"""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: time.sleep(delay))
    print(f"{message} ({delay}s)")
    return message


async def with_await():
    """単にawaitすると直列に実行されるので3秒かかる"""

    with timer("with await"):
        await say(2, "hello")
        await say(1, "world")


async def with_task():
    """Taskを使うと並列に実行されるので2秒で終わる"""

    task1 = asyncio.create_task(say(2, "hello"))
    task2 = asyncio.create_task(say(1, "world"))

    with timer("with task"):
        await task1
        await task2


async def with_gather():
    """gatherを使うと与えたawaitableをTaskとして並行実行し、結果をリストで返す"""

    with timer("with gather"):
        results = await asyncio.gather(say(2, "hello"), say(1, "world"))
        print("results:", results)


async def with_blocking_function():
    """ブロックしてしまう関数はラップすれば同様に扱える"""

    with timer("with blocking function"):
        results = await asyncio.gather(block_say(2, "hello"), block_say(1, "world"))
        print("results:", results)


async def main():
    """非同期処理のエントリーポイント"""

    await with_await()
    await with_task()
    await with_gather()
    await with_blocking_function()


if __name__ == "__main__":
    # asyncio.run()はエントリーポイントを呼び出す1回だけ使われるべき
    asyncio.run(main())
