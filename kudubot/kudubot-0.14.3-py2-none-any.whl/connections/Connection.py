u"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

from __future__ import absolute_import
import logging
import os
import sqlite3
from threading import Thread
from typing import List, Dict

from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from kudubot.entities.Message import Message
from kudubot.exceptions import InvalidConfigException
from kudubot.users.AddressBook import AddressBook
from kudubot.users.Contact import Contact


class Connection(object):
    u"""
    Abstract class that provides a unified model for a chat service connection
    It keeps track of various state variables and provides APIs to send messages
    and start a listener that reacts on incoming messages using the implemented
    service modules
    """

    logger = logging.getLogger(u"kudubot.connections.Connection")
    u"""
    The Logger for this class
    """

    def __init__(self, services, config_handler):
        u"""
        Initializes the connection object using the specified services
        Starts the database connection

        :param services: The services to use with the connection
        :param config_handler: The GlobalConfigHandler to determine config file locations
        """
        self.identifier = self.define_identifier()
        self.config_handler = config_handler

        self.database_file_location = config_handler.data_location
        self.config_file_location = config_handler.specific_connection_config_location
        self.external_services_directory = os.path.join(config_handler.external_services_directory, self.identifier)

        if not os.path.isdir(self.external_services_directory):
            os.makedirs(self.external_services_directory)

        self.database_file_location = os.path.join(self.database_file_location, self.identifier + u".db")
        self.config_file_location = os.path.join(self.config_file_location, self.identifier + u".conf")

        try:

            self.db = self.get_database_connection_copy()

            self.address_book = AddressBook(self.db)
            self.config = self.load_config()
            self.user_contact = self.define_user_contact()

            self.services = []
            for service in services:
                self.services.append(service(self))

        except InvalidConfigException, e:
            self.generate_configuration()
            raise e

    @staticmethod
    def define_identifier():
        u"""
        Defines the connection's identifier

        :return: The identifier for the Connection type
        """
        raise NotImplementedError()

    def apply_services(self, message, break_on_match = True):
        u"""
        Applies the services to a Message
        First, the method checks if a service is applicable to a message.
        Then, if it is applicable, the service will process the message
        If the break_on_match parameter is set to True, the first match will
        always end the loop.

        :param message: The message to process
        :param break_on_match: Can be set to False to allow more than one result
        :return: None
        """

        self.logger.info(u"Received message " + message.message_body + u".")
        self.logger.info(u"Checking for contact information")

        message.sender = self.address_book.add_or_update_contact(message.sender)
        if message.sender_group is not None:
            message.sender_group = self.address_book.add_or_update_contact(message.sender_group)

        self.logger.debug(u"Applying services to " + repr(message.message_body) + u".")

        for service in self.services:
            if service.is_applicable_to(message):
                service.handle_message(message)
                if break_on_match:
                    break

    def load_config(self):
        u"""
        Loads the configuration for the connection. If this fails for some reason, an InvalidConfigException
        is raised

        :return: A dictionary containing the configuration
        """
        raise NotImplementedError()

    def generate_configuration(self):
        u"""
        Generates a new configuration file for this connection.

        :return: None
        """
        raise NotImplementedError()

    def define_user_contact(self):
        u"""
        Creates a Contact object for the connection by which the connection itself is identified

        :return: The connection's user object
        """
        raise NotImplementedError()

    def send_message(self, message):
        u"""
        Sends a Message using the connection

        :param message: The message to send
        :return: None
        """
        raise NotImplementedError()

    def send_audio_message(self, receiver, audio_file, caption = u""):
        u"""
        Sends an audio message using the connection

        :param receiver: The receiver of the message
        :param audio_file: The path to the audio file to send
        :param caption: The caption sent together with the message
        :return: None
        """
        raise NotImplementedError()

    def send_video_message(self, receiver, video_file, caption = u""):
        u"""
        Sends a video message using the connection

        :param receiver: The recipient of the video message
        :param video_file: The path to the video file to be sent
        :param caption: The caption to be displayed with the video
        :return: None
        """
        raise NotImplementedError()

    def send_image_message(self, receiver, image_file, caption = u""):
        u"""
        Sends an image message using the connection

        :param receiver: The recipient of the image message
        :param image_file: The path to the image file
        :param caption: The caption to be displayed with the image
        :return: None
        """
        raise NotImplementedError()

    def listen(self):
        u"""
        Starts listening on the connection in an infinite loop. If the execution of the
        program has to continue past starting the listener, the listen_in_separate_thread() method
        should be called instead

        :return: None
        """
        raise NotImplementedError()

    def listen_in_separate_thread(self):
        u"""
        Runs the listen() method in a separate daemon thread

        :return: The listening thread
        """

        self.logger.info(u"Starting daemon thread for connection " + self.identifier + u".")

        thread = Thread(target=self.listen)
        thread.daemon = True
        thread.start()
        return thread

    def get_database_connection_copy(self):
        u"""
        Creates a new sqlite Connection to the kudubot Connection's database file

        :return: The generated sqlite Connection
        """
        return sqlite3.connect(self.database_file_location)
