from __future__ import absolute_import, division, print_function, unicode_literals


from amaasutils.random_utils import random_string, random_decimal, random_date
import datetime
from decimal import Decimal
import random

from amaascore.assets.asset import Asset
from amaascore.assets.bond import BondGovernment
from amaascore.assets.bond_option import BondOption
from amaascore.assets.foreign_exchange import ForeignExchange
from amaascore.assets.fund import Fund
from amaascore.assets.future import Future
from amaascore.assets.sukuk import Sukuk
from amaascore.assets.synthetic import Synthetic
from amaascore.core.reference import Reference

REFERENCE_TYPES = ['External']


def generate_common(asset_manager_id=None, asset_id=None):

    common = {'asset_manager_id': asset_manager_id or random.randint(1, 1000),
              'asset_id': asset_id or str(random.randint(1, 1000)),
              'currency': random.choice(['SGD', 'USD']),
              'display_name': random_string(10)
              }

    return common


def generate_asset(asset_manager_id=None, asset_id=None, fungible=None):

    common = generate_common(asset_manager_id=asset_manager_id, asset_id=asset_id)
    common['fungible'] = random.choice([True, False]) if fungible is None else fungible

    asset = Asset(**common)
    references = {ref_type: Reference(reference_value=random_string(10)) for ref_type in REFERENCE_TYPES}

    asset.references.update(references)
    return asset


def generate_bond(asset_manager_id=None, asset_id=None):
    props = generate_common(asset_manager_id=asset_manager_id, asset_id=asset_id)
    bond = BondGovernment(par=Decimal('1000'),
                          pay_frequency='M',  # Need to check how we want to represent this
                          coupon=Decimal('0.05'),
                          **props)
    return bond


def generate_bond_option(asset_manager_id=None, asset_id=None, option_type=None, strike=None, option_style=None):
    props = generate_common(asset_manager_id=asset_manager_id, asset_id=asset_id)
    asset = BondOption(underlying_asset_id=random_string(10),
                       option_style=option_style or random.choice(['European', 'American']),
                       option_type=option_type or random.choice(['Put', 'Call']),
                       strike=strike or Decimal(random.uniform(99.0, 102.0)).quantize(Decimal('0.05')),
                       **props)
    return asset


def generate_foreignexchange(asset_id=None):
    asset = ForeignExchange(asset_id=asset_id)
    return asset


def generate_fund(asset_manager_id=None, asset_id=None):
    props = generate_common(asset_manager_id=asset_manager_id, asset_id=asset_id)
    asset = Fund(fund_type=random.choice(['Open', 'Closed']),
                 nav=random_decimal(),
                 expense_ratio=random_decimal(),
                 net_assets=1e06*random.randint(1, 10000),
                 **props)
    return asset


def generate_future(asset_manager_id=None, asset_id=None):
    props = generate_common(asset_manager_id=asset_manager_id, asset_id=asset_id)
    asset = Future(settlement_type=random.choice(['Cash', 'Physical']),
                   contract_size=10000,
                   point_value=Decimal('50'),
                   tick_size=Decimal('0.01'),
                   **props)
    return asset


def generate_sukuk(asset_manager_id=None, asset_id=None):
    props = generate_common(asset_manager_id=asset_manager_id, asset_id=asset_id)
    sukuk = Sukuk(maturity_date=random_date(end_year=2050), **props)
    return sukuk


def generate_synthetic(asset_manager_id=None, asset_id=None):
    props = generate_common(asset_manager_id=asset_manager_id, asset_id=asset_id)
    synthetic = Synthetic(**props)
    return synthetic


def generate_assets(asset_manager_ids=[], number=5):
    assets = []
    for i in range(number):
        asset = generate_asset(asset_manager_id=random.choice(asset_manager_ids))
        assets.append(asset)
    return assets
