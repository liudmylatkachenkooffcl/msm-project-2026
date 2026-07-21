#loremipsum XDD
import db_utils
import json
class User:
    def __init__(self):
        self.username = None
        self.user_id = ""
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        self.profile_pic = None
        self.bio = ""
        self.is_active = True
        self.created = None
        self.is_moderator = False

    def pack_in_json(self): #welp, I'm gonna start with the hardest one XDD
        json_dict = {
            "user_id":self.user_id






        }
