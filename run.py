from scrap_inst import Inst
import config
import sys


def run():
    pars_url = []
    with open('accounts.txt', 'r') as f:  # читаем файл с аккаунтами
        for acc in f.readlines():
            pars_url.append(acc.strip('\n'))  # заполняем список
    url = config.URL
    login = config.LOGIN
    password = config.PASSWORD

    if len(pars_url) == 0:
        sys.exit('Файл accounts.txt пуст.')
    elif login == '':
        sys.exit('Логин пуст.')
    elif password == '':
        sys.exit('Пароль пуст.')

    parser = Inst(url, login, password)  # Инициализируем класс авторизации
    parser.auth_inst()  # Авторизация в инстаграм
    for user_url in pars_url:
        parser.scrap_post(user_url, 3)  # Парсим страницу
    parser.close_browser()  # закрываем браузер


if __name__ == '__main__':
    run()
