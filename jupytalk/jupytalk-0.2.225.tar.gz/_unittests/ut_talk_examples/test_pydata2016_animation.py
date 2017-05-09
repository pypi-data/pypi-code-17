"""
@brief      test log(time=20s)
"""

import sys
import os
import unittest
import warnings


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_

from pyquickhelper.loghelper import fLOG, run_cmd
from pyquickhelper.pycode import get_temp_folder, fix_tkinter_issues_virtualenv, is_travis_or_appveyor
from pyquickhelper.pycode import add_missing_development_version


class TestPyData2016Animation(unittest.TestCase):

    def test_matplotlib_example(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor() == "travis":
            warnings.warn("issue with datashader.bokeh_ext, skipping")
            return

        if is_travis_or_appveyor() == "appveyor":
            warnings.warn("no ffmpeg installed")
            return

        fLOG("test ffmpeg")
        out, err = run_cmd("ffmpeg", wait=True, fLOG=fLOG)
        fLOG("end ffmpeg")
        if "ffmpeg version" not in out or err is None or len(err) == 0:
            if sys.platform.startswith("win"):
                fLOG("download ffmpeg")
                add_missing_development_version(
                    ["pyensae"], __file__, hide=True)
                from pyensae.datasource import download_data
                download_data("ffmpeg.zip", website="xd")
            else:
                raise FileNotFoundError(
                    "Unable to find ffmpeg. PATH={0}".format(os.environ["PATH"]))

        fLOG("test")
        temp = get_temp_folder(__file__, "temp_example_example")
        fix_tkinter_issues_virtualenv()

        # update a distribution based on new data.
        import numpy as np
        import matplotlib.pyplot as plt
        import scipy.stats as ss
        from matplotlib.animation import FuncAnimation, writers

        class UpdateDist(object):

            def __init__(self, ax, prob=0.5):
                self.success = 0
                self.prob = prob
                self.line, = ax.plot([], [], 'k-')
                self.x = np.linspace(0, 1, 200)
                self.ax = ax

                # Set up plot parameters
                self.ax.set_xlim(0, 1)
                self.ax.set_ylim(0, 15)
                self.ax.grid(True)

                # This vertical line represents the theoretical value, to
                # which the plotted distribution should converge.
                self.ax.axvline(prob, linestyle='--', color='black')

            def init(self):
                self.success = 0
                self.line.set_data([], [])
                return self.line,

            def __call__(self, i):
                # This way the plot can continuously run and we just keep
                # watching new realizations of the process
                if i == 0:
                    return self.init()

                # Choose success based on exceed a threshold with a uniform
                # pick
                if np.random.rand(1,) < self.prob:
                    self.success += 1
                y = ss.beta.pdf(self.x, self.success + 1,
                                (i - self.success) + 1)
                self.line.set_data(self.x, y)
                return self.line,

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ud = UpdateDist(ax, prob=0.7)
        anim = FuncAnimation(fig, ud, frames=np.arange(100), init_func=ud.init,
                             interval=100, blit=True)

        Writer = writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        anim.save(os.path.join(temp, 'lines2.mp4'), writer=writer)

        plt.close('all')
        fLOG("end")


if __name__ == "__main__":
    unittest.main()
