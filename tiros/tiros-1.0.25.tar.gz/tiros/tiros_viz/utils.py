import os
import errno
from datetime import datetime
from werkzeug import secure_filename
from flask import Markup

allowed_extensions = set({'json'})

# For a given file, return whether it's an allowed type or not
def allowed_file(app, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowed_extensions



# Check if we have cached results
def check_error(cache_result, general_query):
    error = [k['error'] for k in cache_result.values()]
    err = True in error
    cashed_status = '0' if (err or general_query is None) else '1'
    tiros_status = ""
    if (not err or general_query is None):
        tiros_status = Markup("<font color=\"green\">OK<font>")
    else:
        tiros_status = Markup("<font color=\"red\">KO<font>")
    return cashed_status, tiros_status


def mkDir(root, name):
    timed_dir = datetime.now().isoformat()
    dir_name = name.split('.json')[0] + "_" + timed_dir
    dir_name = os.path.join(root, 'static', 'data', dir_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name


def check_input_file(input_file, app):
    return input_file and allowed_file(app, input_file.filename)


def save_snap_file(input_file, app):
    filename = secure_filename(input_file.filename)
    snap_dir = mkDir(app.root_path, filename)
    snap_file = os.path.join(snap_dir, filename)
    input_file.save(snap_file)
    return snap_dir, snap_file


def get_view_path(select, current_snap, snap_dir):
    snap_session = os.path.basename(current_snap).split('.')[0]
    snap_name = select + "_" + snap_session.split('main_')[1] + ".json"
    snap_path = os.path.join(snap_dir, 'viz_data', snap_name)
    rel = os.path.relpath(snap_path)
    return rel.split('tiros_viz/')[1]
