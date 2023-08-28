import asyncio
from datetime import datetime, timedelta

from aiocfscrape import CloudflareScraper


async def authenticate(username: str, password: str):
    """
    Authenticate user and return response dict with access_token
    """

    data = {
        "username": username,
        "password": password
    }

    headers = {
        "user-agent": "IRC RESTClient",
        "accept": "application/json"
    }

    async with CloudflareScraper() as session:
        async with session.post("https://api-mobile.nz.ua/v1/user/login", data=data, headers=headers) as resp:
            return await resp.json()


async def get_diary(access_token: str, start_date: str = None, end_date: str = None):
    """
    Get user's diary
    :param access_token: user's bearer token
    :param start_date: start date of diary, if None, then 10 days ago
    :param end_date: end date of diary, if None, then today
    """

    headers = {
        "Authorization": "Bearer " + access_token,
        "user-agent": "IRC RESTClient",
        "accept": "application/json"
    }

    data = {
        "start_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d") if start_date is None else start_date,
        "end_date": datetime.now().strftime("%Y-%m-%d") if end_date is None else end_date
    }

    async with CloudflareScraper() as session:
        async with session.post("https://api-mobile.nz.ua/v1/schedule/diary", data=data, headers=headers) as resp:
            return await resp.json()


async def get_student_performance(access_token: str, start_date: str = None, end_date: str = None):
    """
    Get user's performance
    :param access_token: user's bearer token
    :param start_date: start date of diary, if None, then selects the whole semester
    :param end_date: end date of diary, if None, then selects the whole semester
    """

    if not start_date or not end_date:
        today = datetime.now().today()

        # get current semester date ranges
        if today.month < 9:
            start_date = f"{today.year}-01-01"
            end_date = f"{today.year}-08-31"
        else:
            start_date = f"{today.year}-09-01"
            end_date = f"{today.year}-12-31"

    data = {
        "start_date": start_date,
        "end_date": end_date
    }

    headers = {
        "Authorization": "Bearer " + access_token,
        "user-agent": "IRC RESTClient",
        "accept": "application/json"
    }

    async with CloudflareScraper() as session:
        async with session.post(
                "https://api-mobile.nz.ua/v1/schedule/student-performance", data=data, headers=headers) as resp:
            return await resp.json()


async def main():
    print(await authenticate("skok_daniil", "dania1506"))


if __name__ == "__main__":

    # print(authentificate("skok_daniil", "dania1506"))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
