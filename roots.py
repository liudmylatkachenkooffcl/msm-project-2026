#loremipsum XDD
import db_utils
import json
import datetime
from flask import Flask, request
import os
import uuid
class User:
    def __init__(self):
        self.username = None
        self.user_id = ""
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        self.profile_pic = "" #is in link, we're taking it from folder from server
        self.bio = ""
        self.is_active = True
        self.created = None #datetime format
        self.is_moderator = False

    def dict_public(self): #Contains no password and email. Here is only publicly available data. Maybe I should remove is_active
        dict_public = {
            "user_id":self.user_id,
            "username":self.username,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "profile_pic":self.profile_pic,
            "bio":self.bio,
            "is_active":self.is_active,
            "created":self.created,
            "is_moderator":self.is_moderator
        }
        return dict_public

    def pack_in_json(pack_dict, self): #just dict to JSON, maybe used for every dict
        return json.dumps(pack_dict)

    def import_from_db_public(self, user_id): #we get everything besides email and password.
        imported_data = db_utils.recall_user(user_id)
        self.username = imported_data[1]
        self.first_name = imported_data[2]
        self.last_name = imported_data[3]
        self.profile_pic = imported_data[4]
        self.bio = imported_data[5]
        self.created = imported_data[6]
        #add maybe some message to console with "[SUCCESS]User [user_id] data was recalled successfully"

    def log_out(self):
        self.username = None
        self.user_id = ""
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        self.profile_pic = ""  # is in link, we're taking it from folder from server
        self.bio = ""
        self.is_active = True
        self.created = None  # datetime format
        self.is_moderator = False
        #message of logout in console

    def import_from_db_private(self, user_id):
        imported_data_private = db_utils.recall_user(user_id) #do private recall in db, but idk is it safe...
