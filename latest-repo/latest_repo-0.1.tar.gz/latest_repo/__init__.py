from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from github import Github
import arrow
import os
import time
import tzlocal


app = Flask(__name__)
Bootstrap(app)

@app.route('/repo')
def latest_repo():

    '''client_id and client_secret generated via registration of new application
    on Gitgub account. Increases rate limit from 60/h to 5000/h
    Client_id and client_secret saved in os.environ to protect private data'''
    try:
        g = Github(client_id = os.environ['client_id'], client_secret = os.environ['client_secret'])
    except:
        g = Github()

	# pass login of GitHub user or organisation, here allegro
    login_name = g.get_user('allegro')

	# gets (user/org)'s full name, here Allegro Tech
    name = login_name.name

    #creates dict with (user/org)'s repositories names and pushed time
    results = {}
    """
    TIP: do get_repos() można przekazać argumenty odpowiadające za sortowanie,
         dzięki temu można będzie zrezygnować z funkcji max() do wybrania
         najświeższego repo.
    """
    repos = login_name.get_repos()
    for repo in repos:
        results[repo.name] = repo.pushed_at

    #gets the latest repo by it's pushed time
    repo_name = max(results.keys(), key=(lambda k: results[k]))

    ############################################################
    """
    Between hashes extra code showing information about:
    - when repository was updated
    - rate limiting
    - remaining time
    """

    '''gets time of latest pushed_at, which is info that goes to 'updated (...) ago' info 
    (not updated_at, which might be e.g. repo's description edit, which doesn't 
    places the repository on the top of the GitHub page)'''
    updated_time = (results.get(repo_name))
    nicely_to_arrow = arrow.get(updated_time)
    updated = nicely_to_arrow.humanize()

    #gets user's limit and remaining rates
    limit_list = list(g.rate_limiting)
    remaining = limit_list[0]
    limit_per_h = limit_list[1]
    limit = 'Rate limit: {}/h, remaining: {}.'.format(limit_per_h, remaining)

    #gets time left to reset the rate clock
    reset_timestamp = g.rate_limiting_resettime
    local_timezone = tzlocal.get_localzone()
    reset_time = datetime.fromtimestamp(reset_timestamp, local_timezone)
    
    #counts time left to reset in timestamp
    time_now = time.time()
    delta = reset_timestamp - time_now

    #conversion time left from timestamp to strftime in minutes and seconds
    time_left = reset_time.strftime("%d %B %Y, %H:%M:%S")
    user_timezone = reset_time.strftime("%Z")
    minutes_left = datetime.fromtimestamp(delta).strftime('%M')
    seconds_left = datetime.fromtimestamp(delta).strftime('%S')

    reset = 'Limit will be renewed on: {} of your timezone ({}), it means in {} minutes and {} seconds.'.format(time_left, user_timezone, minutes_left, seconds_left)

    ############################################################

    return render_template("repo.html", name=name, repo_name=repo_name, updated=updated, limit=limit, reset=reset)

if __name__ == "__main__":
    app.run()
