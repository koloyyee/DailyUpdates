from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)

from dailyUpdates.db import getDB
from dailyUpdates.Models.agencies import AgencyModel

bp = Blueprint("agency", __name__, url_prefix="/agency")

# create


@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Register a news agency with url.
    Validate that the agency is not taken.
    """

    if request.method == "POST":
        agency = request.form["agency"]
        url = request.form["url"]
        db = getDB()
        error = None

        if not agency:
            error = "agency already registered"
        if not url:
            error = "url already registered"
        if error is None:
            try:
                # db.execute(
                #     "INSERT INTO agency (agency, url) VALUES (?, ?)", (agency, url)
                # )
                # db.commit()
                agency = AgencyModel()
                agency.registerAgency(agency, url)

            except db.IntegrityError:
                error = f"News Agency {agency} is already registered"
            else:
                return redirect(url_for("agency.show"))

        flash(error)
    return render_template("agency/register.html")


@bp.route("/")
def show():
    """
    Show all agencies the user has registered with the related url.
    """
    # agencies = db.execute(
    #     "SELECT id, agency, url from agency"
    # ).fetchall()
    agencyModel = AgencyModel()
    agencies = agencyModel.getAllAgencies()
    return render_template("agency/index.html", agencies=agencies)


def agency(id):
    # agency = getDB().execute(
    #     "SELECT id, agency, url FROM agency WHERE id = ?", (id,)
    # ).fetchone()
    agencyModel = AgencyModel
    agency = agencyModel.getAgency(id)

    if agency is None:
        abort(404, f"Agency doesn't exist")
    return agency


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    agencyModel = AgencyModel()
    newAgency = agencyModel.getAgency(id)

    if request.method == "POST":
        agency = request.form["agency"]
        url = request.form["url"]
        error = None

        if not agency:
            error = "Agency name is required"
        if not url:
            error = "URL name is required"
        if error is not None:
            flash(error)
        else:
            agencyModel.updateAgency(agency=agency, url=url, id=id)
            return redirect(url_for("agency.show"))
    return render_template("agency/update.html", agency=newAgency)
