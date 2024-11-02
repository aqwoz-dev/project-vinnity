import os, threading, socket
import server
import setup

class user:
    def __init__(self, username):
        self.username = setup.username
        self.token = setup.token