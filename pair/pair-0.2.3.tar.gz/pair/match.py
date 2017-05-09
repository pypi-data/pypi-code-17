# match.py
## matches teams to opponents
## and/or players into teams

# imports
import copy
import random
from networkx import Graph, max_weight_matching
from kuhn_munkres import Cost, Matrix

# functions
def make_entity_list(entities, scramble=False):
    entity_list, mappings = list(), list()
    i = 0
    for entity in entities:
        count = max(entities[entity]['count'], 0)
        mappings += ([entity,] * count)
        entity_list += range(i, i+count)
        i += count
    if scramble: random.shuffle(mappings)
    return entity_list, mappings

def process_pairs(matchings, mappings):
    processed, results = set(), set()
    for team in matchings:
        opp = matchings[team]
        if (team not in processed and opp not in processed):
            results.add((mappings[team], mappings[opp]))
            processed.update([team, opp])
    return results

def pair_some_teams(teams, score_fn, scramble=False):
    """single iteration of team pairing"""
    team_list, mappings = make_entity_list(teams, scramble)
    team_graph = Graph()
    team_graph.add_nodes_from(team_list)
    for i in xrange(len(team_list)):
        team, added = team_list[i], set()
        team_ID = mappings[team]
        for opp in team_list[(i+1):]: # prior teams already connected
            opp_ID = mappings[opp]
            if opp_ID in added: continue # skip all but first
            if (opp_ID is not team_ID and
                opp_ID not in teams[team_ID]['conflicts'] and
                team_ID not in teams[opp_ID]['conflicts']):
                weight = score_fn(teams[team_ID]['rating'],
                                  teams[opp_ID]['rating'])
                added.add(opp_ID)
                team_graph.add_edge(team, opp, weight=weight)
    max_matchings = max_weight_matching(team_graph, True)
    return process_pairs(max_matchings, mappings)

def decrement_and_conflict(data, val, opponent, remove=True):
    """helper for post-processing partial pairings"""
    decrement_update(data, val, remove)
    if val in data:
        if isinstance(data[val]['conflicts'], set):
            data[val]['conflicts'].add(opponent)
        else: data[val]['conflicts'].append(opponent)

def prune_full_conflicts(data):
    """removes values that have all other values as conflicts"""
    all_vals, to_pop = set(data), set()
    for val in data:
        conflicts = set(data[val].get('conflicts', set()))
        conflicts.intersection_update(all_vals)
        conflicts.update(set([val,]))
        if len(conflicts) == len(all_vals): to_pop.add(val)
    for val in to_pop: data.pop(val)

def pair_teams(teams, score_fn, scramble=False):
    """
    generates optimal team pairings
    :param teams: a dictionary of teams, with teams[teamID]
      returning a dictionary with 'rating', 'count', and 'conflicts',
      teams[teamID]['count'] as an nonnegative integer,
      and teams[teamID]['conflicts'] as a list of team ID's
    :param score_fn: a function that, given two ratings,
      returns a nonnegative score such that higher scores are better,
      e.g.: abs(.5 - p(rating_1 beats rating_2))
      score_fn should be commutative
    :param scramble: (bool) whether to add randomization
    :return: team pairings (using ID's)
    :rtype: set of tuples
    """
    teams = copy.deepcopy(teams)
    for team in set(teams):
        if teams[team]['count'] < 1: teams.pop(team)
    results = set()
    while len(teams) > 1:
        temp_results = pair_some_teams(teams, score_fn, scramble)
        results.update(temp_results)
        for x,y in temp_results:
            decrement_and_conflict(teams, x, y)
            decrement_and_conflict(teams, y, x)
        prune_full_conflicts(teams)
    return results

def pair_players(players, score_fn, scramble=False):
    """
    generates optimal player pairings
    :param players: a dictionary of players, with players[playerID]
      returning a dictionary with 'rating', 'count', and 'conflicts',
      players[playerID]['count'] as an nonnegative integer,
      and players[playerID]['conflicts'] as a list of player ID's
    :param score_fn: a function that, given two ratings,
      returns a nonnegative score such that higher scores are better,
      e.g.: abs(.5 - p(rating_1 beats rating_2))
      score_fn should be commutative
    :param scramble: (bool) whether to randomize
    :return: player pairings (using ID's)
    :rtype: set of tuples
    """
    return pair_teams(players, score_fn, scramble)

