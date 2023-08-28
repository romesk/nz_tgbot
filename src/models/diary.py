from datetime import datetime
from typing import Optional

from src.texts import TEXTS


class Diary:

    def __init__(self, diary_json: dict):
        self.json = diary_json

        self.dates = self.json['dates']  # list of days of a week
        self.number_emojis = ('0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟')

    async def found_weekday_in_diary(self, date: str = None, day_num: int = None) -> Optional[dict]:
        """
        Found if day is present in the current diary by date of day or week day number
        :param date: date in format YYYY-MM-DD
        :param day_num: week day number (0-6). e.g 0 for Monday, 1 for Tuesday, etc.
        :return: day if is present, None otherwise
        """

        days = None

        if date:
            days = [day for day in self.dates if day['date'] == date]
        elif day_num:
            days = [day for day in self.dates if datetime.strptime(day['date'], "%Y-%m-%d").weekday() == day_num]

        return days[0] if days else None

    async def get_diary_for_day(self, date: str, day_num: int = None) -> str:
        """
        Returns formatted diary for a passed day by its date
        :param date: date in format YYYY-MM-DD
        :param day_num: week day number (0-6). e.g 0 for Monday, 1 for Tuesday, etc.
        """

        day = await self.found_weekday_in_diary(date=date, day_num=day_num)

        if not day_num:
            day_num = datetime.strptime(date, "%Y-%m-%d").weekday()

        # header line for a day
        weekdays = ('Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя')
        res_str = f"<b>{weekdays[day_num]}</b> - {datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y')}\n\n"

        if not day:
            # notify user that there is no data for this day
            return res_str + TEXTS.DIARY.DAY_NOT_FOUND

        calls = day['calls']

        for call in calls:
            # process each call (lesson)
            for subject in call['subjects']:
                # process each subject in a call (maybe more than one)

                # process lesson number to convert it to emoji
                call_number = call['call_number']
                if call_number is None:
                    call_number = '❔'
                elif call_number < 11:
                    call_number = self.number_emojis[call_number]
                else:
                    call_number = self.number_emojis[1] + self.number_emojis[call_number % 10]

                # lesson title
                res_str += f"{call_number} <b>{subject['subject_name']}</b>\n"

                # lesson homework
                for hometask in subject['hometask']:
                    if hometask:
                        res_str += f"🔹 Домашнє завдання: <i>{hometask}</i>\n"

                # lesson mark
                for lesson in subject['lesson']:
                    if lesson['mark']:
                        res_str += f"🔸 Оцінка: {lesson['mark']} - <i>{lesson['type']} " \
                                   f"{'(' + lesson['comment'] + ')' if lesson['comment'] else ''}</i>\n"

                # divider
                if call != calls[-1]:
                    res_str += "〰️" * 10 + "\n"

        return res_str



