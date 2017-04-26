from assetadapter.core import VisaDeviceManager
from assetadapter.version import __version__
from orchestrator.settings import VISA_BACKEND

visa_device_manager = VisaDeviceManager(visa_library=VISA_BACKEND)
