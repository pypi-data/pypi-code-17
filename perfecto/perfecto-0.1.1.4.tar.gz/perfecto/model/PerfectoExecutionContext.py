class PerfectoExecutionContext:
    def __init__(self, webdriver, context_tags=None, job=None, project=None):
        if webdriver is None:
            raise 'Missing required webdriver argument. Call your builder\'s withWebDriver() method'
        self.webdriver = webdriver
        self.job = job
        self.project = project
        self.context_tags = context_tags

