###############################################################################
#
#   Copyright: (c) 2015 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from . import scheduling_fns

import tornado.httpserver
import tornado.ioloop
import tornado.web

import argh
import logging
import os

# --- configure logging
LOG_FMT = "%(asctime)-15s %(levelname)-8s %(name)-38s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FMT)


# -----------------------------------------------------------------------------
def run(port=9100, sqlite_path=None):

    sqlite_base = os.getenv("HOME", "./")
    sqlite_path = sqlite_path or os.path.join(sqlite_base, ".jobs.sqlite")
    sqlite_url = "sqlite:///{0:s}".format(sqlite_path)

    jobs_stores = {
        "default": SQLAlchemyJobStore(url=sqlite_url),
    }

    jobs_executors = {
        "default": ProcessPoolExecutor(2)
    }

    handlers = [
        (r"/jobs$", scheduling_fns.JobsHandler),
        (r"/jobs/(\w+$)", scheduling_fns.JobsHandler),
    ]

    app = scheduling_fns.SchedulingServer(
        jobs_stores,
        jobs_executors,
        handlers,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


# -----------------------------------------------------------------------------
def main():
    argh.dispatch_command(run)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    run()
