# Copyright 2015 Rackspace
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cdbclient import base
from cdbclient import exceptions
from cdbclient import utils


class Schedule(base.Resource):
    """
    Schedule used to hold storage information.
    """
    def __repr__(self):
        return '<Schedule: %s>' % self.id


class Schedules(base.Manager):
    """
    Manage :class:`Schedule` resources.
    """
    resource_class = Schedule

    def create_backup(self, instance_id=None, day_of_week=None, hour=None,
                      minute=None, source_type=None, source_id=None,
                      copy_to=None):
        """
        Creates a schedule backup for an instance.
        """
        normal_copy_to = None
        if copy_to:
            normal_copy_to = copy_to.split(',')
        data = {
            'schedule': {
                'action': 'backup',
                'instance_id': instance_id,
                'source_id': source_id,
                'source_type': source_type,
                'copy_to': normal_copy_to,
            }
        }
        body = self._set_time(data, day_of_week, hour, minute)
        return self._create('/schedules', body, 'schedule')

    def list(self, limit=None, marker=None,
             action=None, source_id=None, source_type=None):
        return self._paginated('/schedules', 'schedules', limit, marker, {
                               'action': action, 'source_id': source_id,
                               'source_type': source_type})

    def get(self, schedule_id):
        return self._get('/schedules/%s' % base.getid(schedule_id), 'schedule')

    def delete(self, schedule_id):
        return self._delete('/schedules/%s' % base.getid(schedule_id))

    def update(self, schedule_id, full_backup_retention=None,
               day_of_week=None, hour=None, minute=None, **kwargs):
        url = '/schedules/%s' % base.getid(schedule_id)
        data = {'schedule': kwargs}
        if full_backup_retention:
            data['schedule']['full_backup_retention'] = full_backup_retention
        body = self._set_time(data, day_of_week, hour, minute)
        return self._update(url, body)

    def _set_time(self, data, day_of_week=None, hour=None, minute=None):
        if day_of_week is not None:
            data['schedule']['day_of_week'] = int(day_of_week)
        if hour is not None:
            data['schedule']['hour'] = int(hour)
        if minute is not None:
            data['schedule']['minute'] = int(minute)
        return data


@utils.arg('--action', metavar='<action>',
           help='Schedule action to filter on.')
@utils.arg('--source_id', metavar='<source_id>',
           help='Source ID to filter on.')
@utils.arg('--source_type', metavar='<source_type>',
           help='Schedule type to filter on: ha or instance')
def do_schedule_list(cs, args):
    """List schedules."""
    schedules = cs.schedules.list()
    utils.print_list(
        schedules,
        ['id', 'instance_id', 'action', 'minute', 'hour',
         'day_of_month', 'month', 'day_of_week', 'last_scheduled',
         'full_backup_retention', 'next_run']
    )


@utils.arg('schedule', metavar='<schedule>', help='ID of the schedule.')
def do_schedule_show(cs, args):
    """Get a schedule."""
    schedule = cs.schedules.get(args.schedule)
    utils.print_dict(schedule._info)


@utils.arg('--instance_id', metavar='<instance_id>',
           help='ID of the instance.')
@utils.arg('--source_id', metavar='<source_id>',
           help='ID of the source.')
@utils.arg('--day', metavar='<day>', type=int,
           help='Integer of day to run the automated backup on. '
                '[0(sun)-6(sat)]')
@utils.arg('--hour', metavar='<hour>', type=int,
           help='Hour of the day to run the automated backup. [0-23]')
@utils.arg('--minute', metavar='<minute>', type=int,
           help='Minute of the hour to run the automated backup. [0-59]')
@utils.arg('--source_type', metavar='<source_type>',
           help='Type of source ("ha", "instance").')
@utils.arg('--copy-to', metavar='<copy_to>',
           help=('Comma separated list of data centers to copy this '
                 'backup to on completion, eg.: DFW,IAD'))
def do_schedule_create_backup(cs, args):
    """Create a new schedule for an instance."""
    if (args.instance_id is None and args.source_id is None):
        err_msg = ('Specify either an instance id or ha source id.'
                   '$trove help schedule-create-backup')
        raise exceptions.CommandError(err_msg)
    if (args.instance_id and args.source_id):
        err_msg = ('Specify either an instance or ha source id.'
                   '$trove help schedule-create-backup')
    schedule = cs.schedules.create_backup(
        instance_id=args.instance_id,
        source_id=args.source_id,
        day_of_week=args.day,
        hour=args.hour,
        minute=args.minute,
        source_type=args.source_type,
        copy_to=args.copy_to
    )
    utils.print_dict(schedule._info)


@utils.arg('schedule', metavar='<schedule>', help='ID of the schedule.')
def do_schedule_delete(cs, args):
    """Delete a schedule."""
    cs.schedules.delete(args.schedule)


@utils.arg('schedule', metavar='<schedule>', help='ID of the schedule')
@utils.arg('--full-backup-retention', metavar='<full_backup_retention>',
           type=int, help=('The number of full backups to keep.'))
@utils.arg('--day', metavar='<day>', type=int,
           help='Integer of day to run the automated backup on. '
                '[0(sun)-6(sat)]')
@utils.arg('--hour', metavar='<hour>', type=int,
           help='Hour of the day to run the automated backup. [0-23]')
@utils.arg('--minute', metavar='<minute>', type=int,
           help='Minute of the hour to run the automated backup. [0-59]')
@utils.arg('--run-now', action='store_true',
           help=('Update next-run to now; forces the backup to start during '
                 'the next periodic task cycle.'))
@utils.arg('--copy-to', metavar='<copy_to>',
           help=('Comma separated list of data centers to copy this '
                 'backup to on completion, eg.: DFW,IAD'))
def do_schedule_update(cs, args):
    """Update a schedule"""
    schedule = cs.schedules.update(
        args.schedule,
        full_backup_retention=args.full_backup_retention,
        day_of_week=args.day,
        hour=args.hour,
        minute=args.minute,
        run_now=args.run_now,
        copy_to=args.copy_to
    )
