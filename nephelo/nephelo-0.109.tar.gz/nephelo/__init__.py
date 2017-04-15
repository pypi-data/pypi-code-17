import config
import network
import segments as Segments
import template_generator as Templates
import deploy as Deployment
import delete as DeleteStack


def testpypi():
    return "This is packaged correctly"


def configure():
    return config.getconfigfile()


def get(filepath, config, segment, stage):
    print Segments.getSegment(filepath, segment, config, stage)
    return None


def save(config, stage):
    Templates.saveTemplates(config, stage)
    return None


def deploy(config, stage):
    save(config, stage)
    Deployment.deploy(config, stage)
    return ""


def deleteStack(config, stage):
    DeleteStack.deleteStack(config, stage)
    return None

