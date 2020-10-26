# Тестовое задание для Уфимского НТЦ

Суть задания описана в [task.md](task.md).

У вас должны быть установлены Python и PostgreSQL. 
При желании можно использовать venv, чтобы не устанавливать psycopg2 в систему.

Для начала зайдём в psql и создадим новую базу данных и подключимся к ней:

```CREATE DATABASE pens;
\connect pens```

Затем создадим таблицы цветов и вкусов:

```CREATE TABLE colors (
  id serial PRIMARY KEY,
  color varchar(50) UNIQUE NOT NULL
);
CREATE TABLE flavors (
  id serial PRIMARY KEY,
  flavor varchar(50) UNIQUE NOT NULL
);```

А теперь можно создать таблицу фломастеров:

```CREATE TABLE pens (
  id serial PRIMARY KEY,
  color varchar(50) REFERENCES colors(color) NOT NULL,
  flavor varchar(50) REFERENCES flavors(flavor) NOT NULL,
  created_at timestamp NOT NULL DEFAULT current_timestamp,
  UNIQUE (color, flavor)
);```

Дальше действовать будет скрипт на Python:

```pip install -r requirements.txt
python main.py```