#-------------------------------------------------------------#
# -*- coding: utf-8 -*-										  #
#-------------------------------------------------------------#
# IPTV-Tools.com											  #
# Copyright 2021 (c) ERDesigns								  #
#															  #
# Author: Ernst Reidinga 									  #
# Email: contact@iptv-tools.com 							  #
#-------------------------------------------------------------#
# Changelog:												  #
# 1.0.0														  #
# - First Release											  #
# 2.0.1														  #
# - Second Release 											  #
#-------------------------------------------------------------#
# ERDesigns Plugin Tools Unit							 	  #
#-------------------------------------------------------------#

import xbmc
import xbmcplugin
import xbmcaddon
import xbmcgui

import os
import sys
import urllib
import datetime
import re
import json
import shutil
import zipfile
import base64
import time
import xbmcvfs

from urllib import request

# Enable application logging
__application_log__ = True
# Enable for debug logging
__debug_log__ = True

# ---------------------------------------------------------------------------------------------------------
#  Parse string and extracts first match as a string - Return value: String
# ---------------------------------------------------------------------------------------------------------
def find_single_match(text,pattern):
	result = ''
	try:    
		matches = re.findall(pattern, text, flags = re.DOTALL)
		result = matches[0]
	except:
		result = ''
	return result

# ---------------------------------------------------------------------------------------------------------
#  Set globals for Plugin Tools
# ---------------------------------------------------------------------------------------------------------
f = open(os.path.join(os.path.dirname(__file__) , 'addon.xml'))
fdata = f.read()
f.close()

self_id = find_single_match(fdata, 'id="([^"]+)"')
if self_id == '':
    self_id = find_single_match(fdata, 'id=\'([^\']+)\'')

__addon_id__ = self_id
__settings__ = xbmcaddon.Addon(id = self_id)
__language__ = __settings__.getLocalizedString

# ---------------------------------------------------------------------------------------------------------
#  Get addon id - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_addon_id():
    return __addon_id__

# ---------------------------------------------------------------------------------------------------------
#  Write to log - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def log(message):
    if __application_log__:
        xbmc.log(msg = message, level = xbmc.LOGINFO)

# ---------------------------------------------------------------------------------------------------------
#  Write debug message to log - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def debug_log(message):
    if __debug_log__:
        xbmc.log(msg = 'DEBUG LOG FOR: [{}] - LOG: {}'.format(__addon_id__, message), level = xbmc.LOGDEBUG)

# ---------------------------------------------------------------------------------------------------------
#  Get setting from "this" addon - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_local_setting(name):
    debug_log('Get local setting: {}'.format(name))
    return __settings__.getSetting(name)

# ---------------------------------------------------------------------------------------------------------
#  Get setting from "this" addon - Return value: Bool
# ---------------------------------------------------------------------------------------------------------
def get_local_setting_bool(name):
    debug_log('Get local setting Bool: {}'.format(name))
    return __settings__.getSetting(name) == 'true'

# ---------------------------------------------------------------------------------------------------------
#  Set setting for "this" addon - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def set_local_setting(name, value):
	debug_log('Set local setting: {} - {}'.format(name, value))
	__settings__.setSetting(name, value)

# ---------------------------------------------------------------------------------------------------------
#  Get setting from "other" - "NOT This" addon - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_remote_setting(addon, name):
	debug_log('Get remote setting: {}'.format(name))
	remote_addon = xbmcaddon.Addon(id = addon)
	return remote_addon.getSetting(name)

# ---------------------------------------------------------------------------------------------------------
#  Set setting for "other" - "NOT This" addon - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def set_remote_setting(addon, name, value):
	debug_log('Set remote setting: {} - {}'.format(name, value))
	remote_addon = xbmcaddon.Addon(id = addon)
	remote_addon.setSetting(name, value)

# ---------------------------------------------------------------------------------------------------------
#  Open Settings dialog - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def open_settings_dialog():
	debug_log('Open settings dialog')
	__settings__.openSettings()

