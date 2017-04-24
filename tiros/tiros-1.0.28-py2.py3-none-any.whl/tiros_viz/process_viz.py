import os
import glob
import pprint
import json

from flask import  Markup

from tiros.tiros_viz.snapshot_data import SData
from tiros.tiros_viz import tiros_config
from tiros import server as tiros_server
from tiros import util as tiros_util


class TirosVizProc(object):
    """
    Tiros Snapshot Viz Processor
    """

    def __init__(self, debug):
        self.snap_file = None
        self.snapshot_name = None
        self.snapshot_viz_out = dict()
        self.snapshot_dir = None
        self.main_snap_path = None
        self.debug = debug
        self.session = None
        self.config = None
        self.sData = SData(debug)
        return

    def mk_snap_dir(self, snap_dir):
        """
        For a given snapshot create a directory to store viz_data
        """
        self.snapshot_dir = os.path.join(snap_dir, 'viz_data')
        if not os.path.exists(self.snapshot_dir):
            os.makedirs(self.snapshot_dir)
        return

    def run(self, snap_file, snap_dir, do_cache, config):
        """
        Main run.
        snap_file : Tiros snapshot file
        snap_dir : dir where output will be stored
        do_cache : perform general query
        session: tiros session
        host: tiros host
        """
        try:
            print('Processing: {}'.format(snap_file))
            self.config = config
            self.snap_file = snap_file
            self.snapshot_name = os.path.basename(snap_file).split('.')[0]
            self.mk_snap_dir(snap_dir)
            vsi_data, vsi_collapse, acls_data = self.sData.process_snapshot(snap_file)
            vsi_path = self.mk_path(vsi_data, 'main')
            self.main_snap_path = vsi_path
            vsi_collapse_path = self.mk_path(vsi_collapse, 'vsi_collapse')
            aclView_file_path = self.mk_path(acls_data, 'acl')
            cached_result = dict()
            if do_cache:
                cached_result = self.cache_query(vsi_data)
            return vsi_path, cached_result
        except Exception as e:
            print("Error: {}".format(e))
            return None, None

    def cache_query(self, vsi_data):
        """
        Pre-compute some queries
        """
        cached_dict = dict()
        for info, cmd in tiros_config.TIROS_QUERIES.items():
            result = self.ask_tiros(info, cmd, vsi_data)
            cached_dict.update({info: result})
        return cached_dict

    def mk_path(self, data, name):
        """
        Create a file for data viz
        """
        viz_filename = "_".join([name, self.snapshot_name, ".json"])
        viz_filepath = os.path.join(self.snapshot_dir, viz_filename)
        try:
            os.remove(viz_filepath)
        except Exception as e:
            pass
        with open(viz_filepath, 'w') as fp:
            json.dump(data, fp)
        print('{} View : {}'.format(name, viz_filepath))
        return viz_filepath

    def tiros_proc(self, config, snap_file, query):
        """
        Tiros Service Proc
        """
        snap_contents = [json.loads(tiros_util.file_contents(snap_file))]
        response = tiros_server.query(config['session'],
                                      query,
                                      backend=tiros_config.BACKEND,
                                      host=config['host'],
                                      raw_snapshots=None,
                                      snapshot_sessions=None,
                                      snapshots=snap_contents,
                                      source='viz',
                                      ssl=config['ssl'],
                                      throttle=tiros_config.THROTTLE,
                                      transforms=tiros_config.TRANSFORMS,
                                      unsafe_ignore_classic=tiros_config.UIC,
                                      user_relations=tiros_config.UR)
        print('Status code: %d' % response.status_code)
        return response

    def ask_tiros(self, query_name, query, vsi_data):
        """
        Ask Tiros for general queries defined in tiros_config.TIROS_QUERIES
        """
        viz_filepath = self.main_snap_path
        message = ""
        error = False
        color = 'instance_ssh'
        print('Caching query: %s' % query_name)
        try:
            response = self.tiros_proc(self.config, self.snap_file, query)
            query_dict = json.loads(response.text)
            body = query_dict[0]['body']
            try:
                solutions = body['substitutions']
                sol = [list(s.values())[0] for s in solutions]
                viz_data = self.sData.update_color(color, sol, vsi_data)
                viz_filepath = self.mk_path(viz_data, query_name)
                message = ("N. solutions: {}".format(body['num-solutions']))
            except Exception as e:
                error = True
                message = ("Result: {}".format(body))
        except Exception as e:
            error = True
            message = "Tiros Service Error"
        return {'file_path': viz_filepath,
                'message': message,
                'error': error}

    def inline_tiros(self, session, config, query):
        """
        Function to make Tiros query inline
        """
        snap_file = session['snap_file']
        c_view = session['main_vsi_view']
        if not c_view:
            c_view = session['current_view']
        c_path = session['rel_path']
        snap_dir = session['snap_dir']
        if query == "":
            return {'viz_json_path': c_path,
                    'query': query,
                    'message': "Error: Invalid query"}
        viz_filepath = c_path
        message = ""
        try:
            response = self.tiros_proc(config, snap_file, query)
            viz_path = os.path.join(snap_dir, 'viz_data', c_view)
            viz_data = json.loads(tiros_util.file_contents(viz_path))
            query_dict = json.loads(response.text)
            is_error =  type(query_dict) is dict
            if is_error:
                error_dict = query_dict.get('error')
                err_msg = error_dict.get('message', 'Tiros Service Error')
                err_msg = "<font color=\"red\">%s</font>" % err_msg
                message = Markup(err_msg)
            else:
                body = query_dict[0]['body']
                try:
                    solutions = body['substitutions']
                    sol = [list(s.values())[0] for s in solutions]
                    viz_data = self.sData.update_color('high', sol, viz_data)
                    viz_filepath = self.sData.mk_path_inline(snap_dir, viz_data)
                    message = ("N. solutions: {}".format(body['num-solutions']))
                except Exception as e:
                    message = ("Result: {}".format(body))
        except Exception as e:
            message = Markup("<font color=\"red\">Tiros Service Error</font>")
        return {'viz_json_path': viz_filepath,
                'query': query,
                'message': message}
