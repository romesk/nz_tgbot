import asyncio

import aiohttp
from bs4 import BeautifulSoup


class ParseNews:
    url = 'https://nz.ua/'

    cookies = {
        'SERVERID': 'app2',
        '_csrf': '585c6d0c400ed47a995bce33b876c9b3cadbbc809ad2423a2349ad54d7d3b8e0a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf'
                 '%22%3Bi'
                 '%3A1%3Bs%3A32%3A%221c-GQl6aEfgMtD26XH0tGQEvK36DVEqu%22%3B%7D',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/webp,/;q=0.8',
        'Accept-Language': 'uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://nz.ua/',
        'Connection': 'keep-alive',
        'Referer': 'https://nz.ua/',
        'Upgrade-Insecure-Requests': '1',
    }

    async def set_connection(self, login, password, url):

        # getting response from the website

        async with aiohttp.ClientSession() as session:
            csrf = 'Vlz4AyMg_pyO6e9Y3w84GAJNnsHOZHXjnw_hI9Aeo7BnP9VEckzI_cuPiBWrSwouWgWutYk1MJXUPNdnhlvSxQ=='
            data = [
                ('_csrf', csrf),
                ('LoginForm[login]', login),
                ('LoginForm[password]', password),
                ('LoginForm[rememberMe]', '0'),
                ('LoginForm[rememberMe]', '1'),
            ]
            async with session.post(url=self.url,
                                    auth=aiohttp.BasicAuth(login, password),
                                    headers=self.headers,
                                    cookies=self.cookies,
                                    data=data, verify_ssl=False):

                async with session.get(url, verify_ssl=False) as response:
                    if response.status == 200:
                        resp = await response.text()
                        return resp
                    else:
                        error = 'Не вдалось встановити зв\'зок з сайтом.'
                        return error

    async def get_news(self, login, password):

        # parsing news from the website

        content = await self.set_connection(login, password, url='https://nz.ua/dashboard/school-news')
        soup = BeautifulSoup(content, 'html.parser')
        auth_check = soup.find('div', class_='h-user-info clear')  # проверка удалось ли войти в аккаунт
        if auth_check is not None:
            news = soup.find_all('div', class_='ml-message')  # парсинг новостей
            msg_text = [
                f'Логін: ✋🏻<b>{login}</b>🤚🏻\n',
                '📃Ваші останні новини:',
                '➖➖➖➖➖➖➖➖➖➖',
            ]
            for new in news:
                msg_text.append(f'📚{new.text.strip()}')
                msg_text.append('➖➖➖➖➖➖➖➖➖➖')

            return '\n'.join(msg_text)
        else:
            text = 'Перевірте правильність введених даних.\n Напишіть /start, щоб спробувати ще раз.'
            return text

    async def check_new(self, login, password):

        # checking for news on the website
        content = await self.set_connection(login, password, url='https://nz.ua/')
        soup = BeautifulSoup(content, 'html.parser')
        new_counter = soup.find('span', class_='count-messages')

        if new_counter is not None:
            return int(new_counter.text.replace('(', '').replace(')', ''))
        else:
            return new_counter


def main(login, password):
    asyncio.get_event_loop().run_until_complete(ParseNews().get_news(login, password))


if __name__ == '__main__':
    main('login', 'pass')
