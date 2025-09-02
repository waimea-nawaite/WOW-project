#===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
#-----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


#-----------------------------------------------------------
# Home page route shows garments
#-----------------------------------------------------------
@app.get("/")
def show_all_garments():
    with connect_db() as client:
        # Get all the things from the DB
        sql = "SELECT priority, name, date, id FROM garments ORDER BY priority DESC"
        params = []
        result = client.execute(sql, params)
        garments = result.rows

        # And show them on the page
        return render_template("pages/garment_list.jinja", garments=garments)


#-----------------------------------------------------------
# Garment page route - Show details of a single garment
#-----------------------------------------------------------
@app.get("/garment_repairs/")
def show_all_garment_repairs():
    with connect_db() as client:
        # Get all the things from the DB
        sql = "SELECT priority, name, date, id FROM garments ORDER BY priority DESC"
        params = []
        result = client.execute(sql, params)
        garments = result.rows

        # And show them on the page
        return render_template("pages/garment_list.jinja", garments=garments)
        


#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_garment():
    # Get the data from the form
    name  = request.form.get("name")
    priority = request.form.get("priority")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO garments (name, priority) VALUES (?, ?)"
        params = [name, priority]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Garment '{name}' added", "success")
        return redirect("/")
    
@app.post("/add_repair")
def add_a_repair():
    # Get the data from the form
    name  = request.form.get("name")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO repairs (name) VALUES (?)"
        params = [name]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Repair '{name}' added", "success")
        return redirect("garment_single")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_a_garment(id):
    with connect_db() as client:
        # Delete the thing from the DB
        sql = "DELETE FROM garments WHERE id=?"
        params = [id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Garment deleted", "success")
        return redirect("/")
    
# # #-----------------------------------------------------------
# # # A complete task
# # #-----------------------------------------------------------
# @app.get("/complete/<int:id>")
# def complete_task(id):
#     with connect_db() as client:
#         sql = "UPDATE garments SET complete=1 WHERE id=?"
#         values = [id]
#         client.execute(sql, values)
#     return redirect("/")
    
# # #-----------------------------------------------------------
# # # A incomplete task
# # #-----------------------------------------------------------
# @app.get("/incomplete/<int:id>")
# def incomplete_task(id):
#     with connect_db() as client:
#         sql = "UPDATE tasks SET complete=0 WHERE id=?"
#         values = [id]
#         client.execute(sql, values)
#     return redirect("/")


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")