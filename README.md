# YouTitle - HexChat Addon #

> Deciphers YouTube URLs read on IRC, getting back the titles to you or, optionally, the whole channel.

Secondary features:
- Non-blocking HTTP requests.
- Avoiding useless public printing of title already sent by user with the YouTube URL.
- Handling HTML entities in title.

## Installation ##

For auto-loading, copy the script in your hexchat addon folder:

+ On Linux: ~/.config/hexchat/addons 
+ On other OS, find it!

Alternatively you can (un)load a script manually through:

The commands:
 
		/py load youtitle.py
		/py unload youtitle.py
 
 Or, the hexchat GUI: 
 
		Window > Plugins and Scripts.

## Configuration ##

* Printing YouTube titles on channel

Editing hexchat python addon configuration file, you can set the option to display deciphered title publicly on channel (otherwise, by default, the title is printed only for you on the window).

On Linux the configuration file path is: 

		~/.config/hexchat/addon_python.conf
		
On other OSes, for sure you'll find it easily!

Find the following line in the configuration file:

		youtitle.sending_msg = no

And set the value to yes.

## Downloading HexChat ##

If you don't know HexChat yet, this is an IRC client.

[Click here to download HexChat.](https://hexchat.github.io/downloads.html)

## Contact ##

hakim.hexchat 
[[[a t]]] gmail

> Hakim HADJ-DJILANI
