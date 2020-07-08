# PcPhoneShare
This software package consists of 3 seperate pieces of software and can be used to easily share files from any local network computer system to any other local network computer system.
This includes, but is not limited to, desktops, android smartphones, servers and notebooks. Every device that can run either Python 3 or Android is able to use this system.

Therefore this system contains a client application, a server application as well as an Android application.


This project is mainly driven by the lack of easy to use, free, open source file sharing applications across systems. For example cloud setups like Nextcloud are much more powerful and should be used when possible, but their setup is usually not 'Download and run'.
This project aims to fill that void.

An additional bonus of this software package is, that you can either run the server on a seperate device in your network, like a Raspberry Pi, or directly on you desktop pc through activating server mode.
With a seperate device that is always running, buffering of files is possible, because the server will store the files until the intended target comes back online and connects to it.
When using the server mode of the client, this buffering is only possible when the pc is running.


Currently the dektop client and the server are in development and the Android application will follow as soon as these two are usable.

##Important information: At this stage, everything is sent in plain text through the network. There is no encryption going on, so that you should not send critial file via this system.