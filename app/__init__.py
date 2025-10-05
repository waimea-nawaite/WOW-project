#===========================================================
# WOW garment lister
# Ned Waite
#-----------------------------------------------------------
# A list of garments and if they need repairing can tick if 
# complete and you can add/remove garments to change it how
# you please 
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
        sql = """
            SELECT 
                priority, 
                name, 
                date, 
                id,
                (SELECT COUNT(id) FROM repairs WHERE garment_id=garments.id and complete=0) AS repair_count
            FROM garments 
            ORDER BY priority DESC
        """
        params = []
        result = client.execute(sql, params)
        garments = result.rows

        # And show them on the page
        return render_template("pages/garment_list.jinja", garments=garments)

#-----------------------------------------------------------
# Single page route shows the garment name, what repairs it
# has and the list of repairs for that garment
#-----------------------------------------------------------
@app.get("/garment/<int:id>")
def show_all_single(id):
    with connect_db() as client:
        # Get all the garment details from the DB
        sql = "SELECT name, date, priority, id FROM garments WHERE id=?"
        params = [id]
        result = client.execute(sql, params)
        garment = result.rows[0]

        # Get all the repairs from the DB
        sql = "SELECT complete, name, id FROM repairs WHERE garment_id=?"
        params = [id]
        result = client.execute(sql, params)
        repairs = result.rows

        return render_template("pages/garment.jinja", garment=garment, repairs=repairs)
    
# @app.get('/garment_single/<int:garment_id>')
# def show_single_garment(garment_id):
#     with connect_db() as client:
#         # Get the garment info if you want to show it too
#         sql_garment = "SELECT name, id FROM garments WHERE id = ?"
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
        # Add the garment to the DB
        sql = "INSERT INTO garments (name, priority) VALUES (?, ?)"
        params = [name, priority]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Garment '{name}' added", "success")
        return redirect("/")

#-----------------------------------------------------------
# Route for deleting a garment, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_a_garment(id):
    with connect_db() as client:
        # Delete the garment from the DB
        sql = "DELETE FROM garments WHERE id=?"
        params = [id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Garment deleted", "success")
        return redirect("/")
    
# # #-----------------------------------------------------------
# # # A complete garment
# # #-----------------------------------------------------------
# @app.get("/complete/<int:id>")
# def complete_garment(id):
#     with connect_db() as client:
#         sql = "UPDATE garments SET complete=1 WHERE id=?"
#         values = [id]
#         client.execute(sql, values)
#     return redirect("/")
    
# # #-----------------------------------------------------------
# # # A incomplete garment
# # #-----------------------------------------------------------
# @app.get("/incomplete/<int:id>")
# def incomplete_garment(id):
#     with connect_db() as client:
#         sql = "UPDATE garments SET complete=0 WHERE id=?"
#         values = [id]
#         client.execute(sql, values)
#     return redirect("/")

# #-----------------------------------------------------------
# # A complete repair
# #-----------------------------------------------------------
@app.get("/complete_repair/<int:id>")
def complete_repair(id):
    with connect_db() as client:
        sql = "UPDATE repairs SET complete=1 WHERE id=?"
        values = [id]
        client.execute(sql, values)
    return redirect("/")
    
# #-----------------------------------------------------------
# # A incomplete repair
# #-----------------------------------------------------------
@app.get("/incomplete_repair/<int:id>")
def incomplete_repair(id):
    with connect_db() as client:
        sql = "UPDATE repairs SET complete=0 WHERE id=?"
        values = [id]
        client.execute(sql, values)
    return redirect("/")
