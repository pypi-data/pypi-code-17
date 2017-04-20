import pytest
import os

from git import Repo
from elasticgit import EG

from elasticgit.tests.base import ModelBaseTest

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.content_import.tests.base import ElasticGitTestMixin
from molo.core.content_import import api
from molo.core.models import Page as WagtailPage, SectionPage

from unicore.content.models import (
    Category, Page, Localisation as EGLocalisation)

slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)


PageMapping = {
    'properties': {
        'id': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'uuid': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'primary_category': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'source': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'language': {
            'index': 'not_analyzed',
            'type': 'string'
        },
        'slug': {
            'type': 'string',
            'index': 'not_analyzed',
        }
    }
}

CategoryMapping = {
    'properties': {
        'id': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'uuid': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'source': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'language': {
            'index': 'not_analyzed',
            'type': 'string'
        },
        'slug': {
            'type': 'string',
            'index': 'not_analyzed',
        }
    }
}

LocalisationMapping = {
    'properties': {
        'locale': {
            'type': 'string',
            'index': 'not_analyzed',
        }
    }
}


def clone_repo(url, name):
    repo_path = os.path.join('tmp_test_repos/', name)
    if os.path.exists(repo_path):
        return Repo(repo_path)
    return Repo.clone_from(url, repo_path)


def setup_workspace(repo_path, index_prefix, es={}):
    es_default = {'urls': ['http://localhost:9200']}
    es_default.update(es)
    workspace = EG.workspace(
        repo_path, index_prefix=index_prefix, es=es_default)

    branch = workspace.sm.repo.active_branch
    if workspace.im.index_exists(branch.name):
        workspace.im.destroy_index(branch.name)

    workspace.setup('ubuntu', 'dev@praekeltfoundation.org')

    while not workspace.index_ready():
        pass

    workspace.setup_custom_mapping(Category, CategoryMapping)
    workspace.setup_custom_mapping(Page, PageMapping)
    workspace.setup_custom_mapping(EGLocalisation, LocalisationMapping)

    return workspace


@pytest.mark.django_db
class ContentImportAPITestCase(
        ModelBaseTest, MoloTestCaseMixin, ElasticGitTestMixin):

    def setUp(self):
        self.mk_main()

    @slow
    def test_import_using_iogt_00(self):
        ffl = clone_repo(
            'git@github.com:universalcore/'
            'unicore-cms-content-ffl-i1-prod.git', 'ffl-i1')
        hiv = clone_repo(
            'git@github.com:universalcore/'
            'unicore-cms-content-hiv-i1-prod.git', 'hiv-i1')
        barefootlaw = clone_repo(
            'git@github.com:universalcore/'
            'unicore-cms-content-barefootlaw-i1-prod.git', 'barefootlaw-i1')
        connectsmart = clone_repo(
            'git@github.com:universalcore/'
            'unicore-cms-content-connectsmart-i1-prod.git', 'connectsmart-i1')
        ebola = clone_repo(
            'git@github.com:universalcore/'
            'unicore-cms-content-ebola-i1-prod.git', 'ebola-i1')
        ecd = clone_repo(
            'git@github.com:universalcore/'
            'unicore-cms-content-ecd-i1-prod.git', 'ecd-i1')

        ffl_ws = setup_workspace(
            ffl.working_dir, 'import-test-repo-prefix-%s' % 'ffl-i1')
        hiv_ws = setup_workspace(
            hiv.working_dir, 'import-test-repo-prefix-%s' % 'hiv-i1')
        barefootlaw_ws = setup_workspace(
            barefootlaw.working_dir,
            'import-test-repo-prefix-%s' % 'barefootlaw-i1')
        connectsmart_ws = setup_workspace(
            connectsmart.working_dir,
            'import-test-repo-prefix-%s' % 'connectsmart-i1')
        ebola_ws = setup_workspace(
            ebola.working_dir, 'import-test-repo-prefix-%s' % 'ebola-i1')
        ecd_ws = setup_workspace(
            ecd.working_dir, 'import-test-repo-prefix-%s' % 'ecd-i1')

        workspaces = [
            ffl_ws, hiv_ws, barefootlaw_ws, connectsmart_ws, ebola_ws, ecd_ws]

        for ws in workspaces:
            ws.sync(EGLocalisation)
            ws.sync(Category)
            ws.sync(Page)
            ws.refresh_index()

        repos = [
            api.Repo(ffl_ws, 'ffl', 'Facts for Life'),
            api.Repo(hiv_ws, 'hiv', 'HIV'),
            api.Repo(barefootlaw_ws, 'barefootlaw', 'Barefoot Law'),
            api.Repo(connectsmart_ws, 'connectsmart', 'Connect Smart'),
            api.Repo(ebola_ws, 'ebola', 'Ebola'),
            api.Repo(ecd_ws, 'ecd', 'ECD')]
        locales = [
            {'locale': 'eng_GB', 'site_language': 'en', 'is_main': True},
            {'locale': 'ara_AE', 'site_language': 'es', 'is_main': False}]

        result = api.validate_content(repos, locales)

        self.assertEquals(WagtailPage.objects.all().count(), 5)

        if not result['errors']:
            api.import_content(repos, locales)

        self.assertFalse(result['errors'])
        self.assertEquals(WagtailPage.objects.all().count(), 175)
        self.assertEquals(
            SectionPage.objects.all().child_of(self.section_index).count(), 9)
