import os
import flask
import rq_dashboard

app = flask.Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)

app.config.update(
    REDIS_HOST=os.getenv('REDIS_HOST', '127.0.0.1'),
    REDIS_PORT=int(os.getenv('REDIS_PORT', '6379')),
    REDIS_PASSWORD=None,
    REDIS_DB=int(os.getenv('REDIS_DB', '0')),
    DEBUG=False
)

app.register_blueprint(rq_dashboard.blueprint, url_prefix='/rq')


@app.route('/')
def base():
    return flask.redirect('/rq')
