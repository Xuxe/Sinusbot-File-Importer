# Sinusbot - File Importer
A CLI Tool to Import audio files via the HTTP API. Written in Python.

Usage:

Non SSL -> ./sinusbot_uploader.py 123.124.125.1 8087 admin foobar /myfolder
SSL -> ./sinusbot_uploader.py 123.124.125.1 8087 admin foobar /myfolder SSL

Result:

xuxe@sinus:~$ sudo ./sinusbot_uploader.py 127.0.0.1 8087 admin foobar /home/xuxe/test/
Success Authenticated!
Success uploaded: /home/xuxe/test/Glowworm+-+Periphescence.mp3
Success uploaded: /home/xuxe/test/Death+Grips+-+Come+Up+and+Get+Me.mp3
Success uploaded: /home/xuxe/test/The+Echelon+Effect+-+Your+First+Light+My+Eventide.mp3


SUPPORTED FILE TYPES: extensions=['mp3', 'mp4', 'wav', '3gp'] - i have added at the moment only mp3, mp4, wav and 3gp. If you need others you can add your own or report it and i will add it! 

I tested it only on Python 2.7 Debian & Ubuntu. 

If you encounter an issue open a Report here: https://github.com/Xuxe/Sinusbot-File-Importer/issues/new - Please apply the backtrace! :)