# Overview

Unofficial Python bindings for the Jellyfin API. Our goal is to mirror [pkkid/python-plexapi](https://github.com/pkkid/python-plexapi>) to allow [Jellyfin-Meta-Manager](https://github.com/ghomasHudson/Jellyfin-Meta-Manager>) to directly use this as a drop-in-replacement.

## Project status
- [x] Logging in
- [ ] Searching
- [ ] Shows
- [ ] Library
- [ ] Movies

# Installation & Documentation

```python
pip install jellyfinapi
```

# Connecting to a Jellyfin Instance

Pass in the baseurl and auth token:

```python
    from jellyfinapi.server import JellyfinServer
    baseurl = 'http://jellyfinserver:32400'
    token = '2ffLuB84dqLswk9skLos'
    jellyfin = JellyfinServer(baseurl, token)
```

# Usage Examples

```python
    # Example 1: List all unwatched movies.
    movies = jellyfin.library.section('Movies')
    for video in movies.search(unwatched=True):
        print(video.title)
```

```python
    # Example 2: Mark all Game of Thrones episodes as played.
    jellyfin.library.section('TV Shows').get('Game of Thrones').markPlayed()
```

```python
    # Example 3: List all clients connected to the Server.
    for client in jellyfin.clients():
        print(client.title)
```

```python
    # Example 4: Play the movie Cars on another client.
    # Note: Client must be on same network as server.
    cars = jellyfin.library.section('Movies').get('Cars')
    client = jellyfin.client("Michael's iPhone")
    client.playMedia(cars)
```

```python
    # Example 5: List all content with the word 'Game' in the title.
    for video in jellyfin.search('Game'):
        print(f'{video.title} ({video.TYPE})')
```

```python
    # Example 6: List all movies directed by the same person as Elephants Dream.
    movies = jellyfin.library.section('Movies')
    elephants_dream = movies.get('Elephants Dream')
    director = elephants_dream.directors[0]
    for movie in movies.search(None, director=director):
        print(movie.title)
```

```python
    # Example 7: List files for the latest episode of The 100.
    last_episode = jellyfin.library.section('TV Shows').get('The 100').episodes()[-1]
    for part in last_episode.iterParts():
        print(part.file)
```

```python
    # Example 8: Get audio/video/all playlists
    for playlist in jellyfin.playlists():
        print(playlist.title)
```

```python
    # Example 9: Rate the 100 four stars.
    jellyfin.library.section('TV Shows').get('The 100').rate(8.0)
```

Common Questions
----------------

What are some helpful links if trying to understand the raw Jellyfin API?

https://api.jellyfin.org/
