from __future__ import unicode_literals

import os
import io
import logging
import imaplib
import email
import uuid

from email.utils import parsedate_tz, mktime_tz
from datetime import datetime, date, timedelta

from dojo.source import SparkSource


class EmailDropSource(SparkSource):
    '''
    Extract and build meta data about drops from messages in a given email inbox.

    https://tools.ietf.org/html/rfc2822
    '''

    OUTPUT = {
        'fields': [
            {'name': 'id', 'type': 'string'},
            {'name': 'date', 'type': 'timestamp'},
            {'name': 'resent_date', 'type': 'timestamp', 'nullable': True},
            {'name': 'from', 'type': 'string'},
            {'name': 'subject', 'type': 'string'},
            {'name': 'to', 'type': 'string'},
            {'name': 'cc', 'type': 'string', 'nullable': True},
            {'name': 'resent_to', 'type': 'string', 'nullable': True},
            {'name': 'resent_cc', 'type': 'string', 'nullable': True},
            {'name': 'parts', 'type': {
                'type': 'array',
                'elementType': {
                    'fields': [
                        {'name': 'part_filename', 'type': 'string', 'nullable': True},
                        {'name': 'content_type', 'type': 'string'},
                        {'name': 'content_file', 'type': 'string'}
                    ]
                }
            }}
        ]
    }

    def read(self, inputs):
        mail = imaplib.IMAP4_SSL(self.config['imap_host'], self.config['imap_port'])
        mail.login(self.config['email_user'], self.secrets['email_password'])
        mail.select('INBOX', readonly=True)

        days = self.config.get('days', 1) # default to 1 day ago
        start_date = (date.today() - timedelta(days=days)).strftime('%d-%b-%Y')
        result, data = mail.uid('SEARCH', None, 'SENTSINCE %s ALL' % (start_date, ))
        email_uids = data[0].split()
        email_uids = [uid.decode('utf-8') for uid in email_uids]
        result, data = mail.uid('FETCH', ','.join(email_uids), '(RFC822)')
        rows = []
        for datum in data:
            if len(datum) != 2:
                logging.info('imap fetch returned invalid entry: %s' % (datum, ))
                continue
            email_id = datum[0].decode('utf-8')
            try:
                body = datum[1].decode('utf-8')
            except UnicodeDecodeError as e:
                logging.info('failed to decode email body as utf-8, trying latin-1', e)
                body = datum[1].decode('latin-1')
            message = email.message_from_string(body)
            row = self._build_email_row(email_id, message)
            rows.append(row)
        return rows

    def _build_email_row(self, email_id, message):
        return {
            'id': email_id,
            'date': self._parse_rfc2822_datetime(message['Date']),
            'resent_date': self._parse_rfc2822_datetime(message['Resent Date']) if message['Resent Date'] else None,
            'from': message['From'],
            'subject': message['Subject'],
            'to': message['To'],
            'cc': message['CC'],
            'resent_to': message['Resent-To'],
            'resent_cc': message['Resent-CC'],
            'parts': self._build_part_rows(email_id, message)
        }

    def _parse_rfc2822_datetime(self, s):
        return datetime.fromtimestamp(mktime_tz(parsedate_tz(s)))

    def _build_part_rows(self, email_id, message):
        rows = []
        if message.is_multipart():
            for part in message.get_payload():
                rows += self._build_part_rows(email_id, part)
        else:
            rows.append(self._build_part_row(email_id, message))
        return rows

    def _build_part_row(self, email_id, message):
        file_path = self._write_file(email_id, message)
        return {
            'part_filename': message.get_filename(),
            'content_type': message.get_content_type(),
            'content_file': file_path
        }

    def _write_file(self, email_id, message):
        part_filename = message.get_filename()
        file = io.BytesIO(message.get_payload(decode=True))
        unique_filename = str(uuid.uuid4())[:8]
        if part_filename and '.' in part_filename:
            unique_filename += '.%s' % (part_filename.split('.')[-1].lower(), )
        file_path = os.path.join(email_id, unique_filename)
        return self.store.write_file(file_path, file)
