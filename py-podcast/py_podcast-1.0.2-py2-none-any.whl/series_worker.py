import threading
import csv
from models.series import Series
from series_crawler import SeriesCrawler
import time
import log
import os

class SeriesWorker(threading.Thread):

  def __init__(self, directory, genre_urls, i):
    """
    Constructor
    """
    super(SeriesWorker, self).__init__()
    self.directory  = directory
    self.genre_urls = genre_urls
    self.i          = i
    self.crawler    = SeriesCrawler()
    self.logger     = log.logger
    # Make this ...
    if not os.path.exists('./{}'.format(self.directory)):
      os.makedirs('./{}'.format(self.directory))

  def run(self):
    """
    Requests, parses series, writes to appropriate CSV
    """
    while self.i < len(self.genre_urls):
      # Grab fields
      url  = self.genre_urls[self.i]
      namestamp = "{}.csv".format(str(int(round(time.time() * 1000000))))

      # GET request
      self.logger.info("Attempting to request {}".format(url))
      self.crawler.set_url(url)
      series = self.crawler.get_series()
      self.logger.info("Attempting to write {}".format(url))

      # Grab writer -> writes series
      writer = csv.writer(open('./{}/{}'.format(self.directory, namestamp), 'wb'))
      writer.writerow(Series.fields)
      for s in series:
        writer.writerow(s.to_line())

      # Move onto the next one
      self.i += 10
      self.logger.info("Wrote {}".format(namestamp))
