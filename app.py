from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_db_connection
from init_db import create_mock_data

app = Flask(__name__)
app.config["SECRET_KEY"] = "qwerty"
create_mock_data()


@app.route("/")
def index():
    connection = get_db_connection()
    menu_items = connection.execute("SELECT * FROM menu_items").fetchall()
    connection.close()
    return render_template("menu.html", menu_items=menu_items)


@app.route("/create/", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]

        if not name or not price:
            flash("Название и цена обязательны", "danger")
            return render_template("create.html")

        connection = get_db_connection()
        connection.execute(
            "INSERT INTO menu_items (name, description, price) VALUES (?, ?, ?)",
            (name, description, price),
        )
        connection.commit()
        connection.close()

        flash("Пицца добавлена!", "success")
        return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/<int:item_id>/edit/", methods=["GET", "POST"])
def edit(item_id):
    connection = get_db_connection()
    item = connection.execute(
        "SELECT * FROM menu_items WHERE id = ?", (item_id,)
    ).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]

        if not name or not price:
            flash("Название и цена обязательны!", "danger")
            return render_template("edit.html", item=item)

        connection.execute(
            "UPDATE menu_items SET name = ?, description = ?, price = ? WHERE id = ?",
            (name, description, price, item_id),
        )
        connection.commit()
        connection.close()

        flash("Пицца обновлена!", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", item=item)


@app.post("/<int:item_id>/delete/")
def delete(item_id):
    connection = get_db_connection()
    connection.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))
    connection.commit()
    connection.close()

    flash("Блюдо успешно удалено!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