# ---------------------------------------------------------------------------------------------------------
#  POST HTTP REQUEST - Return value: JSON Object
# ---------------------------------------------------------------------------------------------------------
def post_json(url, data, useragent = ''):
	req = request.Request(url, method = 'POST')
	req.add_header('Accept', 'application/json')
	req.add_header('Content-Type', 'application/json')
	if useragent == '':
		req.add_header('User-Agent', __addon_id__)
	else:
		req.add_header('User-Agent', useragent)
	data = json.dumps(data)
	data = str(data)
	data = data.encode('utf-8')
	response = request.urlopen(req, data = data)
	respdata = response.read()
	try:
		jdata = json.loads(respdata.decode('utf8'))
	except json.JSONDecodeError:
		debug_log('Error decoding JSON!')
		# Ignore error
		pass
	response.close()
	if jdata:
		return jdata
	else:
		return None

# ---------------------------------------------------------------------------------------------------------
#  Get Subscription Type - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_subscription_type(val):
	subscriptions = {
		0: 'Enthousiast',
		1: 'Professional',
		2: 'Pro +'
	}
	return subscriptions.get(val, __settings__.getLocalizedString(32205))

# ---------------------------------------------------------------------------------------------------------
#  Get Playlist Type - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_playlist_type(val):
	playlists = {
		0: 'Xtream-API & M3U',
		1: 'Xtream-API',
		2: 'M3U'
	}
	return playlists.get(val, __settings__.getLocalizedString(32206))

# ---------------------------------------------------------------------------------------------------------
#  Get Date - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_date(val):
	if not val or val is None:
		return 'Unlimited'
	else:
		return datetime.datetime.fromtimestamp(val).strftime(__settings__.getLocalizedString(32298))

# ---------------------------------------------------------------------------------------------------------
#  Get Genres - Return value: List of strings
# ---------------------------------------------------------------------------------------------------------
def get_genres(genres):
	result = []
	for genre in genres:
		result.append(genre['name'])
	return result

# ---------------------------------------------------------------------------------------------------------
#  Get Countries - Return value: List of strings
# ---------------------------------------------------------------------------------------------------------
def get_countries(countries):
	result = []
	for country in countries:
		result.append(country['name'])
	return result

# ---------------------------------------------------------------------------------------------------------
#  Get Year - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_year(date):
	return ''

# ---------------------------------------------------------------------------------------------------------
#  Get Cast - Return value: List of Dictionaries
# ---------------------------------------------------------------------------------------------------------
def get_cast(cast):
	result = []
	for person in cast:
		result.append({ 'name': person['name'], 'role': person['character'], 'thumbnail': 'http://tmdb-img.iptv-tools.com{}'.format(person['profile_path']), 'order': person['cast_id'] })
	return result

# ---------------------------------------------------------------------------------------------------------
#  Get Cast Series - Return value: List of Dictionaries
# ---------------------------------------------------------------------------------------------------------
def get_cast_series(cast):
	result = []
	for person in cast:
		result.append({ 'name': person['name'], 'role': person['character'], 'thumbnail': 'http://tmdb-img.iptv-tools.com{}'.format(person['profile_path']), 'order': person['order'] })
	return result

# ---------------------------------------------------------------------------------------------------------
#  Get Directors - Return value: List of strings
# ---------------------------------------------------------------------------------------------------------
def get_directors(crew):
	if not type(crew) == list:
		return ''
	result = []
	for person in crew:
		if 'Director' in person['job']:
			result.append(person['name'])
	return result

# ---------------------------------------------------------------------------------------------------------
#  Get Writers - Return value: List of strings
# ---------------------------------------------------------------------------------------------------------
def get_writers(crew):
	if not type(crew) == list:
		return ''
	result = []
	for person in crew:
		if 'Writer' in person['job']:
			result.append(person['name'])
	return result

# ---------------------------------------------------------------------------------------------------------
#  Get Studios - Return value: List of strings
# ---------------------------------------------------------------------------------------------------------
def get_studios(studios):
	if not type(studios) == list:
		return ''
	result = []
	for studio in studios:
		result.append(studio['name'])
	return result

# ---------------------------------------------------------------------------------------------------------
#  Get Tags (Keywords) - Return value: List of strings
# ---------------------------------------------------------------------------------------------------------
def get_tags(keywords):
	if not type(keywords) == list:
		return ''
	result = []
	for keyword in keywords:
		result.append(keyword['name'])
	return result

