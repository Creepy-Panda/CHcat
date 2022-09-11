# QRKot - Приложение для Благотворительного фонда поддержки котиков

## Стек технологий
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Google CloudAPI](https://img.shields.io/badge/google-CloudAPI-blue?style=for-the-badge&logo=appveyor)

## Описание
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

### Порядок локального запуска
- Клонировать репозиторий и перейти в него в командной строке:


    - `git clone git@github.com:Creepy-Panda/cat_charity_fund.git`
    - `cd cat_charity_fund`


- Cоздать и активировать виртуальное окружение:

`python3 -m venv venv`


    - Если у вас Linux/MacOS

        `source venv/bin/activate`

    - Если у вас Windows

        `source venv/scripts/activate`

- Установить зависимости из файла requirements.txt:


    `python3 -m pip install --upgrade pip`
    `pip install -r requirements.txt`


- Создаем .env файл, примеры находятся в env.example


- Запускаем проект:

    `uvicorn app.main:app`


#### Автор:
*Владислав Носиков*