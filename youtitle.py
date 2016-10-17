#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

# Author: hakim.hexchat 
# 			[a t] gmail 

# to install: copy to ~/.config/hexchat/addons/ for autoloading
# to load in hexchat: /py load youtitle.py
# to unload: /py unload youtitle.py
# hexchat API doc: https://hexchat.readthedocs.org/en/2.9.6/script_python.html

import xchat  # @UnresolvedImport
import re
from urllib.request import urlopen
from html import unescape
from threading import Thread

__module_name__ = "youtitle"
__module_version__ = "1.1"
__module_description__ = "Deciphers YouTube URLs read on IRC, getting back the titles to you or the whole channel."

DEBUG = False
SENDING_MSG_PREF = xchat.strip(__module_name__)+".sending_msg"

# TODO: moving template string in conf file
# TODO: exclusive mode for sending_msg opt. on network basis
# TODO: exclusive mode, specifying networks on which the plugin parses youtube urls
# TODO: commands to edit config without going directly in config file.
# TODO: optionnally/defaulty ignoring youtube url posted by ignored user
# TODO: option to proxify the http requests
# TODO: command to enable/disable the sending msg option
# TODO: sending messages in the right ctxt (the one where the url was received)
# TODO: map for caching pairs of youtube link and title, avoiding two same requests in a row

def msg_containing_word_of_title(msg,title):
	MIN_WORD_LEN=5
	msg = msg.lower()
	for t_word in title.split(' '):
		if(len(t_word) >= MIN_WORD_LEN and msg.find(t_word.lower()) > -1):
			return True
	return False

def format_msg(nick, url, title):
	template = "%url, sent by %nick, has YouTube title: %title"
	return template.replace("%nick", nick).replace("%url", url).replace("%title", title)

def decipher_youtube_url(url, nick, orig_msg, dest=None):
	try:
		for line in urlopen(url):
			line = line.decode('utf-8')
			if line.startswith("<title>"):
				title = unescape(re.sub(r"^<title>(.*) - YouTube</title>.*",r"\1",line))
				msg = format_msg(nick,url,title)
				sending_msg = xchat.get_pluginpref(SENDING_MSG_PREF)
				not sending_msg and xchat.set_pluginpref(SENDING_MSG_PREF,"no") 
				DEBUG and xchat.prnt(__module_name__+": "+SENDING_MSG_PREF+": "+sending_msg)
				if sending_msg != None and dest != None and sending_msg == "yes" and not msg_containing_word_of_title(orig_msg,title):
					DEBUG and xchat.prnt(__module_name__+": sending msg")
					xchat.command("msg "+dest+" "+ msg)
				else:
					xchat.prnt(msg)
	except BaseException as e:
		xchat.prnt(__module_name__+" failed to decipher : "+url+" error: "+e.__str__())

def process_youtube_urls(msg, nick, dest=None):
	# TODO: do a findall() on word_eol and loop in the returned list to process all urls
	m = re.match("^.*(https?://(www.)?((youtube.com/)|(youtu.be/))[?&=a-zA-Z0-9_-]*).*$",xchat.strip(msg),re.I)
	if m != None:
		DEBUG and xchat.prnt("msg: "+xchat.strip(msg))
		url = m.group(1)
		DEBUG and xchat.prnt("url: "+url)
		task = Thread()
		def task_func():
			decipher_youtube_url(url,nick,msg,dest)
		task.run = task_func
		task.start()
	return xchat.EAT_NONE
	
def process_priv_msg(word, word_eol, userdata):
	nick = word[0]
	nick = nick[1:nick.find('!')] # word[0] format: ":nick!*@host"
	if(not word[2].startswith('#') and not word[2].startswith('&')): 
		# not a channel message
		process_youtube_urls(word_eol[0],nick)
	return xchat.EAT_NONE

def process_chan_msg(word, word_eol, userdata, priority):
	process_youtube_urls(word[1],word[0],xchat.get_info("channel"))
	return xchat.EAT_NONE
	
xchat.hook_print_attrs("Channel Message", process_chan_msg)
xchat.hook_print_attrs("Channel Msg Hilight", process_chan_msg)
xchat.hook_server("PRIVMSG", process_priv_msg)
xchat.hook_server("NOTICE", process_priv_msg)

xchat.prnt(__module_name__+" loaded")

xchat.hook_unload(lambda user_data : xchat.prnt(__module_name__+" unloaded"))
