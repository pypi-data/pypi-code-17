
from flask import render_template, Markup

error_alert = "alert alert-danger alert-error"

def snap_error():
    msg = Markup("<strong>Error!</strong> Snapping AWS network config")
    return render_template('index.html',
                           alert=error_alert,
                           snapshot_validation=msg)

def error_file():
    msg = Markup("<strong>Error!</strong> Wrong file format.")
    return render_template('index.html',
                           alert=error_alert,
                           snapshot_validation=msg)

def viz_error():
    msg = Markup("<strong>Error!</strong> Invalid Tiros Snapshot")
    return render_template('index.html',
                           alert=error_alert,
                           snapshot_validation=msg)
