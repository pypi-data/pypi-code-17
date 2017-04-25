try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError
import pytest
from rev_assets import RevAssets, AssetNotFound


def test_default_url():
    rev = RevAssets(manifest='tests-manifest.json')
    asset = 'styles/home.css'
    expected = '/static/styles/home-2b0339133a.css'
    assert rev.asset_url(asset) == expected


def test_base_url():
    rev = RevAssets(
        base_url='//cdn.amazon.com',
        manifest='tests-manifest.json'
    )
    asset = 'styles/home.css'
    expected = '//cdn.amazon.com/styles/home-2b0339133a.css'
    assert rev.asset_url(asset) == expected


def test_base_url_too_many_slashes():
    rev = RevAssets(
        base_url='//cdn.amazon.com/',
        manifest='tests-manifest.json'
    )
    asset = '/styles/home.css'
    expected = '//cdn.amazon.com/styles/home-2b0339133a.css'
    assert rev.asset_url(asset) == expected


def test_base_url_to_few_slashes():
    rev = RevAssets(
        base_url='',
        manifest='tests-manifest.json'
    )
    asset = 'styles/home.css'
    expected = '/styles/home-2b0339133a.css'
    assert rev.asset_url(asset) == expected


def test_base_url_local():
    rev = RevAssets(
        base_url='/static/',
        manifest='tests-manifest.json'
    )
    asset = 'styles/home.css'
    expected = '/static/styles/home-2b0339133a.css'
    assert rev.asset_url(asset) == expected

    asset = 'scripts/home.js'
    expected = '/static/scripts/home-0ec3e34646.js'
    assert rev.asset_url(asset) == expected


def test_dont_reload():
    rev = RevAssets(manifest='tests-manifest.json', reload=False)
    asset = 'styles/home.css'
    expected = '/static/styles/home-2b0339133a.css'
    assert rev.asset_url(asset) == expected

    new = 'foobar'
    rev._load_manifest = lambda: {asset: new}
    assert rev.asset_url(asset) == expected


def test_reload():
    rev = RevAssets(
        base_url='/static/',
        manifest='tests-manifest.json',
        reload=True
    )
    asset = 'styles/home.css'
    expected = '/static/styles/home-2b0339133a.css'
    assert rev.asset_url(asset) == expected

    new = 'whatever'
    rev._load_manifest = lambda: {asset: new}
    assert rev.asset_url(asset) == '/static/' + new


def test_no_manifest():
    rev = RevAssets()
    with pytest.raises(FileNotFoundError):
        rev.asset_url('styles/home.css')


def test_no_asset_quiet():
    rev = RevAssets(manifest='tests-manifest.json')
    asset = 'no can do'
    rev.asset_url(asset) == ''


def test_no_asset_loud():
    rev = RevAssets(manifest='tests-manifest.json', quiet=False)
    asset = 'no can do'
    with pytest.raises(AssetNotFound):
        rev.asset_url(asset)
