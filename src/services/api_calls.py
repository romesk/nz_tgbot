import asyncio

import aiohttp


async def authentificate(username: str, password: str):
    data = {
        "username": username,
        "password": password
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api-mobile.nz.ua:443/v1/user/login", data=data) as response:
            return await response.json()


async def get_diary():
    headers = {"Authorization": "Bearer " + await authentificate("skok_daniil", "dania1506")}
    data = {
        "start_date": "2022-01-17",
        "end_date": "2022-01-23"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://api-mobile.nz.ua:443/v1/schedule/diary", headers=headers, data=data) as response:
            from pprint import pprint
            marks = await response.json()
            pprint(marks)


async def main():
    await get_diary()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
