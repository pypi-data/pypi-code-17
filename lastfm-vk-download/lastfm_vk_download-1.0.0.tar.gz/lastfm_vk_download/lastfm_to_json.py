#!/usr/bin/env python3

import requests
import click  # pip install --user click
import json
from functools import partial


TRACKS_PER_PAGE = 50


def request_page(api_key: str, username: str, period: str, page: int):
    """Requests a page with 50 tracks"""
    response = requests.get(
        "https://ws.audioscrobbler.com/2.0/",
        params={
            "method": "user.gettoptracks",
            "user": username,
            "api_key": api_key,
            "page": str(page),  # count from 1, not from 0
            "limit": str(TRACKS_PER_PAGE),  # tracks per page
            "period": period,
            "format": "json"
        }
    )
    assert response.status_code == 200  # 200 means OK
    return response


def extract_tracks(page_json):
    return [
        {
            "artist": track["artist"]["name"],
            "title": track["name"],
            "lastfm_url": track["url"],
            "musicbrainz_id": track["mbid"]
            
        }
        for track in page_json["toptracks"]["track"]]


def get_tracks(api_key, username, period, num_tracks, skip_tracks):
    """Calls lastfm API many times. Returns a list of jsons."""
    request_page_with_settings = partial(request_page, api_key, username, period)
    tracks = []
    page1_json = request_page_with_settings(1).json()
    
    total_tracks = int(page1_json["toptracks"]["@attr"]["total"])
    assert total_tracks >= num_tracks + skip_tracks
    
    # need_pages * TRACKS_PER_PAGE >= num_tracks + skip_tracks
    need_pages = (num_tracks + skip_tracks) // TRACKS_PER_PAGE + 1
    
    tracks.extend(extract_tracks(page1_json))
    
    for page in range(2, need_pages + 1):
        page_json = request_page_with_settings(page).json()
        tracks.extend(extract_tracks(page_json))
        
    return tracks[skip_tracks:skip_tracks + num_tracks]


@click.command()
@click.pass_context
@click.option("--api-key", type=str, required=True, envvar="LASTFM_API_KEY",
              help="Lastfm API key. You can also use LASTFM_API_KEY environment variable.")
@click.option("--username", "-u", type=str, required=True)
@click.option("--num-tracks", "-n", type=int, default=60, show_default=True)
@click.option("--skip-tracks", "-s", help="number of tracks to save",
              type=int, default=0, show_default=True)
@click.option("--period", "-p", help="time period over which to retrieve top tracks for",
              type=click.Choice(["overall", "7day", "1month", "3month", "6month", "12month"]),
              default="overall")
@click.argument("output", type=click.File(mode='w', encoding='utf-8'))
def save_tracks(context, api_key, username, num_tracks, skip_tracks, output, period):
    assert skip_tracks >= 0
    assert num_tracks > 0
    jsons = get_tracks(api_key, username, period, num_tracks, skip_tracks)
    json.dump(jsons, output, ensure_ascii=False, indent=2, sort_keys=True)


if __name__ == "__main__":
    save_tracks()
