import psycopg2

from contextlib import closing
from datetime import datetime
import random

DB_NAME = "pens"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"

COLORS = ["красный", "оранжевый", "жёлтый", "зелёный", "голубой", "синий", "фиолетовый"]
FLAVORS = ["клубника", "апельсин", "банан", "яблоко", "лайм", "черника", "виноград"]

MENU = """
Введите число фломастеров, которые нужно сгенерировать случайным образом (макс. 20).
Введите 0, чтобы заполнить заполнить базовые цвета и вкусы (работает только один раз).
Введите "new", чтобы получить самый свежий фломатер.
Введите пустую строку для выхода.\n"""

def create_cursor():
    """Create cursor for future database interaction"""
    conn = psycopg2.connect(
        dbname=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD, 
        host=DB_HOST,
    )
    return conn.cursor()

def add_colors_and_flavors(cursor):
    """Create basic colors and flavors"""
    cursor.executemany(
        "INSERT INTO colors(color) VALUES(%s)", [(i,) for i in COLORS]
    )
    cursor.executemany(
        "INSERT INTO flavors(flavor) VALUES(%s)", [(i,) for i in FLAVORS]
    )

def get_colors(cursor):
    """Fetch a list of all colors existing in the database"""
    cursor.execute("SELECT color FROM colors")
    return [i[0] for i in cursor.fetchall()]

def get_flavors(cursor):
    """Fetch a list of all flavors existing in the database"""
    cursor.execute("SELECT flavor FROM flavors")
    return [i[0] for i in cursor.fetchall()]

def create_or_update_random_pen(cursor, colors, flavors):
    """Create a pen with random color and flavor"""
    color = random.choice(colors)
    flavor = random.choice(flavors)
    try:
        cursor.execute(
            "INSERT INTO pens(color, flavor) VALUES(%s, %s)",
            (color, flavor)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        cursor.execute(
            "UPDATE pens "
            "SET created_at = current_timestamp "
            "WHERE color = %s AND flavor = %s",
            (color, flavor)
        )
        conn.commit()

def get_freshest_pen(cursor):
    """Fetch the pen with most recent timestamp"""
    cursor.execute(
        "SELECT color, flavor, created_at "
        "FROM pens ORDER BY created_at DESC LIMIT 1"
    )
    result = list(cursor.fetchone())
    result[2] = datetime.strftime(result[2], "%Y-%m-%d %H:%M:%S.%f")
    return " ".join(result)

def int_convertable(string):
    """Return True if string is convertable into int"""
    try: 
        int(string)
        return True
    except (ValueError, TypeError):
        return False

if __name__ == "__main__":
    print("====================\nФломастерМастер 9000\n====================\n")
    with closing(psycopg2.connect(
        dbname="pens", 
        user="postgres", 
        password="postgres", 
        host="localhost"
    )) as conn:
        while True:
            command = input(MENU)
            # The newest pen
            if command.lower() == "new":
                with conn.cursor() as cursor:
                    freshest = get_freshest_pen(cursor)
                    print(f"Самый свежий фломастер:\n{freshest}")
            # Exit
            elif not int_convertable(command) or "-" in command:
                break
            # Populate colors and flavors
            elif int(command) == 0:
                with conn.cursor() as cursor:
                    try:
                        add_colors_and_flavors(cursor)
                        conn.commit()
                    except psycopg2.errors.UniqueViolation:
                        conn.rollback()
                        print("Базовые цвета и вкусы уже существуют!")
            # Create N pens
            elif int(command) > 0 and int(command) <= 20:
                with conn.cursor() as cursor:
                    colors = get_colors(cursor)
                    flavors = get_flavors(cursor)
                    for _ in range(int(command)):
                        create_or_update_random_pen(cursor, colors, flavors)
                print("Готово!")
            elif int(command) > 20:
                print("Не более 20 фломастеров за раз!")