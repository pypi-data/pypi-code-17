import asyncio
import logging
import random
import time
import yaml

from aiohttp import web
from collections import Counter
from concurrent.futures import CancelledError
from datetime import datetime
from enum import Enum
from os import path

logger = logging.getLogger(__name__)

DEFAULT_STATE_FILENAME = path.join(
    path.dirname(__file__), 'default-state.yaml')

def compute_deployable_resonators(data):
    for offset, count in enumerate((1, 1, 2, 2, 4, 4, 4, 8)):
        if data.get(8 - offset, 0) < count:
            yield 8 - offset

class Faction(Enum):
    NEUTRAL = 0
    ENL = 1
    RES = 2

class Resonator(object):
    POSITIONS = set(['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'])

    __slots__ = ('level', 'health', 'owner', 'position')

    def __init__(self, *, level, health, owner, position):
        if position not in self.POSITIONS:
            raise ValueError(
                'position must be one of %r found %r' %
                (self.POSITIONS, position))

        self.level = level
        self.health = health
        self.owner = owner
        self.position = position

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class Portal(object):
    def __init__(self, *, title, faction=Faction.NEUTRAL, resonators=None):
        self.title = title
        self.faction = faction
        self.resonators = list(resonators) if resonators else []

        if self.faction == Faction.NEUTRAL and resonators:
            raise ValueError(
                'Faction must be ENL or RES if there are resonators')
        elif self.faction != Faction.NEUTRAL and not resonators:
            raise ValueError(
                'Faction may not be ENL or RES if there are no resonators')

    @property
    def level(self):
        return max(1, int(sum(r.level for r in self.resonators) / 8))

    @property
    def health(self):
        if not self.resonators:
            return 0

        return int(
            sum(r.health for r in self.resonators) / len(self.resonators))

    def to_dict(self):
        return {
            'controllingFaction': str(self.faction.value),
            'level': self.level,
            'health': self.health,
            'title': self.title,
            'resonators': [r.to_dict() for r in self.resonators],
        }

    @classmethod
    def from_dict(cls, data):
        data['faction'] = Faction(int(data.pop('controllingFaction')))
        data['resonators'] = [
            Resonator.from_dict(r) for r in data['resonators']]

        data.pop('level', None)
        data.pop('health', None)

        return cls(**data)

