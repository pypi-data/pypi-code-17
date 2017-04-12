# Project: RET-RNN （用于雷达回波外推的RNN类神经网络）
# Module: 日志记录模块
#
# Author: Lex.Teng
# E-mail: lexteng@163.com
# ==============================================================================
import LexTengLib.xfile as xf


class Logger(object):
    """
    日志记录器，日志同步记录到记录器内的所有文件

    :since: 0.5.0
    """
    paths = []
    f = []

    def add_file(self, path):
        """
        向日志记录器中添加一个文件

        :param path: 文件路径
        :since: 0.5.0
        """
        xf.mkdirs(path)
        self.paths.append(path)
        self.f.append(open(path, 'a'))

    def rm_file(self, path):
        """
        从日志记录器中移除一个文件

        :param path: 文件路径
        :since: 0.5.0
        """
        index = self.paths.index(path)
        self.paths.pop(index)
        self.f.pop(index)

    def new_line(self):
        """
        向日志文件中追加一行空行

        :since: 0.5.0
        """
        for f in self.f:
            f.write('\n')

    def log(self, info, write_line=True):
        """
        向日志文件中追加一行内容

        :param info: 日志内容
        :param write_line: 追加完成后是否换行
        :since: 0.5.0
        """
        for f in self.f:
            f.write(info)
        if write_line:
            self.new_line()

    def log_multi(self, info_list):
        """
        向日志文件中追加多行内容

        :param info_list: 日志内容列表（每个元素为一行内容）
        :since: 0.5.0
        """
        for info in info_list:
            self.log(info, True)
