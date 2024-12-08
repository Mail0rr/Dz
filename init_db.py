import sqlite3


def create_mock_data():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    with open("schema.sql") as f:
        cursor.executescript(f.read())

    pizzas = [
        ("Пепперони", "Протёртые томаты, моцарелла, салями, пикантные пепперони. Аллергены: злаки, лактоза.", 305),
        ("Сырная", "Моцарелла бейби, фета, пармезан, горгонзола, проволоне, моцарелла. Аллергены: глютен, лактоза.", 280),
        ("Маргарита", "Протёртые томаты, моцарелла, базилик. Аллергены: злаки, лактоза.", 190),
        ("Гавайская", "Курица, ананас, моцарелла, томатный соус. Аллергены: злаки, лактоза.", 250),
        ("Вегетарианская", "Цукини, баклажан, томаты черри, перец болгарский, моцарелла, томатный соус. Аллергены: злаки, лактоза.", 220),
    ]

    for pizza in pizzas:
        cursor.execute("INSERT INTO menu_items (name, description, price) VALUES (?, ?, ?)", pizza)

    connection.commit()
    connection.close()