def group_teams(teams, score_fn, game_size, scramble=False):
    """
    attempts to generate optimal team groupings
    :param teams: a dictionary of teams, with teams[teamID]
      returning a dictionary with 'rating', 'count', and 'conflicts',
      teams[teamID]['count'] as a nonnegative integer
      representing the maximum number of games to make with that team,
      and teams[teamID]['conflicts'] as a list of team ID's
    :param score_fn: a function that, given an arbitrary number of
      ratings, returns a score such that higher scores
      are preferable, e.g. a measure of variance
      score_fn should be commutative and associative
    :param game_size: number of teams per game
    :param scramble: (bool) whether to add randomness
    :return: team groupings (using ID's)
    :rtype: set of tuples
    """
    if (game_size < 2):
        return set([(team,) for team in teams])
    elif (game_size == 2):
        return pair_teams(teams, score_fn, scramble)
    mappings = make_entity_list(teams)[1]
    remains = copy.copy(mappings)
    counts = dict()
    for team in teams:
        counts[team] = 0
    groupings = set()
    for team in mappings:
        if counts[team] >= teams[team]['count']: continue
        current = [team,]
        for i in xrange(game_size-1):
            remaining = [t for t in remains if
                         (t not in current and
                          tuple(sorted(current + [t,]))
                          not in groupings)]
            for teamID in  current:
                remaining = [t for t in remaining if
                             (t not in teams[teamID]['conflicts'] and
                              teamID not in teams[t]['conflicts'])]
            if len(remaining) == 0: break
            remaining.sort(key=lambda x:
                           score_fn(teams[x]['rating'],
                           *[teams[t]['rating'] for t in current]))
            current.append(remaining[0])
        if len(current) < game_size: continue
        for i in xrange(len(current)):
            counts[current[i]] += 1
            remains.remove(current[i])
        groupings.add(tuple(sorted(current)))
    return groupings

def group_players(players, score_fn, team_size, scramble=False):
    """
    attempts to generate optimal player groupings
    :param players: a dictionary of players, with players[playerID]
      returning a dictionary with 'rating', 'count', and 'conflicts',
      players[playerID]['count'] as a nonnegative integer
      representing the number of teams to make with that player,
      and players[playerID]['conflicts'] as a list of player ID's
    :param score_fn: a function that, given an arbitrary number of
      ratings, returns a score such that higher scores
      are preferable, e.g. a measure of variance
      score_fn should be commutative and associative
    :param team_size: number of players per team
    :param scramble: (bool) whether to add randomness
    :return: player groupings (using ID's)
    :rtype: set of tuples
    """
    return group_teams(players, score_fn, team_size, scramble)

def process_assignments(assignments, match_map, temp_map,
                         matchings):
    results = set()
    for match, temp in assignments: # unpack tuple
        if (match >= len(match_map) or
            temp >= len(temp_map)): continue
        match_ID, temp_ID = match_map[match], temp_map[temp]
        if temp_ID in matchings[match_ID].get('conflicts', dict()):
            continue
        results.add((match_ID, temp_ID))
    return results

def perform_assignments(matchings, match_list, match_map,
                        temp_list, temp_map):
    array = list()
    for match in match_list:
        match_row, match_ID = list(), match_map[match]
        scores = matchings[match_ID].get('scores', dict())
        conflicts = matchings[match_ID].get('conflicts', set())
        for temp in temp_list:
            temp_ID = temp_map[temp]
            if (temp_ID in conflicts): score = Cost(1, 0)
            else: score = Cost(0, scores.get(temp_ID, 0))
            match_row.append(score)
        array.append(match_row)
    m = Matrix(array)
    assignments = m.solve()
    return process_assignments(assignments, match_map, temp_map,
                               matchings)

def decrement_update(data, val, remove=True):
    ct = data[val]['count']
    if remove and ct < 2: data.pop(val)
    else: data[val]['count'] -= 1

def get_full_conflicts(matchings):
    conflicts = None
    for matching in matchings:
        match_conf = set(matchings[matching].get('conflicts', set()))
        if conflicts is None: conflicts = match_conf
        else: conflicts.intersection_update(match_conf)
    return conflicts

def add_to_conflicts(matchings, m, t):
    if m not in matchings: return
    elif 'conflicts' not in matchings[m]:
        matchings[m]['conflicts'] = set()
    elif not isinstance(matchings[m]['conflicts'], set):
        matchings[m]['conflicts'] = set(matchings[m]['conflicts'])
    matchings[m]['conflicts'].add(t)

