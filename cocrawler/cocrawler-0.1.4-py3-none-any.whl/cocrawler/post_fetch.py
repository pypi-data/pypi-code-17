'''
builtin post_fetch event handler

Default actions to move here from existing code:

redirect analysis and following -- cocrawler.cocrawler

special seed handling -- don't count redirs in depth, and add www.seed if naked seed fails -- cocrawler.cocrawler
  do this by elaborating the work unit to have an arbitrary callback

parse links and embeds, using an algorithm chosen in conf -- cocrawler.cocrawler

parent subsequently calls add_url on them -- cocrawler.cocrawler
'''
