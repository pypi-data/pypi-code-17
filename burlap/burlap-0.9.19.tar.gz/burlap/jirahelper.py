from __future__ import print_function

import sys
import re
import traceback
from pprint import pprint

from burlap import ContainerSatchel
from burlap.constants import *
from burlap.decorators import task

class JiraHelperSatchel(ContainerSatchel):
    
    name = 'jirahelper'
    
    def set_defaults(self):
    
        self.env.server = None
        self.env.basic_auth_username = None
        self.env.basic_auth_password = None
        self.env.update_from_git = False
        self.env.ticket_update_message_template = 'This has been deployed to {role}.'
        
        # A map of status->transition to follow when making deployments.
        self.env.deploy_workflow = {}
        
        # A map of the new-status->new-assignee to auto-assign.
        self.env.assignee_by_status = {}
        
        # The regex used to search the commit messages for a ticket number.
        self.env.ticket_pattern = None

    def get_tickets_from_str(self, s):
        pattern = re.compile(self.env.ticket_pattern, flags=re.I)
        tickets = []
        if self.env.ticket_pattern:
            pattern = re.compile(self.env.ticket_pattern, flags=re.I)
            tickets.extend(pattern.findall(s))
        return set(_.strip().upper() for _ in tickets)

    @task
    def get_tickets_between_commits(self, a, b):
        from burlap.git import gittracker
        tickets = []
        if self.env.ticket_pattern:
            ret = gittracker.get_logs_between_commits(a, b)
            tickets.extend(self.get_tickets_from_str(ret))
        self.vprint(tickets)
        return tickets
    
    @task
    def update_tickets_from_git(self, from_commit=None, to_commit=None):
        """
        Run during a deployment.
        Looks at all commits between now and the last deployment.
        Finds all ticket numbers and updates their status in Jira.
        """
        from jira import JIRA, JIRAError
        from burlap.deploy import get_last_current_diffs
        from burlap.git import gittracker, CURRENT_COMMIT
        
        r = self.local_renderer
        
#         get_current_commit = gittracker.get_current_commit
#         GITTRACKER = gittracker.name.upper()
        
        # Ensure this is only run once per role.
        if self.genv.host_string != self.genv.hosts[-1]:
            self.vprint('Not first server. Aborting.')
            return
        
        print('self.env.update_from_git:', self.env.update_from_git)
        print('self.genv.jirahelper_update_from_git:', self.genv.jirahelper_update_from_git)
        if not self.env.update_from_git:
            self.vprint('Update from git disabled. Aborting.')
            return
        
        if not self.env.ticket_pattern:
            self.vprint('No ticket pattern defined. Aborting.')
            return
        
        if not self.env.basic_auth_username or not self.env.basic_auth_password:
            self.vprint('Username or password not given. Aborting.')
            return
        
        # During a deployment, we should be given these, but for testing,
        # lookup the diffs dynamically.
        last = gittracker.last_manifest
        current = gittracker.current_manifest
        
        last_commit = from_commit or last.current_commit#[CURRENT_COMMIT]
        print('last_commit:', last_commit)
        current_commit = to_commit or current[CURRENT_COMMIT]
        print('current_commit:', current_commit)
        
        if not last_commit or not current_commit:
            print('Missing commit ID. Aborting.')
            return
        
        if self.verbose:
            print('-'*80)
            print('last.keys:', last.keys())
            print('-'*80)
            print('current.keys:', current.keys())
        
#         try:
#             last_commit = last['GITTRACKER']['current_commit']
#         except KeyError:
#             return
#         current_commit = current['GITTRACKER']['current_commit']
        
        # Find all tickets deployed between last deployment and now.
        tickets = self.get_tickets_between_commits(current_commit, last_commit)
        if self.verbose:
            print('tickets:', tickets)
        
        # Update all tickets in Jira.
        jira = JIRA({
            'server': self.env.server
        }, basic_auth=(self.env.basic_auth_username, self.env.basic_auth_password))
        for ticket in tickets:
            
            # Mention this Jira updated.
            r.env.role = r.genv.ROLE.lower()
            comment = r.format(self.env.ticket_update_message_template)
            print('Commenting on ticket %s: %s' % (ticket, comment))
            if not self.dryrun:
                jira.add_comment(ticket, comment) 
            
            # Update ticket status.
            recheck = False
            while 1:
                print('Looking up jira ticket %s...' % ticket)
                issue = jira.issue(ticket)
                print('Ticket %s retrieved.' % ticket)
                transition_to_id = dict((t['name'], t['id']) for t in jira.transitions(issue))
                print('%i allowable transitions found:')
                pprint(transition_to_id)
                print('issue.fields.status.id:', issue.fields.status.id)
                print('issue.fields.status.name:', issue.fields.status.name)
                jira_status_id = issue.fields.status.name.title()
                print('jira_status_id:', jira_status_id)
                next_transition_name = self.env.deploy_workflow.get(jira_status_id)
                print('next_transition_name:', next_transition_name)
                next_transition_id = transition_to_id.get(next_transition_name)
                print('next_transition_id:', next_transition_id)
                if next_transition_name:
                    new_fields = {}
                    new_assignee = self.env.assignee_by_status.get(
                        #issue.fields.status.name.title(),
                        next_transition_name,
                        issue.fields.assignee.name,
                    )
                    if new_assignee == 'reporter':
                        new_assignee = issue.fields.reporter.name
    #                 print('new_assignee:', new_assignee)
                        
                    print('Updating ticket %s to status %s (%s) and assigning it to %s.' \
                        % (ticket, next_transition_name, next_transition_id, new_assignee))
                    if not self.dryrun:
                        try:
                            jira.transition_issue(
                                issue,
                                next_transition_id,
                            )
                            recheck = True
                        except AttributeError as e:
                            print('Unable to transition ticket %s to %s: %s' \
                                % (ticket, next_transition_name, e), file=sys.stderr)
                            traceback.print_exc()
                        
                        # Note assignment should happen after transition, since the assignment may
                        # effect remove transitions that we need.
                        try:
                            if new_assignee:
                                print('Assigning ticket %s to %s.' % (ticket, new_assignee))
                                jira.assign_issue(issue, new_assignee)
                            else:
                                print('No new assignee found.')
                        except JIRAError as e:
                            print('Unable to reassign ticket %s to %s: %s' \
                                % (ticket, new_assignee, e), file=sys.stderr)
                else:
                    recheck = False
                    print('No transitions found for ticket %s currently in status "%s".' \
                        % (ticket, issue.fields.status.name))
                        
                if not recheck:
                    break

jirahelper = JiraHelperSatchel()
