Python-JellyfinAPI
==============
.. image:: https://github.com/pkkid/python-jellyfinapi/workflows/CI/badge.svg
    :target: https://github.com/pkkid/python-jellyfinapi/actions?query=workflow%3ACI
.. image:: https://readthedocs.org/projects/python-jellyfinapi/badge/?version=latest
    :target: http://python-jellyfinapi.readthedocs.io/en/latest/?badge=latest
.. image:: https://codecov.io/gh/pkkid/python-jellyfinapi/branch/master/graph/badge.svg?token=fOECznuMtw
    :target: https://codecov.io/gh/pkkid/python-jellyfinapi
.. image:: https://img.shields.io/github/tag/pkkid/python-jellyfinapi.svg?label=github+release
    :target: https://github.com/pkkid/python-jellyfinapi/releases
.. image:: https://badge.fury.io/py/JellyfinAPI.svg
    :target: https://badge.fury.io/py/JellyfinAPI
.. image:: https://img.shields.io/github/last-commit/pkkid/python-jellyfinapi.svg
    :target: https://img.shields.io/github/last-commit/pkkid/python-jellyfinapi.svg


Overview
--------
Unofficial Python bindings for the Jellyfin API. Our goal is to match all capabilities of the official
Jellyfin Web Client. A few of the many features we currently support are:

* Navigate local or remote shared libraries.
* Perform library actions such as scan, analyze, empty trash.
* Remote control and play media on connected clients, including `Controlling Sonos speakers`_
* Listen in on all Jellyfin Server notifications.
 

Installation & Documentation
----------------------------

.. code-block:: python

    pip install jellyfinapi

*Install extra features:*

.. code-block:: python

    pip install jellyfinapi[alert]  # Install with dependencies required for jellyfinapi.alert

Documentation_ can be found at Read the Docs.

.. _Documentation: http://python-jellyfinapi.readthedocs.io/en/latest/

Join our Discord_ for support and discussion.

.. _Discord: https://discord.gg/GtAnnZAkuw


Getting a JellyfinServer Instance
-----------------------------

There are two types of authentication. If you are running on a separate network
or using Jellyfin Users you can log into MyJellyfin to get a JellyfinServer instance. An
example of this is below. NOTE: Servername below is the name of the server (not
the hostname and port).  If logged into Jellyfin Web you can see the server name in
the top left above your available libraries.

.. code-block:: python

    from jellyfinapi.myjellyfin import MyJellyfinAccount
    account = MyJellyfinAccount('<USERNAME>', '<PASSWORD>')
    jellyfin = account.resource('<SERVERNAME>').connect()  # returns a JellyfinServer instance

If you want to avoid logging into MyJellyfin and you already know your auth token
string, you can use the JellyfinServer object directly as above, by passing in
the baseurl and auth token directly.

.. code-block:: python

    from jellyfinapi.server import JellyfinServer
    baseurl = 'http://jellyfinserver:32400'
    token = '2ffLuB84dqLswk9skLos'
    jellyfin = JellyfinServer(baseurl, token)


Usage Examples
--------------

.. code-block:: python

    # Example 1: List all unwatched movies.
    movies = jellyfin.library.section('Movies')
    for video in movies.search(unwatched=True):
        print(video.title)


.. code-block:: python

    # Example 2: Mark all Game of Thrones episodes as played.
    jellyfin.library.section('TV Shows').get('Game of Thrones').markPlayed()


.. code-block:: python

    # Example 3: List all clients connected to the Server.
    for client in jellyfin.clients():
        print(client.title)


.. code-block:: python

    # Example 4: Play the movie Cars on another client.
    # Note: Client must be on same network as server.
    cars = jellyfin.library.section('Movies').get('Cars')
    client = jellyfin.client("Michael's iPhone")
    client.playMedia(cars)


.. code-block:: python

    # Example 5: List all content with the word 'Game' in the title.
    for video in jellyfin.search('Game'):
        print(f'{video.title} ({video.TYPE})')


.. code-block:: python

    # Example 6: List all movies directed by the same person as Elephants Dream.
    movies = jellyfin.library.section('Movies')
    elephants_dream = movies.get('Elephants Dream')
    director = elephants_dream.directors[0]
    for movie in movies.search(None, director=director):
        print(movie.title)


.. code-block:: python

    # Example 7: List files for the latest episode of The 100.
    last_episode = jellyfin.library.section('TV Shows').get('The 100').episodes()[-1]
    for part in last_episode.iterParts():
        print(part.file)


.. code-block:: python

    # Example 8: Get audio/video/all playlists
    for playlist in jellyfin.playlists():
        print(playlist.title)


.. code-block:: python

    # Example 9: Rate the 100 four stars.
    jellyfin.library.section('TV Shows').get('The 100').rate(8.0)


Running tests over JellyfinAPI
--------------------------

Use:

.. code-block:: bash

     tools/jellyfin-boostraptest.py 
    
with appropriate
arguments and add this new server to a shared user which username is defined in environment variable `SHARED_USERNAME`.
It uses `official docker image`_ to create a proper instance.

For skipping the docker and reuse a existing server use 

.. code-block:: bash

    python jellyfin-bootstraptest.py --no-docker --username USERNAME --password PASSWORD --server-name NAME-OF-YOUR-SEVER

Also in order to run most of the tests you have to provide some environment variables:

* `PLEXAPI_AUTH_SERVER_BASEURL` containing an URL to your Jellyfin instance, e.g. `http://127.0.0.1:32400` (without trailing
  slash)
* `PLEXAPI_AUTH_MYPLEX_USERNAME` and `PLEXAPI_AUTH_MYPLEX_PASSWORD` with your MyJellyfin username and password accordingly

After this step you can run tests with following command:

.. code-block:: bash

    py.test tests -rxXs --ignore=tests/test_sync.py

Some of the tests in main test-suite require a shared user in your account (e.g. `test_myjellyfin_users`,
`test_myjellyfin_updateFriend`, etc.), you need to provide a valid shared user's username to get them running you need to
provide the username of the shared user as an environment variable `SHARED_USERNAME`. You can enable a Guest account and
simply pass `Guest` as `SHARED_USERNAME` (or just create a user like `jellyfinapitest` and play with it).

To be able to run tests over Mobile Sync api you have to some some more environment variables, to following values
exactly:

* PLEXAPI_HEADER_PROVIDES='controller,sync-target'
* PLEXAPI_HEADER_PLATFORM=iOS
* PLEXAPI_HEADER_PLATFORM_VERSION=11.4.1
* PLEXAPI_HEADER_DEVICE=iPhone

And finally run the sync-related tests:

.. code-block:: bash

    py.test tests/test_sync.py -rxXs

.. _official docker image: https://hub.docker.com/r/jellyfininc/pms-docker/

Common Questions
----------------

**What are some helpful links if trying to understand the raw Jellyfin API?**

* https://api.jellyfin.org/
