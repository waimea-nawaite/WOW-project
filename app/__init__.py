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
# 
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
        return render_template("pages/garment_repairs.jinja", garments=garments)
    
@app.get("/garment_single/")
def show_all_single():
    with connect_db() as client:
        # Get all the things from the DB
        sql_repairs = "SELECT amount, name, id FROM repairs"
        params_repairs = []
        result_repairs = client.execute(sql_repairs, params_repairs)
        repairs = result_repairs.rows

        return render_template("pages/garment_single.jinja", repairs=repairs)
    
# @app.get('/garment_single/<int:garment_id>')
# def show_single_garment(garment_id):
#     with connect_db() as client:
#         # Get the garment info if you want to show it too
#         sql_garment = "SELECT name, id FROM garments WHERE id = %s"
#         garment_result = client.execute(sql_garment, [garment_id])
#         garment = garment_result.rows[0] if garment_result.rows else None
        
#         # Get repairs only for this garment
#         sql_repairs = "SELECT amount, name, id FROM repairs WHERE garment_id = %s"
#         repair_result = client.execute(sql_repairs, [garment_id])
#         repairs = repair_result.rows

#     return render_template(
#         "pages/garment_single.jinja",
#         garment=garment,
#         repair=repairs
#     )



# def show_all_single(id):
#     with connect_db() as client:
#         sql_garments = "SELECT id, name FROM garments WHERE id=?"
#         values_garments = [id]
#         result_garments = client.execute(sql_garments, values_garments)
#         garments = result_garments.rows

#         # And show them on the page
#         garments = result_garments.rows[0]
#         return render_template("pages/garment_single.jinja", garments=garments)
        
#-----------------------------------------------------------
# Route for adding a garment, using data posted from a form
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
    name = request.form.get("name")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO repairs (name) VALUES (?)"
        params = [name]
        client.execute(sql, params)

        # Go back to the page
        flash(f"Repair '{name}' added", "success")
        return redirect("/garment_single")
    
@app.get("/delete_repair/<int:id>")
def delete_a_repair(id):
    with connect_db() as client:
        # Delete the thing from the DB
        sql = "DELETE FROM repairs WHERE id=?"
        params = [id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Repair deleted", "success")
        return redirect("/garment_single")


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