def assign_by_count(matchings, templates, scramble=False):
    matchings, templates = copy.deepcopy(matchings), copy.deepcopy(templates)
    if not(len(matchings) and len(templates)): return set()
    results, full_conflicts = set(), get_full_conflicts(matchings)
    while (len(matchings) and (len(full_conflicts) < len(templates))):
        match_list, match_map = make_entity_list(matchings, scramble)
        temp_list, temp_map = make_entity_list(templates, scramble)
        assignments = perform_assignments(matchings, match_list, match_map,
                                          temp_list, temp_map)
        if not(len(assignments)): break
        results.update(assignments)
        update_after_assignment(matchings, templates, assignments)
        full_conflicts = get_full_conflicts(matchings)
    return results

def randomized_assign(matching, data, templates):
    entities, conflicts = dict(), set(data.get('conflicts', set()))
    scores, max_score = data.get('scores', dict()), 0
    for template in templates:
        if template in conflicts: continue
        score = scores.get(template, 0)
        if score > max_score: max_score = score
    for template in templates:
        if template in conflicts: continue
        entities[template] = {'count': max_score + 1 - scores.get(template, 0)}
    if not len(entities): return
    entity_list, mapping = make_entity_list(entities)
    random.shuffle(entity_list)
    return (matching, mapping[entity_list[0]])

def assign_without_count(matchings, templates):
    results = set()
    for matching in matchings:
        data = matchings[matching]
        count = data['count']
        while count > 0:
            count -= 1
            assignment = randomized_assign(matching, data, templates)
            if assignment is None: continue
            add_to_conflicts(matchings, matching, assignment[1])
            results.add(assignment)
    return results

def update_after_assignment(matchings, templates, assignments, remove=True):
    for m, t in assignments:
        decrement_update(matchings, m)
        decrement_update(templates, t, remove)
        add_to_conflicts(matchings, m, t)

def assign_by_usage(matchings, templates, scramble=False):
    usages = dict()
    for template in templates:
        usage = templates[template].get('usage', 0)
        if usage not in usages: usages[usage] = set()
        usages[usage].add(template)
    results, full_conflicts = set(), get_full_conflicts(matchings)
    temp_data, cohort = dict(), min(usages)
    while len(matchings) and (len(full_conflicts) < len(templates)):
        for temp in temp_data: temp_data[temp]['count'] += 1
        for template in usages.get(cohort, set()):
            temp_data[template] = {'count': 1}
        assignments = assign_by_count(matchings, temp_data, scramble)
        results.update(assignments)
        update_after_assignment(matchings, temp_data, assignments, False)
        full_conflicts = get_full_conflicts(matchings)
        cohort += 1
    return results

def assign_templates(matchings, templates, scramble=False):
    """
    given game matchings and templates, provides optimal template assignments
    :param matchings: a dictionary that maps matching tuples to another
      dictionary containing each matching's
      'count' (maximum # of games to be created with this matching),
      'scores' (a dictionary mapping template ID's to the scores
                this matching has for that template; default 0
                with higher scores having lower preference),
      and 'conflicts' (a set containing ID's of templates
                       this matching cannot play on)
    :param templates: a set or dictionary mapping template ID's to another
      dictionary, optionally containing each template's count or usage
      (templates must be consistent- if 'count' is supplied for one template,
       it should be supplied for all others as well)
      'count' (maximum # of games to be created with this template)
      'usage' (# of games that have already taken place with this template)
      if 'count' is supplied, assignments will be performed using counts
      if 'usage' is supplied, assignments will be performed using usage
      if neither is supplied, a weighted random method will be used
    :param scramble: (optional, default False) whether to add randomization
    :return: assignments-template assignments
    :rtype: set of tuples
    """
    matchings, templates = copy.deepcopy(matchings), copy.deepcopy(templates)
    if not len(templates): return set()
    if isinstance(templates, set):
        return assign_without_count(matchings, templates)
    elif 'count' in templates[templates.keys()[0]]:
        return assign_by_count(matchings, templates, scramble)
    elif 'usage' in templates[templates.keys()[0]]:
        return assign_by_usage(matchings, templates, scramble)
    else: return assign_without_count(matchings, templates)
