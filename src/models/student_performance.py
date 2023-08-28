from src.models.performance_components import Subject


class StudentPerformance:

    def __init__(self, subjects: list[Subject]):
        self._subjects = subjects

    async def get_subjects(self) -> list[Subject]:
        """
        Get list of subjects
        """
        return self._subjects

    async def get_subjects_names(self) -> list[str]:
        """
        Get list of subjects names
        """
        return [subject.name for subject in self._subjects]

    async def get_subject_marks_list(self, subject_name: str) -> list:
        """
        Get subject performance
        """
        for subject in self._performance_json["subjects"]:
            if subject["subject_name"] == subject_name:
                return list(map(int, subject["marks"]))
        return []

    # async def get_subject_performance(self, subject_name: str, detailed: bool = False) -> str:
    #     """
    #     Get subject performance and return it as a formatted string
    #     """
    #
    #     # subject_id = await self.get_subject_id(subject_name)
    #     # if not subject_marks_list:
    #     #     subject_marks_list = await self.get_subject_marks_list(subject_name)
    #     subject = await self.get_subject_by_name(subject_name)
    #
    #     return f"🔸 Оцінки з предмету <b>{subject_name}</b>:\n" \
    #            f"<i>{', '.join(map(str, subject_marks_list))}</i>\n\n" \
    #            f"▫️ Середній бал: <b>{round(sum(map(int, subject_marks_list)) / len(subject_marks_list), 2)}</b>"

    async def get_subject_id(self, subject_name: str) -> int:
        """
        Get subject id by its name
        """
        for subject in self._performance_json["subjects"]:
            if subject["subject_name"] == subject_name:
                return int(subject["subject_id"])

    async def get_subject_by_name(self, subject_name: str) -> Subject:
        """
        Get subject by its name
        """
        for subject in self._subjects:
            if subject.name == subject_name:
                return subject

