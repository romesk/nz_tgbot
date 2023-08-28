from datetime import date, datetime


class Mark:
    def __init__(
        self,
        mark: int,
        lesson_date: date,
        lesson_type: str,
        comment: str,
        subject_name: str,
        lesson_id: int,
    ):
        try:
            self.mark: int = int(mark)
        except ValueError:
            self.mark = 0  # expected zero to be as teacher remark

        if isinstance(lesson_date, str):
            self.date: date = datetime.strptime(lesson_date, "%Y-%m-%d")
        else:
            self.date = lesson_date

        self.lesson_type = lesson_type
        self.comment = comment
        self.subject_name = subject_name
        self.lesson_id: int = int(lesson_id)

    def date_str(self):
        return datetime.strftime(self.date, "%d.%m.%Y")

    def __str__(self):
        res = f"<b>{self.mark if self.mark else 'Зауваження'}</b>" \
              f"{' (' + self.lesson_type + ')' if self.mark else ''} - {datetime.strftime(self.date, '%d.%m.%Y')}"

        if self.comment:
            res += f" - <i>{self.comment}</i>"

        return res

    def __int__(self):
        return self.mark


class Subject:
    def __init__(self, name: str, id: int, marks: list[Mark]):
        self.name = name
        self.id: int = int(id)
        self.marks = marks

    async def get_marks_list(self) -> list:
        return [
            mark.mark
            for mark in sorted(self.marks, key=lambda x: x.date, reverse=True)
            if mark.mark != 0
        ]

    async def get_marks_formatted(self, detailed: bool = False):
        header = f"🔸 Оцінки з предмету <b>{self.name}</b>:\n"

        marks_list = await self.get_marks_list()  # get list of marks without zero

        if not detailed:
            marks = f"<i>{', '.join(map(str, marks_list))}</i>"
        else:
            marks = "\n".join(map(str, self.marks))

        footer = f"\n\n▫️ Середній бал за весь час: <b>{round(sum(map(int, marks_list)) / len(marks_list), 2)}</b>"

        return header + marks + footer
