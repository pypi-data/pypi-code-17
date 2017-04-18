import logging

from slacker_log_handler import SlackerLogHandler

# Create slack handler
slack_handler = SlackerLogHandler('my-channel-token', 'my-channel-name')

# Create logger
logger = logging.getLogger('debug_application')
logger.addHandler(slack_handler)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add the handler to logger
slack_handler.setFormatter(formatter)
slack_handler.setLevel(logging.DEBUG)


# Test logging
logger.error("Debug message from slack!")