class State(object):
    def __init__(
            self,
            *,
            relay_mode,
            relay_state,
            agents,
            actions,
            portal):

        # order is important
        self.relay_state = relay_state
        self.relay_mode = relay_mode

        self.agents = list(set(agents['res']) | set(agents['enl']))
        self.enl_agents = list(set(agents['enl']))
        self.res_agents = list(set(agents['res']))

        self.max_sleep_seconds = actions['max_sleep_seconds']
        self.probabilities = actions['probabilities']
        self.faction_change_ts = actions.get('faction_change_ts')
        self.resonator_lost_ts = actions.get('resonator_lost_ts')

        self.portal = Portal.from_dict(portal)

    @asyncio.coroutine
    def action_loop(self):
        try:
            while True:
                action = self.random_action()
                action_ts = int(time.time() * 1000)

                if action == 'none':
                    pass
                else:
                    try:
                        getattr(self, 'do_' + action)(action_ts)
                    except AttributeError:
                        logger.warn('Uknown action %r', action)

                yield from asyncio.sleep(
                    random.random() * self.max_sleep_seconds)
        except CancelledError:
            pass

    def do_attack(self, action_ts):
        if self.portal.faction == Faction.NEUTRAL:
            logger.info('action "attack" skipped on nuetral portal')
            return

        if self.portal.faction == Faction.ENL:
            actor = random.choice(self.res_agents)
        else:
            actor = random.choice(self.enl_agents)

        damage = int(random.random() * 20)
        if self.portal.health <= damage:
            self.faction_change_ts = action_ts
            self.resonator_lost_ts = action_ts
            self.portal.faction = Faction.NEUTRAL
            self.portal.resonators = []
            status = 'neutralized the portal'
        else:
            remaining = []
            for resonator in self.portal.resonators:
                resonator.health -= damage
                if resonator.health > 0:
                    remaining.append(resonator)
                else:
                    self.resonator_lost_ts = action_ts

            status = 'destroyed %d resonators' % (
                len(self.portal.resonators) - len(remaining))
            self.portal.resonators = remaining

        logger.info(
            '%s: %r attacked the portal causing %d damage to each '
            'resonator and %s',
            datetime.fromtimestamp(action_ts / 1000),
            actor,
            damage,
            status)

    def do_deploy(self, action_ts):
        if self.portal.faction == Faction.NEUTRAL:
            self.faction_change_ts = action_ts
            actor = random.choice(self.agents)
            if actor in self.enl_agents:
                self.portal.faction = Faction.ENL
            else:
                self.portal.faction = Faction.RES

        elif self.portal.faction == Faction.ENL:
            actor = random.choice(self.enl_agents)
        else:
            actor = random.choice(self.res_agents)

        if len(self.portal.resonators) < 8:
            available_positions = list(Resonator.POSITIONS -
                set(r.position for r in self.portal.resonators))
            levels = list(compute_deployable_resonators(Counter(
                [r.level for r in self.portal.resonators
                if r.owner == actor])))

            resonator = Resonator(
                level=random.choice(levels),
                health=100,
                owner=actor,
                position=random.choice(available_positions))
            self.portal.resonators.append(resonator)

            logger.info(
                '%s: %r deployed an L%d resonator in position %s',
                datetime.fromtimestamp(action_ts / 1000),
                actor,
                resonator.level,
                resonator.position)
        else:
            # find an agent able to deploy on this portal starting with the
            # selected agent
            if self.portal.faction == Faction.ENL:
                actors = list(self.enl_agents)
            else:
                actors = list(self.res_agents)
            actors.remove(actor)
            random.shuffle(actors)
            actors.insert(0, actor)
            for actor in actors:
                levels = [
                    l for l in compute_deployable_resonators(Counter(
                        [r.level for r in self.portal.resonators
                        if r.owner == actor]))
                    if any(l > r.level for r in self.portal.resonators)]
                if not levels:
                    continue

                level = random.choice(levels)
                resonator = random.choice([
                    r for r in self.portal.resonators if level > r.level])

                resonator.level = level
                resonator.health = 100
                resonator.owner = actor

                logger.info(
                    '%s: %r upgraded a resonator to L%d in position %s',
                    datetime.fromtimestamp(action_ts / 1000),
                    actor,
                    resonator.level,
                    resonator.position)
                return

            logger.info('no agents could deploy on the portal')

    def do_flip(self, action_ts):
        if self.portal.faction == Faction.NEUTRAL:
            logger.info('action "flip" skipped on nuetral portal')
            return

        actor = random.choice(self.agents)
        if actor in self.res_agents and self.portal.faction == Faction.RES:
            owner = '__JARVIS__'
        elif actor in self.enl_agents and self.portal.faction == Faction.ENL:
            owner = '__ADA__'
        else:
            owner = actor

        self.faction_change_ts = action_ts
        if self.portal.faction == Faction.RES:
            self.portal.faction = Faction.ENL
        else:
            self.portal.faction = Faction.RES

        for resonator in self.portal.resonators:
            resonator.owner = owner
            resonator.health = 100

        logger.info(
            '%s, %r flipped the portal to %s and the current owner is %r',
            datetime.fromtimestamp(action_ts / 1000),
            actor,
            self.portal.faction.name,
            owner)

    def do_recharge(self, action_ts):
        if self.portal.faction == Faction.NEUTRAL:
            logger.info('action "recharge" skipped on nuetral portal')
            return

        if self.portal.faction == Faction.ENL:
            actor = random.choice(self.enl_agents)
        else:
            actor = random.choice(self.res_agents)

        health = int(random.random() * 10)
        for resonator in self.portal.resonators:
            resonator.health = min(100, resonator.health + health)

        logger.info(
            '%s: %r recharged the portal %d percent',
            datetime.fromtimestamp(action_ts / 1000), actor, health)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            return cls(**yaml.load(f))

    @property
    def probabilities(self):
        return self._probabilities

    @probabilities.setter
    def probabilities(self, probabilities):
        # convert action information into a more computationally friendly form
        action_range = []
        action_range_end = 0

        for key, value in probabilities.items():
            action_range_end += value
            action_range.append((action_range_end, key))

        _, self._action_range_else = action_range.pop()
        self._action_range = action_range
        self._action_range_end = action_range_end
        self._probabilities = probabilities

    def random_action(self):
        value = random.random() * self._action_range_end
        for limit, action in self._action_range:
            if value < limit:
                return action

        return self._action_range_else

    @property
    def relay_state(self):
        if self.relay_mode == 0:
            pass

        elif self.relay_mode == 1:
            self._relay_state = int(self.portal.faction != Faction.NEUTRAL)

        elif self.relay_mode == 2:
            self._relay_state = int(self.portal.faction == Faction.NEUTRAL)

        elif self.relay_mode == 3:
            if (self.faction_change_ts
                    and (time.time() - self.faction_change_ts / 1000 < 3)):
                self._relay_state = 0
            else:
                self._relay_state = int(
                    self.portal.faction != Faction.NEUTRAL)

        elif self.relay_mode == 4:
            if (self.resonator_lost_ts
                    and (time.time() - self.resonator_lost_ts / 1000 < 1.5)):
                self._relay_state = 0
            else:
                self._relay_state = int(
                    self.portal.faction != Faction.NEUTRAL)

        else:
            raise RuntimeError(
                'Relay mode %s not implemented!' % self.relay_mode)

        return self._relay_state

    @relay_state.setter
    def relay_state(self, value):
        self._relay_state = value
        self.relay_mode = 0

    def save(self, filename):
        with open(filename, 'wb') as f:
            yaml.dump(
                dict(
                    relay_mode=self.relay_mode,
                    relay_state=self.relay_state,
                    actions=dict(
                        max_sleep_seconds=self.max_sleep_seconds,
                        probabilities=self.probabilities,
                        faction_change_ts=self.faction_change_ts,
                        resonator_lost_ts=self.resonator_lost_ts),
                    agents=dict(
                        res=list(self.res_agents),
                        enl=list(self.enl_agents)),
                    portal=self.portal.to_dict(),
                ),
                stream=f,
                encoding='utf-8',
                allow_unicode=True,
                default_flow_style=False)

    @asyncio.coroutine
    def start_action_loop(self, app):
        app['action_loop_task'] = app.loop.create_task(self.action_loop())

    @asyncio.coroutine
    def stop_action_loop_and_save(self, app):
        app['action_loop_task'].cancel()
        yield from app['action_loop_task']

        self.save(app['state_filename'])

