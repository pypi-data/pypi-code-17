"""
Tiros Visualization Flask App
"""
import glob
import os
import sys
import random
from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for, session, escape

from tiros.tiros_viz.process_viz import TirosVizProc
from tiros.tiros_viz import utils
from tiros.tiros_viz import render_error
from tiros.tiros_viz import tiros_config
from tiros import server
from tiros import util as cli_util


TIROS_CONFIG = {'host': tiros_config.HOST,
                'ssl': tiros_config.SSL}

app = Flask(__name__)
app.secret_key = os.urandom(24)
viz = TirosVizProc(False)
tiros_session = None


def take_a_snap():
    app.logger.info('Snapping AWS Network.')
    response = server.snapshot(
        host=TIROS_CONFIG['host'],
        raw_snapshots=[],
        paranoid=TIROS_CONFIG['paranoid'],
        signing_session=TIROS_CONFIG['session'],
        snapshot_sessions=TIROS_CONFIG['snapshot_sessions'],
        snapshots=[],
        source='viz',
        ssl=TIROS_CONFIG['ssl'],
        throttle=TIROS_CONFIG['throttle'],
        unsafe_ignore_classic=TIROS_CONFIG['uic']
    )
    return response.status_code, response.text


# Render main view
@app.route('/')
def index():
    return render_template('index.html')


# Route to take a snapshot
@app.route('/mk_snapshot', methods=['POST'])
def mk_snaphot():
    code, snap_data = take_a_snap()
    if code != 200:
        app.logger.error("Return Code: %s", code)
        return render_error.snap_error(code, snap_data)
    snap_name = 'aws_tiros_snap'
    snap_dir, snap_path = utils.save_snap(snap_data, snap_name, app)
    app.logger.info('Snap Dir Name: %s', snap_dir)
    if not snap_dir:
        app.logger.error("Storing Snapped file")
        return render_error.snap_error()
    viz_path = viz.run(snap_path, snap_dir, TIROS_CONFIG)
    if not viz_path:
        return render_error.viz_error()
    rel = os.path.relpath(viz_path)
    relative_viz_path = rel.split('tiros_viz/')[1]
    session['relative_viz_path'] = relative_viz_path
    session['current_view'] = os.path.basename(viz_path)
    session['main_vsi_view'] = os.path.basename(viz_path)
    set_session(snap_path, snap_dir, relative_viz_path)
    return render_template('snapshot_view.html',
                           snapshot_file=relative_viz_path)


# Route to render the uploaded snapshot
@app.route('/snapshot', methods=['POST'])
def snapshot():
    app.logger.info('Render Snapshot View')
    input_file = request.files.get("file")
    file_ok = utils.check_input_file(input_file, app)
    if not file_ok:
        return render_error.error_file()
    snap_dir, snap_path = utils.save_upload_file(input_file, app)
    viz_path = viz.run(snap_path, snap_dir, TIROS_CONFIG)
    if not viz_path:
        return render_error.viz_error()
    rel = os.path.relpath(viz_path)
    relative_viz_path = rel.split('tiros_viz/')[1]
    session['relative_viz_path'] = relative_viz_path
    session['current_view'] = os.path.basename(viz_path)
    session['main_vsi_view'] = os.path.basename(viz_path)
    set_session(snap_path, snap_dir, relative_viz_path)
    return render_template('snapshot_view.html',
                           snapshot_file=relative_viz_path)


# Route that will process Tiros query
@app.route('/query_page', methods=['POST'])
def query_page():
    query = request.form['text']
    app.logger.info('Query: %s', query)
    current_session = get_session()
    # if there is no session data go back to index
    if not current_session['snap_file']:
        return redirect(url_for('index'))
    response = viz.inline_tiros(current_session,
                                TIROS_CONFIG,
                                query)
    session['current_view'] = os.path.basename(response['viz_json_path'])
    legend = utils.mk_legend(response['legend'])
    return render_template('query_view.html',
                           legend=legend,
                           query_answer=response['message'],
                           snapshot_file=response['viz_json_path'])


# Route that will process different snapshot view (e.g. vsi, acl)
@app.route('/snap_view', methods=['POST'])
def snap_view():
    select = request.form.get('selection')
    app.logger.info("Snap view: %s", select)
    current_session = get_session()
    # if there is no session data go back to index
    if not current_session['snap_file']:
        return redirect(url_for('index'))
    current_snap = current_session['rel_path']
    snap_dir = current_session['snap_dir']
    if select == "vsi":
        session['current_view'] = os.path.basename(current_snap)
        return render_template('snapshot_view.html',
                               snapshot_file=current_snap)
    view_path = utils.get_view_path(select, current_snap, snap_dir)
    session['current_view'] = os.path.basename(view_path)
    return render_template('snapshot_view.html',
                           snapshot_file=view_path)


# Route that will process a collapse view
@app.route('/collapse_view', methods=['POST'])
def collapse_view():
    select = request.form.get('selection')
    app.logger.info("Collapse view: %s", select)
    current_session = get_session()
    # if there is no session data go back to index
    if not current_session['snap_file']:
        return redirect(url_for('index'))
    current_snap = current_session['rel_path']
    snap_dir = current_session['snap_dir']
    view_path = utils.get_view_path(select, current_snap, snap_dir)
    session['current_view'] = os.path.basename(view_path)
    return render_template('snapshot_collapse.html',
                            snapshot_file=view_path)

@app.after_request
def add_header(r):
    """
    Add headers to render in different browsers
    also no caching
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def set_session(snap_file, snap_dir, relative_path):
    """
    Set session data
    """
    session['snap_file'] = snap_file
    session['snap_dir'] = snap_dir
    session['current_viz_data'] = relative_path
    return


def get_session():
    return {'snap_file': session.get('snap_file'),
            'current_view': session.get('current_view'),
            'rel_path': session.get('current_viz_data'),
            'snap_dir': session.get('snap_dir'),
            'main_vsi_view': session.get('main_vsi_view')}


def wrap_args(args, snap_sessions, throttle):
    cli_session = cli_util.new_session(profile_name=args.profile,
                                       region_name=args.region)
    if args.region:
        cli_session = cli_util.change_session_region(cli_session, args.region)
    ssl = not args.no_ssl
    host = args.host or (server.DEV_HOST if args.dev else server.PROD_HOST)
    if not snap_sessions:
        snap_sessions = [cli_session]
    return {'profile': args.profile,
            'host': host,
            'ssl': ssl,
            'session': cli_session,
            'paranoid': args.paranoid,
            'snapshot_sessions': snap_sessions,
            'throttle': throttle,
            'uic': args.unsafe_ignore_classic}


def main(args, snap_sessions, throttle):
    global TIROS_CONFIG
    TIROS_CONFIG = wrap_args(args, snap_sessions, throttle)
    app.run(
        host="0.0.0.0",
        port=args.viz_port,
        debug=False
    )
