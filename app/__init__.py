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
        sql = "SELECT priority, name, id FROM garments ORDER BY priority DESC"
        params = []
        result = client.execute(sql, params)
        garments = result.rows

        # And show them on the page
        return render_template("pages/garments.jinja", garments=garments)


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")

#-----------------------------------------------------------
# Thing page route - Show details of a single thing
#-----------------------------------------------------------
@app.get("/garment/<int:id>")
def show_one_garment(id):
    with connect_db() as client:
        # Get the thing details from the DB
        sql = "SELECT priority, name, id FROM garments WHERE id=?"
        params = [id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            garment = result.rows[0]
            return render_template("pages/garment.jinja", garment=garment)

        else:
            # No, so show error
            return not_found_error()


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


