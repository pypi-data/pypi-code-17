from Products.CMFCore.utils import getToolByName


def null_upgrade_step(context):
    pass


def upgrade0912(context):
    context = getToolByName(context, "portal_setup")
    context.runImportStepFromProfile(
        'profile-collective.behavior.sql:default',
        'catalog',
        purge_old=False)
