import requests
import logging
import re

API_KEY = "cb700fa2ce68e0fbec249b14c2758770"#4d4e18e860de2c06184b5d4a60263c39
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

logging.basicConfig(level=logging.ERROR)

def make_request(method: str, params: dict):
    params.update({
        "api_key": API_KEY,
        "format": "json",
        "method": method
    })
    try:
        res = requests.get(BASE_URL, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e} - {res.text}")
    except requests.exceptions.Timeout:
        logging.error("Request timed out")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception: {e}")
    return None


def artist_info(name: str):
    return make_request("artist.getinfo", {"artist": name})


def artist_top_tracks(name: str):
    return make_request("artist.gettoptracks", {"artist": name})


def similar_artists(name: str):
    return make_request("artist.getsimilar", {"artist": name})


def album_info(artist: str, album: str):
    return make_request("album.getinfo", {"artist": artist, "album": album})


def search_artist(name: str):
    return make_request("artist.search", {"artist": name})


def search_track(name: str):
    return make_request("track.search", {"track": name})


def route_music_query(query: str):
    query = query.lower()

    if match := re.search(r"artist info for (.+)", query):
        return artist_info(match.group(1))

    if match := re.search(r"top tracks by (.+)", query):
        return artist_top_tracks(match.group(1))

    if match := re.search(r"artists like (.+)", query):
        return similar_artists(match.group(1))

    if match := re.search(r"album info for (.+) by (.+)", query):
        return album_info(match.group(2), match.group(1))

    if match := re.search(r"search artist (.+)", query):
        return search_artist(match.group(1))

    if match := re.search(r"search track (.+)", query):
        return search_track(match.group(1))

    return search_artist(query)

def format_music_response(data):
    if not data:
        return "No music information found."

    if "artist" in data:
        artist = data["artist"]
        bio = artist.get("bio", {}).get("summary", "")
        tags = [t["name"] for t in artist.get("tags", {}).get("tag", [])]
        return f"{artist.get('name')}\nTags: {', '.join(tags)}\n\nBio: {bio[:300]}..."

    if "toptracks" in data:
        tracks = data["toptracks"].get("track", [])
        if not tracks:
            return "No top tracks found."
        return "\n".join([f"{t['name']} ({t['playcount']} plays)" for t in tracks[:5]])

    if "similarartists" in data:
        artists = data["similarartists"].get("artist", [])
        return "Similar Artists:\n" + ", ".join([a["name"] for a in artists[:5]])

    if "album" in data:
        album = data["album"]
        tracks = album.get("tracks", {}).get("track", [])
        track_list = "\n".join([f"🎶 {t['name']}" for t in tracks[:5]]) if isinstance(tracks, list) else "No tracks found"
        return f"{album.get('name')} by {album.get('artist')}\nTracks:\n{track_list}"

    if "results" in data:
        matches = data["results"].get("artistmatches", {}).get("artist", []) or \
                  data["results"].get("trackmatches", {}).get("track", [])
        if not matches:
            return "No search results found."
        return "\n".join([f"🎵 {m['name']} - {m.get('artist', '')}" for m in matches[:5]])

    return str(data)

