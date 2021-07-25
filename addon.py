#-------------------------------------------------------------#
# -*- coding: utf-8 -*-										  #
#-------------------------------------------------------------#
# IPTV-Tools.com											  #
# Copyright 2021 (c) ERDesigns								  #
#															  #
# Author: Ernst Reidinga 									  #
# Email: contact@erdesigns.eu    							  #
#-------------------------------------------------------------#
# Changelog:												  #
# 1.0.0														  #
# - Initial test                         				 	  #
#-------------------------------------------------------------#

import os
import sys
import urllib
from urllib.parse import parse_qsl
import xbmcgui
import xbmcplugin
import xbmcaddon
import erdplugintools
import datetime

__addon_name__ = 'IPTV-Tools'
# Set useragent for entire addon
useragent = 'Official Kodi Addon ({})'.format(erdplugintools.get_addon_id())
# Image path
__image_path__ = os.path.join(erdplugintools.get_runtime_path(), 'resources', 'images')
# Get the plugin url in plugin:// notation.
__url__ = sys.argv[0]
# Get the plugin handle as an integer number.
__handle__ = int(sys.argv[1])
# Addon instance for reading strings
addon = xbmcaddon.Addon()

# Actions - Main menu
action_main_m = 'main_movies'
action_main_s = 'main_series'
action_main_a = 'main_account'

# Actions - Movies menu
action_movies_now_playing = 'movies_now_playing'
action_movies_top_rated = 'movies_top_rated'
action_movies_popular = 'movies_popular'
action_movies_browse = 'movies_browse'
action_movies_browse_group = 'movies_browse_group'
action_movies_find = 'movies_find'
action_movies_new = 'movies_new'

# Actions - Series menu
action_series_now_on_tv = 'series_now_on_tv'
action_series_top_rated = 'series_top_rated'
action_series_popular = 'series_popular'
action_series_browse = 'series_browse'
action_series_browse_group = 'series_browse_group'
action_series_browse_serie = 'series_browse_serie'
action_series_browse_episodes = 'series_browse_episodes'
action_series_find = 'series_find'
action_series_new = 'series_new'

# API address
api = 'http://kodi-api.iptv-tools.com'

# Images
image_account = 'account.png'
image_movies = 'movies.png'
image_series = 'series.png'
image_fanart = 'fanart.png'

image_movies_now_playing = 'movies-cinema.png'
image_movies_top_rated = 'movies-star.png'
image_movies_popular = 'movies-popular.png'
image_movies_browse = 'movies-browse.png'
image_movies_find = 'movies-search.png'
image_movies_new = 'movies-new.png'

image_series_now_on_tv = 'series-now-on-tv.png'
image_series_top_rated = 'series-star.png'
image_series_popular = 'series-popular.png'
image_series_browse = 'series-browse.png'
image_series_find = 'series-search.png'
image_series_new = 'series-new.png'

# Big Images
image_account_big = 'account-big.png'
image_movies_big = 'movies-big.png'
image_series_big = 'series-big.png'

image_movies_now_playing_big = 'movies-cinema-big.png'
image_movies_top_rated_big = 'movies-star-big.png'
image_movies_popular_big = 'movies-popular-big.png'
image_movies_browse_big = 'movies-browse-big.png'
image_movies_find_big = 'movies-search-big.png'
image_movies_new_big = 'movies-new-big.png'

image_series_now_on_tv_big = 'series-now-on-tv-big.png'
image_series_top_rated_big = 'series-star-big.png'
image_series_popular_big = 'series-popular-big.png'
image_series_browse_big = 'series-browse-big.png'
image_series_find_big = 'series-search-big.png'
image_series_new_big = 'series-new-big.png'

# ---------------------------------------------------------------------------------------------------------
#  Read addon variables from settings.xml
# ---------------------------------------------------------------------------------------------------------
username = erdplugintools.get_local_setting('username')
password = erdplugintools.get_local_setting('password')
instcode = erdplugintools.get_local_setting('code')

# ---------------------------------------------------------------------------------------------------------
#  Re-Set addon variables from settings.xml - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def set_variables_from_settings():
	# IPTV-Tools Login username & password & instance code
	global username
	username = erdplugintools.get_local_setting('username')
	global password
	password = erdplugintools.get_local_setting('password')
	global instcode
	instcode = erdplugintools.get_local_setting('code')

# ---------------------------------------------------------------------------------------------------------
#  Get image - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_image(image):
	return os.path.join(__image_path__, image)