# ---------------------------------------------------------------------------------------------------------
#  Get Trailer - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_trailer(videos):
	if not type(videos) == list:
		return ''
	result = ''
	for video in videos:
		if video['site'] == 'Youtube' and video['type'] == 'Trailer':
			result = 'http://www.youtube.com/watch?v={}'.format(video['key'])
	return result

# ---------------------------------------------------------------------------------------------------------
#  Get String - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_string(string):
	if not string or not type(string) == str:
		return ''
	return string

# ---------------------------------------------------------------------------------------------------------
#  Get Runtime - Return value: Number
# ---------------------------------------------------------------------------------------------------------
def get_runtime(runtime):
	if not runtime or not type(runtime) == int:
		return 0
	return int(runtime) * 60

# ---------------------------------------------------------------------------------------------------------
#  Get Episode Runtime - Return value: Number
# ---------------------------------------------------------------------------------------------------------
def get_episode_runtime(runtime):
	if not runtime or not type(runtime) == list:
		return 0
	return int(runtime[0]) * 60

# ---------------------------------------------------------------------------------------------------------
#  Play resolved URL - Return value: Bool
# ---------------------------------------------------------------------------------------------------------
def play_resolved_url(url):
	debug_log('Play resolved url: [URL]: {}'.format(url))
	li = xbmcgui.ListItem(path = url)
	li.setProperty('IsPlayable', 'true')
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)

# ---------------------------------------------------------------------------------------------------------
#  Kodi keyboard input dialog - Return value: String
# ---------------------------------------------------------------------------------------------------------
def keyboard_input(default = '', title = '', hidden = False):
	debug_log('Keyboard input {} - title: {}'.format(default, title))
	kb = xbmc.Keyboard(default, title, hidden)
	kb.doModal()
	if (kb.isConfirmed()):
		return kb.getText()
	else:
		return ''

# ---------------------------------------------------------------------------------------------------------
#  Kodi OK Dialog Message - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def message_ok_dialog(text1, text2 = '', text3 = ''):
	debug_log('Message OK Dialog [Text1]: {} - [Text2]: {} - [Text3]: {}'.format(text1, text2, text3))
	if text3 == '':
		xbmcgui.Dialog().ok(text1 , text2)
	elif text2 == '':
			xbmcgui.Dialog().ok('', text1)
	else:
		xbmcgui.Dialog().ok(text1, text2, text3)

# ---------------------------------------------------------------------------------------------------------
#  Kodi YES/NO Dialog Message - Return value: Bool
# ---------------------------------------------------------------------------------------------------------
def message_yesno_dialog(text1, text2 = '', text3 = ''):
	debug_log('Message YES/NO Dialog [Text1]: {} - [Text2]: {} - [Text3]: {}'.format(text1, text2, text3))
	if text3 == '':
		return xbmcgui.Dialog().yesno(text1, text2)
	elif text2 == '':
		return xbmcgui.Dialog().yesno('', text1 )
	else:
		return xbmcgui.Dialog().yesno(text1, text2, text3)

# ---------------------------------------------------------------------------------------------------------
#  Kodi Selection Dialog - Return value: Selected Item
# ---------------------------------------------------------------------------------------------------------
def selection_dialog(options, title = ''):
	debug_log('Selection Dialog [Title]: {} - [List]: {}'.format(title, repr(options)))
	seldlg = xbmcgui.Dialog()
	return seldlg.select(title, options)

# ---------------------------------------------------------------------------------------------------------
#  Kodi Notification - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def show_notification(title, message, icon = ''):
	debug_log('Show Notification [Title]: {} - [Message]: {} - [Icon]: {}'.format(title, message, icon))
	xbmc.executebuiltin((u'XBMC.Notification("{}", "{}", 2000, "{}")'.format(title, message, icon)))

# ---------------------------------------------------------------------------------------------------------
#  Get parameters from url - Return value: List
# ---------------------------------------------------------------------------------------------------------
def get_params():
	param_str = sys.argv[2]
	debug_log('Get Parameters: {}'.format(param_str))
	commands = {}
	if param_str:
		split_commands = param_str[param_str.find('?') + 1:].split('&')
		for command in split_commands:
			if len(command) > 0:
				if '=' in command:
					split_command = command.split('=')
					key = split_command[0]
					value = urllib.parse.unquote_plus(split_command[1])
					commands[key] = value
				else:
					commands[command] = ''
	return commands

