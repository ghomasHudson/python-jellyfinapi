# -*- coding: utf-8 -*-
import os
from pathlib import Path
from urllib.parse import quote_plus

from jellyfinapi import media, utils, video
from jellyfinapi.base import Playable, JellyfinPartialObject, JellyfinSession
from jellyfinapi.exceptions import BadRequest
from jellyfinapi.mixins import (
    RatingMixin,
    ArtUrlMixin, ArtMixin, PosterUrlMixin, PosterMixin,
    PhotoalbumEditMixins, PhotoEditMixins
)


@utils.registerJellyfinObject
class Photoalbum(
    JellyfinPartialObject,
    RatingMixin,
    ArtMixin, PosterMixin,
    PhotoalbumEditMixins
):
    """ Represents a single Photoalbum (collection of photos).

        Attributes:
            TAG (str): 'Directory'
            TYPE (str): 'photo'
            addedAt (datetime): Datetime the photo album was added to the library.
            art (str): URL to artwork image (/library/metadata/<ratingKey>/art/<artid>).
            composite (str): URL to composite image (/library/metadata/<ratingKey>/composite/<compositeid>)
            fields (List<:class:`~jellyfinapi.media.Field`>): List of field objects.
            guid (str): Jellyfin GUID for the photo album (local://229674).
            index (sting): Jellyfin index number for the photo album.
            key (str): API URL (/library/metadata/<ratingkey>).
            lastRatedAt (datetime): Datetime the photo album was last rated.
            librarySectionID (int): :class:`~jellyfinapi.library.LibrarySection` ID.
            librarySectionKey (str): :class:`~jellyfinapi.library.LibrarySection` key.
            librarySectionTitle (str): :class:`~jellyfinapi.library.LibrarySection` title.
            listType (str): Hardcoded as 'photo' (useful for search filters).
            ratingKey (int): Unique key identifying the photo album.
            summary (str): Summary of the photoalbum.
            thumb (str): URL to thumbnail image (/library/metadata/<ratingKey>/thumb/<thumbid>).
            title (str): Name of the photo album. (Trip to Disney World)
            titleSort (str): Title to use when sorting (defaults to title).
            type (str): 'photo'
            updatedAt (datetime): Datetime the photo album was updated.
            userRating (float): Rating of the photo album (0.0 - 10.0) equaling (0 stars - 5 stars).
    """
    TAG = 'Directory'
    TYPE = 'photo'
    _searchType = 'photoalbum'

    def _loadData(self, data):
        """ Load attribute values from Jellyfin XML response. """
        self.addedAt = utils.toDatetime(data.attrib.get('addedAt'))
        self.art = data.attrib.get('art')
        self.composite = data.attrib.get('composite')
        self.fields = self.findItems(data, media.Field)
        self.guid = data.attrib.get('guid')
        self.index = utils.cast(int, data.attrib.get('index'))
        self.key = data.attrib.get('key', '').replace('/children', '')  # FIX_BUG_50
        self.lastRatedAt = utils.toDatetime(data.attrib.get('lastRatedAt'))
        self.librarySectionID = utils.cast(int, data.attrib.get('librarySectionID'))
        self.librarySectionKey = data.attrib.get('librarySectionKey')
        self.librarySectionTitle = data.attrib.get('librarySectionTitle')
        self.listType = 'photo'
        self.ratingKey = utils.cast(int, data.attrib.get('ratingKey'))
        self.summary = data.attrib.get('summary')
        self.thumb = data.attrib.get('thumb')
        self.title = data.attrib.get('title')
        self.titleSort = data.attrib.get('titleSort', self.title)
        self.type = data.attrib.get('type')
        self.updatedAt = utils.toDatetime(data.attrib.get('updatedAt'))
        self.userRating = utils.cast(float, data.attrib.get('userRating'))

    def album(self, title):
        """ Returns the :class:`~jellyfinapi.photo.Photoalbum` that matches the specified title.

            Parameters:
                title (str): Title of the photo album to return.
        """
        key = f'{self.key}/children'
        return self.fetchItem(key, Photoalbum, title__iexact=title)

    def albums(self, **kwargs):
        """ Returns a list of :class:`~jellyfinapi.photo.Photoalbum` objects in the album. """
        key = f'{self.key}/children'
        return self.fetchItems(key, Photoalbum, **kwargs)

    def photo(self, title):
        """ Returns the :class:`~jellyfinapi.photo.Photo` that matches the specified title.

            Parameters:
                title (str): Title of the photo to return.
        """
        key = f'{self.key}/children'
        return self.fetchItem(key, Photo, title__iexact=title)

    def photos(self, **kwargs):
        """ Returns a list of :class:`~jellyfinapi.photo.Photo` objects in the album. """
        key = f'{self.key}/children'
        return self.fetchItems(key, Photo, **kwargs)

    def clip(self, title):
        """ Returns the :class:`~jellyfinapi.video.Clip` that matches the specified title.

            Parameters:
                title (str): Title of the clip to return.
        """
        key = f'{self.key}/children'
        return self.fetchItem(key, video.Clip, title__iexact=title)

    def clips(self, **kwargs):
        """ Returns a list of :class:`~jellyfinapi.video.Clip` objects in the album. """
        key = f'{self.key}/children'
        return self.fetchItems(key, video.Clip, **kwargs)

    def get(self, title):
        """ Alias to :func:`~jellyfinapi.photo.Photoalbum.photo`. """
        return self.episode(title)

    def download(self, savepath=None, keep_original_name=False, subfolders=False):
        """ Download all photos and clips from the photo album. See :func:`~jellyfinapi.base.Playable.download` for details.

            Parameters:
                savepath (str): Defaults to current working dir.
                keep_original_name (bool): True to keep the original filename otherwise
                    a friendlier filename is generated.
                subfolders (bool): True to separate photos/clips in to photo album folders.
        """
        filepaths = []
        for album in self.albums():
            _savepath = os.path.join(savepath, album.title) if subfolders else savepath
            filepaths += album.download(_savepath, keep_original_name)
        for photo in self.photos() + self.clips():
            filepaths += photo.download(savepath, keep_original_name)
        return filepaths

    def _getWebURL(self, base=None):
        """ Get the Jellyfin Web URL with the correct parameters. """
        return self._server._buildWebURL(base=base, endpoint='details', key=self.key, legacy=1)

    @property
    def metadataDirectory(self):
        """ Returns the Jellyfin Media Server data directory where the metadata is stored. """
        guid_hash = utils.sha1hash(self.guid)
        return str(Path('Metadata') / 'Photos' / guid_hash[0] / f'{guid_hash[1:]}.bundle')


