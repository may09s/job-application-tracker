from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():

    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        total=total
    )


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        company = request.form["company"]
        position = request.form["position"]
        date_applied = request.form["date_applied"]
        status = request.form["status"]
        notes = request.form["notes"]

        conn = sqlite3.connect("applications.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO applications
            (company, position, date_applied, status, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (
            company,
            position,
            date_applied,
            status,
            notes
        ))

        conn.commit()
        conn.close()

        return redirect("/applications")

    return render_template("add.html")


@app.route("/applications")
def applications():

    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")
    jobs = cursor.fetchall()

    conn.close()

    return render_template(
        "applications.html",
        jobs=jobs
    )


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    if request.method == "POST":

        company = request.form["company"]
        position = request.form["position"]
        date_applied = request.form["date_applied"]
        status = request.form["status"]
        notes = request.form["notes"]

        cursor.execute("""
            UPDATE applications
            SET company = ?,
                position = ?,
                date_applied = ?,
                status = ?,
                notes = ?
            WHERE id = ?
        """, (
            company,
            position,
            date_applied,
            status,
            notes,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/applications")

    cursor.execute(
        "SELECT * FROM applications WHERE id = ?",
        (id,)
    )

    job = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        job=job
    )


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/applications")


@app.route("/stats")
def stats():

    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Interview'"
    )
    interviews = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Offer'"
    )
    offers = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Rejected'"
    )
    rejections = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "stats.html",
        total=total,
        interviews=interviews,
        offers=offers,
        rejections=rejections
    )


if __name__ == "__main__":
    app.run(debug=True)
