"""Packets supported by the parser."""
from .eddystone import EddystoneUIDFrame, EddystoneURLFrame, EddystoneEncryptedTLMFrame, \
                       EddystoneTLMFrame
from .ibeacon import IBeaconAdvertisement