@utils.registerJellyfinObject
class Photo(
    JellyfinPartialObject, Playable,
    RatingMixin,
    ArtUrlMixin, PosterUrlMixin,
    PhotoEditMixins
):
    """ Represents a single Photo.

        Attributes:
            TAG (str): 'Photo'
            TYPE (str): 'photo'
            addedAt (datetime): Datetime the photo was added to the library.
            createdAtAccuracy (str): Unknown (local).
            createdAtTZOffset (int): Unknown (-25200).
            fields (List<:class:`~jellyfinapi.media.Field`>): List of field objects.
            guid (str): Jellyfin GUID for the photo (com.jellyfinapp.agents.none://231714?lang=xn).
            index (sting): Jellyfin index number for the photo.
            key (str): API URL (/library/metadata/<ratingkey>).
            lastRatedAt (datetime): Datetime the photo was last rated.
            librarySectionID (int): :class:`~jellyfinapi.library.LibrarySection` ID.
            librarySectionKey (str): :class:`~jellyfinapi.library.LibrarySection` key.
            librarySectionTitle (str): :class:`~jellyfinapi.library.LibrarySection` title.
            listType (str): Hardcoded as 'photo' (useful for search filters).
            media (List<:class:`~jellyfinapi.media.Media`>): List of media objects.
            originallyAvailableAt (datetime): Datetime the photo was added to Jellyfin.
            parentGuid (str): Jellyfin GUID for the photo album (local://229674).
            parentIndex (int): Jellyfin index number for the photo album.
            parentKey (str): API URL of the photo album (/library/metadata/<parentRatingKey>).
            parentRatingKey (int): Unique key identifying the photo album.
            parentThumb (str): URL to photo album thumbnail image (/library/metadata/<parentRatingKey>/thumb/<thumbid>).
            parentTitle (str): Name of the photo album for the photo.
            ratingKey (int): Unique key identifying the photo.
            sourceURI (str): Remote server URI (server://<machineIdentifier>/com.jellyfinapp.plugins.library)
                (remote playlist item only).
            summary (str): Summary of the photo.
            tags (List<:class:`~jellyfinapi.media.Tag`>): List of tag objects.
            thumb (str): URL to thumbnail image (/library/metadata/<ratingKey>/thumb/<thumbid>).
            title (str): Name of the photo.
            titleSort (str): Title to use when sorting (defaults to title).
            type (str): 'photo'
            updatedAt (datetime): Datetime the photo was updated.
            userRating (float): Rating of the photo (0.0 - 10.0) equaling (0 stars - 5 stars).
            year (int): Year the photo was taken.
    """
    TAG = 'Photo'
    TYPE = 'photo'
    METADATA_TYPE = 'photo'

    def _loadData(self, data):
        """ Load attribute values from Jellyfin XML response. """
        Playable._loadData(self, data)
        self.addedAt = utils.toDatetime(data.attrib.get('addedAt'))
        self.createdAtAccuracy = data.attrib.get('createdAtAccuracy')
        self.createdAtTZOffset = utils.cast(int, data.attrib.get('createdAtTZOffset'))
        self.fields = self.findItems(data, media.Field)
        self.guid = data.attrib.get('guid')
        self.index = utils.cast(int, data.attrib.get('index'))
        self.key = data.attrib.get('key', '')
        self.lastRatedAt = utils.toDatetime(data.attrib.get('lastRatedAt'))
        self.librarySectionID = utils.cast(int, data.attrib.get('librarySectionID'))
        self.librarySectionKey = data.attrib.get('librarySectionKey')
        self.librarySectionTitle = data.attrib.get('librarySectionTitle')
        self.listType = 'photo'
        self.media = self.findItems(data, media.Media)
        self.originallyAvailableAt = utils.toDatetime(data.attrib.get('originallyAvailableAt'), '%Y-%m-%d')
        self.parentGuid = data.attrib.get('parentGuid')
        self.parentIndex = utils.cast(int, data.attrib.get('parentIndex'))
        self.parentKey = data.attrib.get('parentKey')
        self.parentRatingKey = utils.cast(int, data.attrib.get('parentRatingKey'))
        self.parentThumb = data.attrib.get('parentThumb')
        self.parentTitle = data.attrib.get('parentTitle')
        self.ratingKey = utils.cast(int, data.attrib.get('ratingKey'))
        self.sourceURI = data.attrib.get('source')  # remote playlist item
        self.summary = data.attrib.get('summary')
        self.tags = self.findItems(data, media.Tag)
        self.thumb = data.attrib.get('thumb')
        self.title = data.attrib.get('title')
        self.titleSort = data.attrib.get('titleSort', self.title)
        self.type = data.attrib.get('type')
        self.updatedAt = utils.toDatetime(data.attrib.get('updatedAt'))
        self.userRating = utils.cast(float, data.attrib.get('userRating'))
        self.year = utils.cast(int, data.attrib.get('year'))

    def _prettyfilename(self):
        """ Returns a filename for use in download. """
        if self.parentTitle:
            return f'{self.parentTitle} - {self.title}'
        return self.title

    def photoalbum(self):
        """ Return the photo's :class:`~jellyfinapi.photo.Photoalbum`. """
        return self.fetchItem(self.parentKey)

    def section(self):
        """ Returns the :class:`~jellyfinapi.library.LibrarySection` the item belongs to. """
        if hasattr(self, 'librarySectionID'):
            return self._server.library.sectionByID(self.librarySectionID)
        elif self.parentKey:
            return self._server.library.sectionByID(self.photoalbum().librarySectionID)
        else:
            raise BadRequest("Unable to get section for photo, can't find librarySectionID")

    @property
    def locations(self):
        """ This does not exist in jellyfin xml response but is added to have a common
            interface to get the locations of the photo.

            Returns:
                List<str> of file paths where the photo is found on disk.
        """
        return [part.file for item in self.media for part in item.parts if part]

    def sync(self, resolution, client=None, clientId=None, limit=None, title=None):
        """ Add current photo as sync item for specified device.
            See :func:`~jellyfinapi.myjellyfin.MyJellyfinAccount.sync` for possible exceptions.

            Parameters:
                resolution (str): maximum allowed resolution for synchronized photos, see PHOTO_QUALITY_* values in the
                                  module :mod:`~jellyfinapi.sync`.
                client (:class:`~jellyfinapi.myjellyfin.MyJellyfinDevice`): sync destination, see
                                                               :func:`~jellyfinapi.myjellyfin.MyJellyfinAccount.sync`.
                clientId (str): sync destination, see :func:`~jellyfinapi.myjellyfin.MyJellyfinAccount.sync`.
                limit (int): maximum count of items to sync, unlimited if `None`.
                title (str): descriptive title for the new :class:`~jellyfinapi.sync.SyncItem`, if empty the value would be
                             generated from metadata of current photo.

            Returns:
                :class:`~jellyfinapi.sync.SyncItem`: an instance of created syncItem.
        """

        from jellyfinapi.sync import SyncItem, Policy, MediaSettings

        myjellyfin = self._server.myJellyfinAccount()
        sync_item = SyncItem(self._server, None)
        sync_item.title = title if title else self.title
        sync_item.rootTitle = self.title
        sync_item.contentType = self.listType
        sync_item.metadataType = self.METADATA_TYPE
        sync_item.machineIdentifier = self._server.machineIdentifier

        section = self.section()

        sync_item.location = f'library://{section.uuid}/item/{quote_plus(self.key)}'
        sync_item.policy = Policy.create(limit)
        sync_item.mediaSettings = MediaSettings.createPhoto(resolution)

        return myjellyfin.sync(sync_item, client=client, clientId=clientId)

    def _getWebURL(self, base=None):
        """ Get the Jellyfin Web URL with the correct parameters. """
        return self._server._buildWebURL(base=base, endpoint='details', key=self.parentKey, legacy=1)

    @property
    def metadataDirectory(self):
        """ Returns the Jellyfin Media Server data directory where the metadata is stored. """
        guid_hash = utils.sha1hash(self.parentGuid)
        return str(Path('Metadata') / 'Photos' / guid_hash[0] / f'{guid_hash[1:]}.bundle')


@utils.registerJellyfinObject
class PhotoSession(JellyfinSession, Photo):
    """ Represents a single Photo session
        loaded from :func:`~jellyfinapi.server.JellyfinServer.sessions`.
    """
    _SESSIONTYPE = True

    def _loadData(self, data):
        """ Load attribute values from Jellyfin XML response. """
        Photo._loadData(self, data)
        JellyfinSession._loadData(self, data)
