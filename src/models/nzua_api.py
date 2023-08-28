from datetime import datetime, timedelta

from aiocfscrape import CloudflareScraper


class NzUaAPI:
    """
    Diary API for nz.ua
    """

    def __init__(self, bearer_token: str = None) -> None:
        self.headers = {"user-agent": "IRC RESTClient", "accept": "application/json"}

        if bearer_token is not None:
            self.headers["Authorization"] = "Bearer " + bearer_token

    async def authentificate(self, username: str, password: str) -> dict:
        """
        Authentificate user with username and password
        """

        data = {"username": username, "password": password}

        async with CloudflareScraper() as session:
            async with session.post("https://api-mobile.nz.ua/v1/user/login", data=data, headers=self.headers) as resp:
                return await resp.json()

    async def get_diary(self, start_date: str = None, end_date: str = None) -> dict:
        """
        Get user's diary
        :param start_date: start date of diary, if None, then 10 days ago
        :param end_date: end date of diary, if None, then today
        """

        if "Authorization" not in self.headers:
            raise Exception("You must authentificate first")

        data = {
            "start_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d") if not start_date else start_date,
            "end_date": datetime.now().strftime("%Y-%m-%d") if not end_date else end_date,
        }

        async with CloudflareScraper() as session:
            async with session.post(
                "https://api-mobile.nz.ua/v1/schedule/diary", data=data, headers=self.headers
            ) as resp:
                return await resp.json()

    async def _get_current_semester_range(self):
        """
        Counts current semester date ranges
        """
        
        today = datetime.now().today()

        # get current semester date ranges
        if today.month < 9:
            start_date = f"{today.year}-01-01"
            end_date = f"{today.year}-08-31"
        else:
            start_date = f"{today.year}-09-01"
            end_date = f"{today.year}-12-31"

        return {'start_date': start_date,
            'end_date': end_date}

    async def get_student_performance(self, start_date: str = None, end_date: str = None) -> dict:
        """
        Get user's performance
        :param start_date: start date of diary (YYYY-MM-DD), if None, then selects the whole semester
        :param end_date: end date of diary (YYYY-MM-DD), if None, then selects the whole semester
        """

        if "Authorization" not in self.headers:
            raise Exception("You must authentificate first")

        if not start_date:
            start_date = (await self._get_current_semester_range()).get('start_date')
        if not end_date:
            end_date = (await self._get_current_semester_range()).get('end_date')

        data = {"start_date": start_date, "end_date": end_date}

        async with CloudflareScraper() as session:
            async with session.post(
                "https://api-mobile.nz.ua/v1/schedule/student-performance", data=data, headers=self.headers
            ) as resp:
                return await resp.json()

    async def get_subject_grades(self, subject_id: str, start_date: str = None, end_date: str = None) -> dict:
        """
        Get all grades for subject by its id
        :param subject_id: id of subject to get grades
        :param start_date: start date of diary (YYYY-MM-DD), if None, then selects the whole semester
        :param end_date: end date of diary (YYYY-MM-DD), if None, then selects the whole semester
        """

        if "Authorization" not in self.headers:
            raise Exception("You must authentificate first")

        if not start_date:
            start_date = (await self._get_current_semester_range()).get('start_date')
        if not end_date:
            end_date = (await self._get_current_semester_range()).get('end_date')

        data = {'start_date': start_date, 'end_date': end_date, 'subject_id': subject_id}

        async with CloudflareScraper() as session:
            async with session.post(
                "https://api-mobile.nz.ua/v1/schedule/subject-grades", data=data, headers=self.headers
            ) as resp:
                return await resp.json()

