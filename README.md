# LearningHub

Сайт для онлайн-обучения.

---

## 1. Клонируйте репозиторий

```sh
git clone https://github.com/aml-709/LearnHub.git
cd LearningHub

```markdown
# LearningHub

Django-платформа для онлайн-обучения.

---

### 2. Установите зависимости

Рекомендуется использовать виртуальное окружение:

```sh
python -m venv venv 

venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Примените миграции

```sh
cd Learn
python manage.py migrate
```

### 4. Создайте суперпользователя (админа)

```sh
python manage.py createsuperuser
```

### 5. Запустите сервер

```sh
python manage.py runserver
```

Откройте [http://127.0.0.1:8000/](http://127.0.0.1:8000/) в браузере.

---

## Тесты

```sh
python manage.py test
```

---


## Структура проекта

```
LearningHub/
├── Learn/           # Django-проект
│   ├── manage.py
│   ├── school/      # Основное приложение
│   └── ...
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── tests.yml
```