# ---------------------------------------------------------------------------------------------------------
#  Authenticate user (Login) - Return value: List
# ---------------------------------------------------------------------------------------------------------
def authenticate():
	erdplugintools.debug_log('Try to login user - username {} - password {} - code {}'.format(username, password, instcode))
	return erdplugintools.post_json('{}/authenticate'.format(api), { 'username': username, 'password': password, 'code': instcode }, useragent)

# ---------------------------------------------------------------------------------------------------------
#  Load Addon menu items - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_addon_main_menu(params):
	if not username and not password and not instcode:
		erdplugintools.open_settings_dialog()
		set_variables_from_settings()
		exit()
	response = authenticate()
	if response and response['status'] == True:
		# Load main menu
		erdplugintools.add_simple_item(action = action_main_m, title = addon.getLocalizedString(32001), plot = addon.getLocalizedString(32021), icon = get_image(image_movies), thumbnail = get_image(image_movies_big), poster =  get_image(image_movies_big), fanart = get_image(image_fanart), folder = True, api_key = response['data']['api_key'])
		erdplugintools.add_simple_item(action = action_main_s, title = addon.getLocalizedString(32002), plot = addon.getLocalizedString(32022), icon = get_image(image_series), thumbnail = get_image(image_series_big), poster =  get_image(image_series_big), fanart = get_image(image_fanart), folder = True, api_key = response['data']['api_key'])
		erdplugintools.add_simple_item(action = action_main_a, title = addon.getLocalizedString(32003), plot = addon.getLocalizedString(32023), icon = get_image(image_account), thumbnail = get_image(image_account_big), poster =  get_image(image_account_big), fanart = get_image(image_fanart), folder = False, api_key = response['data']['api_key'])
		erdplugintools.close_item_list()
	else:
		# Login Failed
		erdplugintools.message_ok_dialog(__addon_name__, addon.getLocalizedString(32101))
		exit()

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Movies menu items - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_addon_movies_menu(params):
	erdplugintools.add_simple_item(action = action_movies_now_playing, title = addon.getLocalizedString(32004), plot = addon.getLocalizedString(32024), icon = get_image(image_movies_now_playing), thumbnail = get_image(image_movies_now_playing_big), poster =  get_image(image_movies_now_playing_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_movies_top_rated, title = addon.getLocalizedString(32005), plot = addon.getLocalizedString(32025), icon = get_image(image_movies_top_rated), thumbnail = get_image(image_movies_top_rated_big), poster =  get_image(image_movies_top_rated_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_movies_popular, title = addon.getLocalizedString(32006), plot = addon.getLocalizedString(32026), icon = get_image(image_movies_popular), thumbnail = get_image(image_movies_popular_big), poster =  get_image(image_movies_popular_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_movies_browse, title = addon.getLocalizedString(32007), plot = addon.getLocalizedString(32027), icon = get_image(image_movies_browse), thumbnail = get_image(image_movies_browse_big), poster =  get_image(image_movies_browse_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_movies_find, title = addon.getLocalizedString(32008), plot = addon.getLocalizedString(32028), icon = get_image(image_movies_find), thumbnail = get_image(image_movies_find_big), poster =  get_image(image_movies_find_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_movies_new, title = addon.getLocalizedString(32009), plot = addon.getLocalizedString(32029), icon = get_image(image_movies_new), thumbnail = get_image(image_movies_new_big), poster =  get_image(image_movies_new_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.close_item_list()

# ---------------------------------------------------------------------------------------------------------
#  Load Movies - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_movies(path, api_key, search = ''):
	movies = erdplugintools.post_json(path.format(api), { 'api_key': api_key, 'search': search }, useragent)['data']
	# Create a list for our movies.
	listing = []
	for index, movie in enumerate(movies):
		li = xbmcgui.ListItem(label = movie['tmdb']['title'])
		# Images
		if not movie['tmdb']['poster_path']:
			poster = movie['stream_tvg_logo']
		else:
			poster = 'http://tmdb-img.iptv-tools.com{}'.format(movie['tmdb']['poster_path'])
		if not movie['tmdb']['backdrop_path']:
			fanart = ''
		else:
			fanart = 'http://tmdb-img.iptv-tools.com{}'.format(movie['tmdb']['backdrop_path'])
		li.setArt({ 'poster': poster, 'thumb': poster, 'fanart': fanart })
		# Set is playable
		li.setProperty('IsPlayable', 'true')
		# Label
		li.setLabel(movie['tmdb']['title'])
		# Movie Info
		li.setInfo('video', {
			'date': datetime.datetime.utcfromtimestamp(int(movie['added'])).strftime(addon.getLocalizedString(32299)),
			'tracknumber': index,
			'genre': erdplugintools.get_genres(movie['tmdb']['genres']),
			'country': erdplugintools.get_countries(movie['tmdb']['production_countries']),
			'year': erdplugintools.get_year(movie['tmdb']['release_date']),
			#'rating': movie['tmdb']['vote_average'],
			'director': erdplugintools.get_directors(movie['tmdb_credits']['crew']),
			'plot': movie['tmdb']['overview'],
			'title': movie['tmdb']['title'],
			'originaltitle': movie['tmdb']['original_title'],
			'duration': erdplugintools.get_runtime(movie['tmdb']['runtime']),
			'studio': erdplugintools.get_studios(movie['tmdb']['production_companies']),
			'tagline': movie['tmdb']['tagline'],
			'writer': erdplugintools.get_writers(movie['tmdb_credits']['crew']),
			'premiered': movie['tmdb']['release_date'],
			'tag': erdplugintools.get_tags(movie['tmdb_keywords']),
			'imdbnumber': movie['tmdb']['imdb_id'],
			#'votes': movie['tmdb']['vote_count'],
			'trailer': erdplugintools.get_trailer(movie['tmdb_videos']),
			'mediatype': 'movie'
		})
		# Cast
		if movie['tmdb_credits'] and movie['tmdb_credits']['cast']:
			li.setCast(erdplugintools.get_cast(movie['tmdb_credits']['cast']))
		# Rating
		li.setRating('tmdb', movie['tmdb']['vote_average'], movie['tmdb']['vote_count'], True)
		# Unique ID's
		li.setUniqueIDs({ 'imdb': movie['tmdb']['imdb_id'], 'tmdb' : movie['tmdb']['id'] }, 'tmdb')
		# Is playable
		li.setProperty('IsPlayable', 'true')
		# Format URL - Play movie with id and file ext
		url = 'http://tv.iptv-tools.com/movie/{}/{}/{}.{}'.format(username, movie['password'], movie['id'], movie['source_container_extension'])
		listing.append((url, li, False))
	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_DATE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_TRACKNUM)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_TITLE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_DURATION)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_GENRE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_VIDEO_RATING)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_STUDIO)
	xbmcplugin.endOfDirectory(__handle__)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmcplugin.setPluginCategory(int(sys.argv[1]), addon.getLocalizedString(32004))

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Movies - Now in Theaters - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_movies_now_in_theaters(params):
	load_movies('{}/movies/now-in-theaters', params['api_key'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Movies - Top Rated - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_movies_top_rated(params):
	load_movies('{}/movies/top-rated', params['api_key'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Movies - Popular - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_movies_popular(params):
	load_movies('{}/movies/popular', params['api_key'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Movies - Search - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_movies_search(api_key, search):
	load_movies('{}/movies/search', api_key, search)

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Movies - New - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_movies_new(params):
	load_movies('{}/movies/new', params['api_key'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Movies - Browse - Groups - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_movies_browse_groups(params):
	groups = erdplugintools.post_json('{}/movies/groups'.format(api), { 'api_key': params['api_key'] }, useragent)['data']
	for group in groups:
		erdplugintools.add_simple_item(action = action_movies_browse_group, title = group['group_name'], icon = get_image(image_movies_browse), thumbnail = get_image(image_movies_browse_big), poster =  get_image(image_movies_browse_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'], group = group['id'])
	erdplugintools.close_item_list()

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Movies - Browse - Group['id'] - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_movies_browse_group(params):
	load_movies('{}/movies/browse/' + params['group'], params['api_key'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Series menu items - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_addon_series_menu(params):
	erdplugintools.add_simple_item(action = action_series_now_on_tv, title = addon.getLocalizedString(32010), plot = addon.getLocalizedString(32030), icon = get_image(image_series_now_on_tv), thumbnail = get_image(image_series_now_on_tv_big), poster =  get_image(image_series_now_on_tv_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_series_top_rated, title = addon.getLocalizedString(32011), plot = addon.getLocalizedString(32031), icon = get_image(image_series_top_rated), thumbnail = get_image(image_series_top_rated_big), poster =  get_image(image_series_top_rated_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_series_popular, title = addon.getLocalizedString(32012), plot = addon.getLocalizedString(32031), icon = get_image(image_series_popular), thumbnail = get_image(image_series_popular_big), poster =  get_image(image_series_popular_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_series_browse, title = addon.getLocalizedString(32013), plot = addon.getLocalizedString(32033), icon = get_image(image_series_browse), thumbnail = get_image(image_series_browse_big), poster =  get_image(image_series_browse_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_series_find, title = addon.getLocalizedString(32014), plot = addon.getLocalizedString(32034), icon = get_image(image_series_find), thumbnail = get_image(image_series_find_big), poster =  get_image(image_series_find_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.add_simple_item(action = action_series_new, title = addon.getLocalizedString(32015), plot = addon.getLocalizedString(32034), icon = get_image(image_series_new), thumbnail = get_image(image_series_new_big), poster =  get_image(image_series_new_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'])
	erdplugintools.close_item_list()

# ---------------------------------------------------------------------------------------------------------
#  Load Series - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series(path, api_key, title = '', search = '', group = 0):
	series = erdplugintools.post_json(path.format(api), { 'api_key': api_key, 'search': search, 'group': group }, useragent)['data']
	# Create a list for our series.
	listing = []
	for index, serie in enumerate(series):
		li = xbmcgui.ListItem(label = serie['tmdb']['name'])
		# Set is folder - the series is just a folder containing episodes
		li.setIsFolder(True)
		# Set is playable - yes because we want to move to the series folder
		li.setProperty('IsPlayable', 'true')
		# Images
		if not serie['tmdb']['poster_path']:
			poster = serie['stream_tvg_logo']
		else:
			poster = 'http://tmdb-img.iptv-tools.com{}'.format(serie['tmdb']['poster_path'])
		if not serie['tmdb']['backdrop_path']:
			fanart = ''
		else:
			fanart = 'http://tmdb-img.iptv-tools.com{}'.format(serie['tmdb']['backdrop_path'])
		li.setArt({ 'poster': poster, 'thumb': poster, 'fanart': fanart })
		# Label
		li.setLabel(serie['tmdb']['name'])
		# Serie Info
		li.setInfo('video', {
			'tracknumber': index,
			'genre': erdplugintools.get_genres(serie['tmdb']['genres']),
			'country': erdplugintools.get_countries(serie['tmdb']['production_countries']),
			'year': erdplugintools.get_year(serie['tmdb']['first_air_date']),
			'director': erdplugintools.get_directors(serie['credits']['crew']),
			'plot': serie['tmdb']['overview'],
			'title': serie['tmdb']['name'],
			'originaltitle': serie['tmdb']['original_name'],
			'tvshowtitle': serie['tmdb']['name'],
			'duration': erdplugintools.get_episode_runtime(serie['tmdb']['episode_run_time']),
			'studio': erdplugintools.get_studios(serie['tmdb']['production_companies']),
			'tagline': serie['tmdb']['tagline'],
			'writer': erdplugintools.get_writers(serie['credits']['crew']),
			'premiered': serie['tmdb']['first_air_date'],
			'tag': erdplugintools.get_tags(serie['keywords']),
			'trailer': erdplugintools.get_trailer(serie['videos']),
			'status': serie['tmdb']['status'],
			'mediatype': 'tvshow'
		})
		# Cast
		if serie['credits'] and serie['credits']['cast']:
			li.setCast(erdplugintools.get_cast_series(serie['credits']['cast']))
		# Rating
		li.setRating('tmdb', serie['tmdb']['vote_average'], serie['tmdb']['vote_count'], True)
		# Unique ID's
		li.setUniqueIDs({ 'tmdb' : serie['tmdb']['id'] }, 'tmdb')
		# Format URL - Play movie with id and file ext
		url = '{0}?action={1}&serie={2}&playlist={3}&title={4}&api_key={5}&password={6}&fanart={7}'.format(__url__, action_series_browse_serie, serie['tmdb_id'], serie['playlist_id'], urllib.parse.quote_plus(serie['tmdb']['name']), api_key, serie['password'], fanart)
		xbmcplugin.addDirectoryItem(handle = __handle__, url = url, listitem = li, isFolder = True)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_DATE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_TRACKNUM)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_TITLE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_GENRE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_STUDIO)
	erdplugintools.close_item_list()
	xbmcplugin.setPluginCategory(int(sys.argv[1]), title)

# ---------------------------------------------------------------------------------------------------------
#  Load Series Seasons - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series_seasons(params):
	seasons = erdplugintools.post_json('{}/series/seasons'.format(api), { 'api_key': params['api_key'], 'playlist_id': params['playlist'], 'tmdb_id': params['serie'] }, useragent)['data']
	# Create a list for our series.
	listing = []
	for index, season in enumerate(seasons):
		# Season title
		title = addon.getLocalizedString(32207).format(season['serie_season'])
		li = xbmcgui.ListItem(label = title)
		# Set is folder - the series is just a folder containing episodes
		li.setIsFolder(True)
		# Set is playable - yes because we want to move to the series folder
		li.setProperty('IsPlayable', 'true')
		# Images
		li.setArt({ 'poster': get_image(image_series_browse), 'thumb': get_image(image_series_browse), 'fanart': params['fanart'] })
		# Label
		li.setLabel(title)
		# Serie Info
		li.setInfo('video', {
			'title': title,
			'mediatype': 'season'
		})
		# Format URL - Play movie with id and file ext
		url = '{0}?action={1}&serie={2}&playlist={3}&title={4}&api_key={5}&password={6}&fanart={7}&season={8}'.format(__url__, action_series_browse_episodes, params['serie'], params['playlist'], params['title'], params['api_key'], params['password'], params['fanart'], season['serie_season'])
		xbmcplugin.addDirectoryItem(handle = __handle__, url = url, listitem = li, isFolder = True)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_TRACKNUM)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_TITLE)
	erdplugintools.close_item_list()
	xbmcplugin.setPluginCategory(int(sys.argv[1]), params['title'])

# ---------------------------------------------------------------------------------------------------------
#  Load Series Episodes - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series_episodes(params):
	series = erdplugintools.post_json('{}/series/episodes'.format(api), { 'api_key': params['api_key'], 'playlist_id': params['playlist'], 'tmdb_id': params['serie'], 'season': params['season'] }, useragent)['data']
	# Create a list for our episodes.
	listing = []
	for index, serie in enumerate(series):
		li = xbmcgui.ListItem(label = serie['tmdb']['name'])
		# Set is folder - the series is just a folder containing episodes
		li.setIsFolder(True)
		# Set is playable
		li.setProperty('IsPlayable', 'true')
		# Images
		if serie['tmdb']['still_path']:
			poster = 'http://tmdb-img.iptv-tools.com{}'.format(serie['tmdb']['still_path'])
		else:
			poster = ''
		if params['fanart']:
			fanart = params['fanart']
		else:
			fanart = ''
		li.setArt({ 'poster': poster, 'thumb': poster, 'fanart': fanart })
		# Label
		title = 'S{0:02d}E{1:02d} {2}'.format(serie['serie_season'], serie['serie_episode'], serie['tmdb']['name'])
		li.setLabel(title)
		# Serie Info
		li.setInfo('video', {
			'tracknumber': index,
			'plot': serie['tmdb']['overview'],
			'title': serie['tmdb']['name'],
			'tvshowtitle': params['title'],
			'writer': erdplugintools.get_writers(serie['tmdb']['crew']),
			'premiered': serie['tmdb']['air_date'],
			'episode': serie['serie_episode'],
			'sortepisode': serie['serie_episode'],
			'season': serie['serie_season'],
			'sortseason': serie['serie_season'],
			'mediatype': 'episode'
		})
		# Cast
		if serie['tmdb'] and serie['tmdb']['guest_stars']:
			li.setCast(erdplugintools.get_cast_series(serie['tmdb']['guest_stars']))
		# Rating
		li.setRating('tmdb', serie['tmdb']['vote_average'], serie['tmdb']['vote_count'], True)
		# Unique ID's
		li.setUniqueIDs({ 'tmdb' : serie['tmdb']['id'] }, 'tmdb')
		# Format URL - Play movie with id and file ext
		url = 'http://tv.iptv-tools.com/series/{}/{}/{}.{}'.format(username, params['password'], serie['id'], serie['source_container_extension'])
		listing.append((url, li, False))
	xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_DATE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_TRACKNUM)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_TITLE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_DURATION)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_GENRE)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_VIDEO_RATING)
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_EPISODE)
	xbmcplugin.endOfDirectory(__handle__)
	xbmcplugin.setContent(int(sys.argv[1]), 'series')
	xbmcplugin.setPluginCategory(int(sys.argv[1]), params['title'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Series - Now on TV - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series_now_on_tv(params):
	load_series('{}/series/now-on-tv', params['api_key'], params['title'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Series - Top Rated - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series_top_rated(params):
	load_series('{}/series/top-rated', params['api_key'], params['title'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Series - Popular - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series_popular(params):
	load_series('{}/series/popular', params['api_key'], params['title'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Series - Search - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series_search(params, search):
	load_series('{}/series/search', params['api_key'], params['title'], search)

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Series - New - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series_new(params):
	load_series('{}/series/new', params['api_key'], params['title'])

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Series - Browse - Groups - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series_browse_groups(params):
	groups = erdplugintools.post_json('{}/series/groups'.format(api), { 'api_key': params['api_key'] }, useragent)['data']
	for group in groups:
		erdplugintools.add_simple_item(action = action_series_browse_group, title = group['group_name'], icon = get_image(image_series_browse), thumbnail = get_image(image_series_browse_big), poster =  get_image(image_series_browse_big), fanart = get_image(image_fanart), folder = True, api_key = params['api_key'], group = group['id'])
	erdplugintools.close_item_list()

# ---------------------------------------------------------------------------------------------------------
#  Load Addon Series - Browse - Group['id'] - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def load_series_browse_group(params):
	load_series('{}/series/browse/' + params['group'], params['api_key'], params['title'])

# ---------------------------------------------------------------------------------------------------------
#  Account Information - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def account_information(params):
	account = erdplugintools.post_json('{}/account'.format(api), { 'api_key': params['api_key'] }, useragent)['data']
	xbmcgui.Dialog().ok(__addon_name__, addon.getLocalizedString(32204).format(account['name'], erdplugintools.get_date(account['start']), erdplugintools.get_date(account['end']), erdplugintools.get_subscription_type(account['subscription_type'])))

# ---------------------------------------------------------------------------------------------------------
#  Router function - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def router():
	params = erdplugintools.get_params()
	if params:
		# Movies
		if params['action'] == action_main_m:
			load_addon_movies_menu(params)
		# Series
		elif params['action'] == action_main_s:
			load_addon_series_menu(params)
		# Account
		elif params['action'] == action_main_a:
			account_information(params)
		# Movies - Now in Theaters
		elif params['action'] == action_movies_now_playing:
			load_movies_now_in_theaters(params)
		# Movies - Top Rated
		elif params['action'] == action_movies_top_rated:
			load_movies_top_rated(params)
		# Movies - Popular
		elif params['action'] == action_movies_popular:
			load_movies_popular(params)
		# Movies - Browse
		elif params['action'] == action_movies_browse:
			load_movies_browse_groups(params)
		# Movies - Browse Group
		elif params['action'] == action_movies_browse_group:
			load_movies_browse_group(params)
		# Movies - Search
		elif params['action'] == action_movies_find:
			load_movies_search(params['api_key'], erdplugintools.keyboard_input('', addon.getLocalizedString(32008)))
		# Movies - New
		elif params['action'] == action_movies_new:
			load_movies_new(params)
		# Series - Now on TV
		elif params['action'] == action_series_now_on_tv:
			load_series_now_on_tv(params)
		# Series - Top Rated
		elif params['action'] == action_series_top_rated:
			load_series_top_rated(params)
		# Series - Top Rated
		elif params['action'] == action_series_popular:
			load_series_popular(params)
		# Series - Browse
		elif params['action'] == action_series_browse:
			load_series_browse_groups(params)
		# Series - Browse Group
		elif params['action'] == action_series_browse_group:
			load_series_browse_group(params)
		# Series - Search
		elif params['action'] == action_series_find:
			load_series_search(params, erdplugintools.keyboard_input('', addon.getLocalizedString(32008)))
		# Series - New
		elif params['action'] == action_series_new:
			load_series_new(params)
		# Series - Seasons
		elif params['action'] == action_series_browse_serie:
			load_series_seasons(params)
		# Series - Episodes
		elif params['action'] == action_series_browse_episodes:
			load_series_episodes(params)
		else:
			# If the provided paramstring does not contain a supported action
			# we raise an exception. This helps to catch coding errors,
			# e.g. typos in action names.
			raise ValueError('Invalid action: {}!'.format(params['action']))
	else:
		# If the plugin is called from Kodi UI without any parameters,
		# display the main menu items
		load_addon_main_menu(params)

# ---------------------------------------------------------------------------------------------------------
#  Call the router function - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	router()