@asyncio.coroutine
def diagnostics_handler(request):
    return web.Response(text=state.portal.title)

@asyncio.coroutine
def relay_handler(request):
    command = request.match_info['relay_command']

    if command == 'get_mode':
        return web.Response(text=str(state.relay_mode))

    if command == 'get_state':
        return web.Response(text=str(state.relay_state))

    if command == 'set_manual':
        state.relay_mode = 0
        return web.Response(text='ok')

    if command.startswith('set_auto'):
        try:
            new_mode = int(command[8:])
        except ValueError:
            raise web.HTTPNotFound()

        if not (1 <= new_mode <= 4):
            raise web.HTTPNotFound()

        state.relay_mode = new_mode
        return web.Response(text='ok')

    if command == 'high':
        state.relay_state = 1
        return web.Response(text='ok')

    if command == 'low':
        state.relay_state = 0
        return web.Response(text='ok')

    if command == 'toggle':
        state.relay_state = int(not state.relay_state)
        return web.Response(text='ok')

    raise web.HTTPNotFound()

@asyncio.coroutine
def status_handler(request):
    status_type = request.match_info['status_type']
    if status_type == 'json':
        return web.json_response({'status': state.portal.to_dict()})

    if status_type == 'faction':
        return web.Response(text=str(state.portal.faction.value))

    if status_type == 'health':
        return web.Response(text=str(state.portal.health))

    if status_type == 'title':
        return web.Response(text=state.portal.title)

    raise web.HTTPNotFound()

def main(*, state_filename=None, host='0.0.0.0', port=8080, debug=False):
    global state
    if state_filename and path.isfile(state_filename):
        state = State.load(state_filename)
    else:
        state = State.load(DEFAULT_STATE_FILENAME)

    app = web.Application(debug=debug)
    app['state'] = state
    app['state_filename'] = state_filename
    app.on_startup.append(state.start_action_loop)
    app.on_cleanup.append(state.stop_action_loop_and_save)

    module_app = web.Application()
    command_app = web.Application()

    command_app.router.add_route('*', '/relay/{relay_command}', relay_handler)
    command_app.router.add_route('*', '/diagnostics', diagnostics_handler)

    module_app.add_subapp('/command', command_app)
    module_app.router.add_route('*', '/status/{status_type}', status_handler)

    app.add_subapp('/module', module_app)
    web.run_app(app, host=host, port=port)
