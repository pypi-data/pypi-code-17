import terminado
from sandstone import settings



class SandstoneTermManager(terminado.UniqueTermManager):
    """
    The manager used for setting up web terminal sessions in Sandstone. Each
    new websocket connection establishes a new terminal session, up to a
    maximum of three connected terminals. Each created terminal is configured
    with the environment variables pulled from the WEB_TERMINAL_ENV setting.
    """
    pass
    # def make_term_env(self, height=25, width=80, winheight=0, winwidth=0, **kwargs):
    #     """
    #     Start each terminal session with a fresh environment, and then apply
    #     settings from the WEB_TERMINAL_ENV dict if any exist.
    #     """
    #     env = {}
    #     env["TERM"] = self.term_settings.get("type",DEFAULT_TERM_TYPE)
    #     dimensions = "%dx%d" % (width, height)
    #     if winwidth and winheight:
    #         dimensions += ";%dx%d" % (winwidth, winheight)
    #     env[ENV_PREFIX+"DIMENSIONS"] = dimensions
    #     env["COLUMNS"] = str(width)
    #     env["LINES"] = str(height)

    #     if self.server_url:
    #         env[ENV_PREFIX+"URL"] = self.server_url

    #     if self.extra_env:
    #         _update_removing(env, self.extra_env)
        
    #     if settings.WEB_TERMINAL_ENV:
    #         env.update(settings.WEB_TERMINAL_ENV)

    #     return env