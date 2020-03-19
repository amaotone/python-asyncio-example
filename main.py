from datetime import datetime
import asyncio

from timer import timer


async def say(delay, message):
    await asyncio.sleep(delay)
    print(message)
    return message


async def with_await():
    """単にawaitすると直列に実行されるので3秒かかる"""

    with timer("with await"):
        await say(1, "hello")
        await say(2, "world")


async def with_task():
    """Taskを使うと並列に実行されるので2秒で終わる"""

    task1 = asyncio.create_task(say(1, "hello"))
    task2 = asyncio.create_task(say(2, "world"))

    with timer("with task"):
        await task1
        await task2


async def with_gather():
    """gatherを使うと与えたawaitableをTaskとして並行実行し、結果をリストで返す"""

    with timer("with gather"):
        results = await asyncio.gather(say(2, "world"), say(1, "hello"))
        print("results: ", results)  # ["world", "hello"]


async def main():
    """非同期処理のエントリーポイント"""
    await with_await()
    await with_task()
    await with_gather()


if __name__ == "__main__":
    # asyncio.run()はエントリーポイントを呼び出す1回だけ使われるべき
    asyncio.run(main())
