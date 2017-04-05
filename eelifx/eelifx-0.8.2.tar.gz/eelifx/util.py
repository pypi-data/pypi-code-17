import sys
import typing
import asyncio
import logging
from copy import deepcopy
from pprint import pformat

from eelifx.bulbs import Bulbs
from eelifx.lifx_commander import LifxCommander
from eelifx.processor import process_game_state


def shutdown_loop(loop):
    logging.info('Cancelling tasks...')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    logging.info('Bye, exiting soon...')


def compile_items(uncomplied: typing.List[typing.Dict], item_key: str, mode: str='exec'):
    res = deepcopy(uncomplied)
    for item in res:
        if item_key not in item:
            logging.warning(
                "Could not find %s in object %s.",
                item_key,
                item
            )
            next
        try:
            item['%s_compiled' % item_key] = compile(item[item_key], '<string>', mode)
        except Exception as e:
            logging.exception("Unable to compile the following code to a python code object: %s" % pformat(item[item_key]))
            raise
    return res


async def wait_for_members(
    loop: asyncio.AbstractEventLoop,
    bulbs: Bulbs,
    lifx_commanders: typing.Sequence[LifxCommander],
    poll_interval: int,
    config: typing.Dict,
    mode: str
):
    ok = True

    if mode in ['grouptest', 'reset']:
        logging.info(f'Forcing wait_for_members on for {mode}')
        config['wait_for_members'] = True

    if 'wait_for_members' in config and config['wait_for_members']:
        logging.info('Checking to see if our groups have members yet')
        if not all([l.has_members(bulbs) for l in lifx_commanders]):
            ok = False
            logging.info(
                'At least one group has no members and wait_for_members is set to true, will retry in %s seconds.',
                poll_interval
            )
    # requeue check
    if not ok:
        await asyncio.sleep(poll_interval)
        asyncio.ensure_future(wait_for_members(loop, bulbs, lifx_commanders, poll_interval, config, mode))

    if ok:
        logging.info('At least one globe in each group is present, or wait_for_members is set to false.')
        logging.info('Compiling base states...')
        config['groups'] = compile_items(config['groups'], 'base_state', mode='exec')

        groups = []

        for group in config['groups']:
            groups.append(deepcopy(group))
            logging.info('Compiling rule statements...')
            groups[-1]['rules'] = compile_items(groups[-1]['rules'], 'statement', mode='eval')
            logging.info('Compiling effects statements...')
            groups[-1]['rules'] = compile_items(groups[-1]['rules'], 'effect', mode='exec')

        if mode == 'grouptest':
            asyncio.ensure_future(
                group_test(loop, bulbs, lifx_commanders, 5, groups, 0, 0)
            )
        elif mode == 'run':
            asyncio.ensure_future(
                process_game_state(loop, bulbs, lifx_commanders, poll_interval, groups, config['endpoint'])
            )
        else:
            asyncio.ensure_future(
                reset_lights(loop, bulbs, lifx_commanders, 5, groups)
            )


async def reset_lights(
    loop: asyncio.AbstractEventLoop,
    bulbs: Bulbs,
    lifx_commanders: typing.Sequence[LifxCommander],
    poll_interval: int,
    groups: typing.Dict
):
    for lc_index, group in enumerate(groups):
        lifx_commanders[lc_index].reset()
        exec(group['base_state_compiled'])
        lifx_commanders[lc_index].apply(bulbs)
    await asyncio.sleep(poll_interval)
    loop.stop()


async def group_test(
    loop: asyncio.AbstractEventLoop,
    bulbs: Bulbs,
    lifx_commanders: typing.Sequence[LifxCommander],
    poll_interval: int,
    groups: typing.Dict,
    group: int,
    rule: int
):
    logging.info(
        "Resetting lights to base state"
    )
    lc_index = group
    exec(groups[group]['base_state_compiled'])
    lifx_commanders[lc_index].apply(bulbs)
    await asyncio.sleep(poll_interval)
    logging.info(
        "[Group %s][Rule %s] Running block for condition '%s'",
        group,
        rule,
        groups[group]['rules'][rule]['statement']
    )
    exec(groups[group]['rules'][rule]['effect_compiled'])
    lifx_commanders[lc_index].apply(bulbs)
    lifx_commanders[lc_index].reset()
    await asyncio.sleep(poll_interval)
    rule += 1

    if rule == len(groups[group]['rules']):
        rule = 0
        group += 1

        if group == len(groups):
            logging.info('End of test cycle')
            loop.stop()

    asyncio.ensure_future(group_test(loop, bulbs, lifx_commanders, poll_interval, groups, group, rule))


def marshal_commanders(config):
    lifx_commanders = []
    for group in config['groups']:
        lifx_commanders.append(
            LifxCommander(
                poll_interval=config['poll_interval'],
                target_group=group['match'],
                max_luminance=group['max_luminance'],
                colour_temp=group['colour_temp']
            )
        )

    if len(lifx_commanders) == 0:
        logging.error('No groups have been defined in the config!')
        sys.exit(1)

    return lifx_commanders


def normalise_endpoint(endpoint):
    if not endpoint.startswith('http'):
        endpoint = f'http://{endpoint}'

    if not endpoint.endswith(':8080/exec.lua'):
        endpoint = f'{endpoint}:8080/exec.lua'

    if not endpoint.endswith('/exec.lua'):
        endpoint = f'{endpoint}/exec.lua'

    return endpoint
