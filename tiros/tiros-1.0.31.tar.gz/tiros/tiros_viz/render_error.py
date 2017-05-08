
from flask import render_template, Markup
import json
import pprint

error_alert = "alert alert-danger alert-error"

def snap_error(code, m_error):
    try:
        # It reached Tiros Service (tiros error)
        j = json.loads(m_error)
        error = j.get('error')
        m = error.get('message')
        msg = Markup("<strong>Error Code: %d</strong>\n %s" % (code, m))
    except (AttributeError, ValueError):
        # It didn't reach Tiros Service (boto error)
        msg = Markup("<strong>Error Code: %d</strong> %s" % (code, m_error))
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
