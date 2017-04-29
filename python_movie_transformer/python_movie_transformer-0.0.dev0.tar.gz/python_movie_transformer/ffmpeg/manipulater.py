import logging
from logging import StreamHandler
import ffmpy
from .options import ImageFileOptions

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

class FFmpegManipulater:
    def __init__(self, input_file, output_file):
        self.__input_file = input_file
        self.__output_file = output_file 
    def manipulate(self):

        input_file_name = self.__input_file.file_name
        logger.debug(input_file_name)
        input_options = self.__input_file.options_string
        logger.debug(input_options)
        output_file_name = self.__output_file.file_name
        logger.debug(output_file_name)
        output_options = self.__output_file.options_string
        logger.debug(output_options)

        ff = ffmpy.FFmpeg(
           inputs={input_file_name: input_options},
           outputs={output_file_name: '-strict -2 ' + output_options}
        )


        ff.run()