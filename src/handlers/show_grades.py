import asyncio

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery

from src.keyboards import generate_subjects_kb
from src.states import Subjects
from src.models import StudentPerformance, NzUaAPI, Mark, Subject
from src.texts import TEXTS
from src.database.dao import DAO
from src.utils import logger
from src.utils.sorting import ukrainian_sort_key


async def ask_subject(message: Message, state: FSMContext, dao: DAO):
    """
    Sends user its performance for selected parameters
    """

    await Subjects.subject.set()
    loading_msg = await message.answer(TEXTS.MARKS.LOADING)

    user = await dao.user.get_by_id(message.from_user.id)
    await dao.action.create(message.from_user.id, user.student_id, "show_grades")

    student_performance = await prepare_student_performance(
        user.student_id, dao, user.access_token, from_db=False
    )

    marks = await update_marks(message.from_user.id, student_performance, dao)
    print(marks)

    await state.update_data(student_performance=student_performance)
    subjects = await student_performance.get_subjects_names()

    await loading_msg.delete()
    await message.answer(
        TEXTS.MARKS.ASK_SUBJECT, reply_markup=await generate_subjects_kb(subjects)
    )

    await asyncio.sleep(3)
    await notify_about_updates(
        message.bot, message.from_user.id, marks["new_marks"], marks["deleted_marks"]
    )


async def show_grades(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Sends user grades for selected subject
    """

    await call.message.delete()

    async with state.proxy() as data:
        student_performance: StudentPerformance = data.get("student_performance")

    if not student_performance:
        await state.finish()
        await call.message.answer("Something went wrong.. Please, contact the support.")
        logger.error(f"No StudentPerformance in callback data. {state.proxy()}")
        return

    subject_name = callback_data["name"]

    if subject_name == "Всі предмети":
        subjects = await student_performance.get_subjects()
        show_detailed = False
    else:
        subjects = [await student_performance.get_subject_by_name(subject_name)]
        show_detailed = True

    for subject in subjects:
        marks = await subject.get_marks_formatted(detailed=show_detailed)
        await call.message.answer(marks)
        await asyncio.sleep(0.5)

    await state.finish()


async def update_marks(user_id: int, student_performance: StudentPerformance, dao: DAO):
    """
    Updates marks in database with current ones (adding and deleting)
    """

    user = await dao.user.get_by_id(user_id)
    all_new_marks = []
    all_deleted_marks = []
    for subject in await student_performance.get_subjects():

        db_marks = await dao.mark.get_marks_for_subject(user.student_id, subject.id)
        db_marks = {mark.lesson_id: mark for mark in db_marks}

        api_marks = {mark.lesson_id: mark for mark in subject.marks}

        new_marks = {id: mark for id, mark in api_marks.items() if id not in db_marks}
        deleted_marks = {
            id: mark for id, mark in db_marks.items() if id not in api_marks
        }

        all_new_marks.extend(new_marks.values())
        all_deleted_marks.extend(deleted_marks.values())

        for mark in new_marks.values():
            logger.info(f"Creating new mark for user {user_id}.\n{mark = }")
            await dao.mark.create(
                chat_id=user_id,
                student_id=user.student_id,
                subject_name=subject.name,
                subject_id=subject.id,
                mark=mark.mark,
                lesson_date=mark.date,
                lesson_type=mark.lesson_type,
                comment=mark.comment,
                lesson_id=mark.lesson_id,
            )

        for mark in deleted_marks.values():
            logger.info(f"Deleting mark for user {user_id}.\n{mark = }")
            await dao.mark.delete(user.student_id, mark.lesson_id)

    return {"new_marks": all_new_marks, "deleted_marks": all_deleted_marks}


async def notify_about_updates(bot, user_id: int, new_marks: list, deleted_marks: list):

    if not new_marks and not deleted_marks:
        return

    msg = "🔔 Оновлення:"

    if new_marks:
        msg += "\n\n<u>Нові оцінки:</u>"

    for mark in new_marks:
        # msg += f"\n🔖 <b>{mark.subject_name}</b> - <i>{mark.mark}</i> ({mark.lesson_type}) - {mark.date_str()}"
        msg += f"\n🔖 <b>{mark.subject_name}</b> - {str(mark)}"

        if mark.comment:
            msg += f"- {mark.comment}"

    if deleted_marks:
        msg += "\n\n<u>Видалені оцінки:</u>"

    for mark in deleted_marks:
        msg += f"\n🗑 <b>{mark.subject_name}</b> - <i>{mark.mark}</i> ({mark.lesson_type}) - {mark.lesson_date.strftime('%d.%m.%Y')}"

    await bot.send_message(user_id, msg)


async def prepare_student_performance(
    student_id: int, dao: DAO, access_token: str, from_db: bool = False
):

    logger.info(f"Preparing student performance for student {student_id}")

    final_subjects = []

    if not from_db:
        nz_ua = NzUaAPI(access_token)
        performance_json = await nz_ua.get_student_performance()

        logger.info(
            f"Got student performance for student {student_id}.\n{performance_json = }"
        )
        subjects = performance_json["subjects"]

        for subject_json in subjects:
            subject_grades = await nz_ua.get_subject_grades(subject_json["subject_id"])
            logger.info(
                f"Got subject grades for student {student_id}.\n{subject_grades = }"
            )

            subject_grades = [
                Mark(
                    grade_json["mark"],
                    grade_json["lesson_date"],
                    grade_json["lesson_type"],
                    grade_json["comment"],
                    grade_json["subject"],
                    grade_json["lesson_id"],
                )
                for grade_json in subject_grades["lessons"]
            ]
            final_subjects.append(
                Subject(
                    subject_json["subject_name"],
                    subject_json["subject_id"],
                    subject_grades,
                )
            )
    else:
        subjects = await dao.mark.get_subjects_for_student(student_id)

        for subject_id in subjects:
            marks = await dao.mark.get_marks_for_subject(student_id, subject_id)
            subject_grades = [
                Mark(
                    mark.mark,
                    mark.lesson_date,
                    mark.lesson_type,
                    mark.comment,
                    mark.subject,
                    mark.lesson_id,
                )
                for mark in marks
            ]

            final_subjects.append(
                Subject(subject_grades[0].subject_name, subject_id, subject_grades)
            )

        final_subjects.sort(key=lambda x: x.name)
        # print(['|' + i.name + '' for i in sorted(final_subjects, key=lambda x: x.name)])
    return StudentPerformance(
        sorted(final_subjects, key=lambda x: ukrainian_sort_key(x.name))
    )
