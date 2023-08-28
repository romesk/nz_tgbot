"""
This class is used to simplify modifying bot's messages text and manage it.
"""


class TEXTS:
    """
    All the texts used in the bot
    """

    class START:
        """
        Texts used in the start command
        """

        HELLO = "👋 Вітаю у боті NzUa. Головна ціль - зробити зручного Телеграм помічника, " \
                "щоб користуватись основними функціями nz.ua у твоєму улюбленому месенджері 🤩 То ж не зволікай і " \
                "тисни на кнопку нижче! 😎"

        LOGIN_BTN = "Увійти в аккаунт"

        ASK_LOGIN = "Введи свій логін 🧐"
        ASK_PASSWORD = "Введи свій пароль 🔐"

        LOGIN_SUCCESS = "Виконано успішний вхід 🔓\n<i>Щоб зберегти дані для входу у безпеці, ти можеш видалити " \
                        "їх з переписки </i>"
        WELCOME = "Ласкаво прошу, {name} 😁"

        LOGIN_FAIL = "{err_msg} 🙁"

        RETRY_LOGIN = "Спробувати ще раз"

    class DIARY:
        """
        Texts used to work with diary
        """

        ASK_WEEK = "Вибери тиждень, щоб побачити його розклад 📅"
        ASK_WEEK_DAY = "Вибери день тижня, щоб побачити розклад на нього"

        LOADING = "Завантажую розклад.. 📚"

        DAY_NOT_FOUND = "На цей день немає інформації 🙁"

    class MARKS:
        """
        Texts used to work with marks
        """

        LOADING = "Завантажую оцінки.. 📚"
        ASK_SUBJECT = "Вибери предмет, щоб побачити його оцінки 📝"

