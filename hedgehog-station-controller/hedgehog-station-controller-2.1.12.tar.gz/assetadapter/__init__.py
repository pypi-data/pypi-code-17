from assetadapter.devicemanager import DeviceManager
import logging

logging.info('Start device-manager ...')
# dm = DeviceManager(visa_library='../test.yml@sim')
dm = DeviceManager(visa_library='test.yml@sim')
logging.info('Device-manager started.')
