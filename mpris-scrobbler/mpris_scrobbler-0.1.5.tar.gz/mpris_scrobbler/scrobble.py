#!/usr/bin/env python
import dbus  # pip install dbus-python
from os import mkdir, path
import re
from getpass import getuser, getpass
from urllib import error
from mpris_scrobbler.services import wiltfm


class Scrobble(object):

    def __init__(self, username=None, password=None, service="wiltfm",
                 device=None):
        self.conf_dir = "/home/{}/.config/mpris-scrobble".format(getuser())

        self.prefix = "org.mpris.MediaPlayer2."

        self.bus = dbus.SessionBus()
        self.bus.request_name("xyz.mashek.mpris.scrobble")

        if device is not None:
            device = self.prefix + device

        if username is None:
            username, password = self.load_config()

        self.config = {
            "username": username,
            "password": password,
            "service": service,
            "device": device
        }

        self.started = self.start()
        self.device = self.register_device()

    def start(self):
        li = self._login()
        if li is not True:
            return li

        dvc = self.get_device()
        if dvc is not True:
            return dvc

        return True

    def save_config(self):
        with open(self.conf_dir + "/config", "w") as f:
            f.write("{}\n{}".format(
                self.config["username"],
                self.config["password"]
            ))

    def load_config(self):
        if not path.isdir(self.conf_dir):
            mkdir(self.conf_dir)
            return

        try:
            with open(self.conf_dir + "/config", "r") as f:
                a = f.readlines()
                return [a[0].strip(), a[1].strip()]
        except FileNotFoundError:
            pass  # No configuration file

    def _login(self):
        if not self.config["username"]:
            self.config["username"] = input("username: ")
        if not self.config["password"]:
            self.config["password"] = getpass("password: ")

        try:
            self.wilt = wiltfm.Wilt(self.config["username"],
                                    self.config["password"])
            self.save_config()
            return True
        except error.HTTPError as e:
            return str(e)

    def get_device(self):
        if not self.config["device"]:
            s = {}
            l = {}
            i = 1
            is_int = False

            print("Availble MPRIS devices:")
            for dev in self.bus.list_names():
                if re.match(self.prefix, dev):
                    spl = dev.rsplit(self.prefix)[1]
                    s[spl] = dev
                    l[i] = spl
                    print("  [{}] {}".format(i, spl))
                    i += 1

            ch = input("Choose a number: ")

            try:
                ch = int(ch)
                is_int = True
            except ValueError:
                pass

            if ch not in s and int(ch) not in l:
                return "Invalid choice"
            if is_int:
                self.config["device"] = s[l[int(ch)]]
                return True

            self.config["device"] = s[ch]

        return True

    def register_device(self):
        try:
            return dbus.SessionBus().get_object(
               self.config["device"], "/org/mpris/MediaPlayer2"
            )
        except dbus.exceptions.DBusException as e:
            return "scrobble.register_device: " + str(e)
        except TypeError:
            self.get_device()

    def push(self):
        if not self.config["device"]:
            return "Do device to push to."

        try:
            metadata = self.device.Get(
                self.prefix + "Player",
                "Metadata",
                dbus_interface="org.freedesktop.DBus.Properties"
            )

        except AttributeError as e:
            if type(self.device) is str:
                return self.device
            return "push.AttributeError: " + str(e)
        except KeyError as e:
            return "push.KeyError: " + str(e)
        except dbus.exceptions.DBusException as e:
            return "push.dbus.exceptions.DBusException: " + str(e)

        try:
            track = metadata["xesam:title"]
            artist = metadata["xesam:artist"][0]

            if track is not None and artist is not None:
                result = self.wilt.scrobble({"song": track, "artist": artist})

                if result:
                    return result
        except KeyError:
            pass  # No track found
