from setuptools import setup
from Cython.Build import cythonize

setup(
    name="alpha_quant",
    version="1.5",
    description="Alpha Quant SDK",
    author="http://www.alpha-qt.com",
    url="http://www.alpha-qt.com",
    license="LGPL",
    install_requires=['redis', 'thrift', 'psutil'],
    packages = ['alpha_trade'],
    #package_dir = {'alpha_trade': 'gen-py/alpha_trade'},

    ext_modules = cythonize(['alpha_update_client.py', 'key_value_store.py', 'realtime_data_client.py', 'ctp_realtime_data_client.py', 'ctp_future_minutes_data_client.py', 'stock_sharing_client.py', 'alpha_trade_client.py',
              'stock_financials_client.py', 'live_trade_system_client.py', 'stock_history_client.py', 'stock_list_client.py', 'alpha_utility.py', 'alpha_error_code.py', 'future_info_client.py', 'futures_history_client.py',
              'host_port_client_config.py', 'alpha_dbutility.py', 'futures_history_minutes_data_client.py', 'static_price_adjust.pyx', 'alpha_quant.pyx']),
    )