# ---------------------------------------------------------------------------------------------------------
#  Get localized string - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_localized_string(code):
	debug_log('Get Localized string code: {}'.format(code))
	res = __language__(code)
	try:
		res = res.encode('utf-8')
	except:
		pass
	return res

# ---------------------------------------------------------------------------------------------------------
#  Get runtime path - Return value: String
# ---------------------------------------------------------------------------------------------------------
def get_runtime_path():
	debug_log('Get runtime path')
	return xbmcvfs.translatePath(__settings__.getAddonInfo('Path'))

# ---------------------------------------------------------------------------------------------------------
#  Add simple item to list - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def add_simple_item(action = '', title = '', plot = '', url = '', thumbnail = '', icon = '', poster = '', fanart = '', category = '', page = '', info_labels = None, context_menu_items = [] , isPlayable = False , folder = True, stream_video = None, stream_audio = None, api_key = '', group = 0):
	debug_log('Add item to list: [Action]: {} - [Title]: {} - [URL]: {}'.format(action, title, url))
	# Create list item
	li = xbmcgui.ListItem(title)
	li.setArt({ 'icon': icon, 'thumbnail': thumbnail, 'poster': poster })
	# Set title filename and plot
	if info_labels is None:
		info_labels = {'Title': title, 'FileName': title, 'Plot': plot }
	li.setInfo('video', info_labels)
	# Add video codec information
	if not stream_video is None:
		li.addStreamInfo('video', stream_video)
	# Add audio codec information
	if not stream_audio is None:
		li.addStreamInfo('audio', stream_audio)
	# Set poster
	if not poster == '':
		li.setArt({'poster': poster})
	# Set context menu items
	if len(context_menu_items) > 0:
		li.addContextMenuItems(context_menu_items, replaceItems = False)
	# Set fanart
	if not fanart == '':
		li.setProperty('fanart_image', fanart)
		xbmcplugin.setPluginFanart(int(sys.argv[1]), fanart)
	# Handle
	handle = int(sys.argv[1])
	# Set playable
	if url.startswith("plugin://"):
		li.setProperty('IsPlayable', 'true')
		xbmcplugin.addDirectoryItem(handle = handle, url = url, listitem = li, isFolder = folder)
	elif isPlayable:
		li.setProperty('Video', 'true')
		li.setProperty('IsPlayable', 'true')
		itemurl = '{0}?action={1}&title={2}&url={3}&thumbnail={4}&fanart={5}&plot={6}&category={7}&page={8}&api_key={9}&group={10}'.format(sys.argv[0], action, urllib.parse.quote_plus(title), urllib.parse.quote_plus(url), urllib.parse.quote_plus(thumbnail), urllib.parse.quote_plus(fanart), urllib.parse.quote_plus(plot), urllib.parse.quote_plus(category), urllib.parse.quote_plus(page), api_key, group)
		xbmcplugin.addDirectoryItem(handle = handle, url = itemurl, listitem = li, isFolder = folder)
	else:
		itemurl = '{0}?action={1}&title={2}&url={3}&thumbnail={4}&fanart={5}&plot={6}&category={7}&page={8}&api_key={9}&group={10}'.format(sys.argv[0], action, urllib.parse.quote_plus(title), urllib.parse.quote_plus(url), urllib.parse.quote_plus(thumbnail), urllib.parse.quote_plus(fanart), urllib.parse.quote_plus(plot), urllib.parse.quote_plus(category), urllib.parse.quote_plus(page), api_key, group)
		xbmcplugin.addDirectoryItem(handle = handle, url = itemurl, listitem = li, isFolder = folder)

# ---------------------------------------------------------------------------------------------------------
#  Refresh items in container - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def refresh_items():
	debug_log('Refresh items in container')
	xbmc.executebuiltin('Container.Refresh')

# ---------------------------------------------------------------------------------------------------------
#  Close item list - Return value: No return value
# ---------------------------------------------------------------------------------------------------------
def close_item_list():
	debug_log('Close item list')
	xbmcplugin.endOfDirectory(handle = int(sys.argv[1]), succeeded = True)
