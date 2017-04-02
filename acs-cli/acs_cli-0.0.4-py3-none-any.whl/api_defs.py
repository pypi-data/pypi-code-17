

apis = {
    #'auth': {
    #    'base-path': '/alfresco/api/-default-/public/authentication/versions/1',
    #    'operations': {
    #        'create-ticket': {
    #            'path': '/tickets',
    #            #'post-params': {'userId', 'password'}
    #        }
    #    }
    #},
    'people': {
        'base-path': '/alfresco/api/-default-/public/alfresco/versions/1',
        'operations': {
            'get-person': {
                'path': '/people/{personId}'
            },
            'create-person': {
                'path': '/people',
                'properties': ['userName', 'password', 'email', 'firstName']
            },
            'list-people': {
                'path': '/people'
            },
        }
    },
    'sites': {
        'base-path': '/alfresco/api/-default-/public/alfresco/versions/1',
        'operations': {
            'get-site': {
                'path': '/sites/{siteId}'
            },
            'get-site-membership': {
                'path': '/people/{personId}/sites/{siteId}'
            },
            'list-sites': {
                'path': '/sites'
            },
            'list-site-memberships': {
                'path': '/people/{personId}/sites'
            }
        }
    }
}