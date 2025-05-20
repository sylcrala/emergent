### ----- User Authentication Module ----- ###
#
#
# handles user authentication, checking whether a user exists in the user bank and handles login/logout
#
#
#--#
import os
import json

import uuid
import getpass
from core.ext._logger import logger, USER_LEVEL
from core.ext.config_loader import load_config

userbank_path = load_config()["security"]["authentication"]["bank_path"]

class UserSession:
    def __init__(self):
        self.active_user = {}
        self.userbank = {}
        self.userbank_path = userbank_path

        if not self.userbank:
            logger.log(USER_LEVEL, "[User Authentication] No user bank found. Creating a new one.")
            self.userbank = {}
            self.save_userbank()
        else:
            logger.log(USER_LEVEL, "[User Authentication] User bank found. Loading existing user bank.")
            self.userbank = self.load_userbank()

        self.user_login(self.prompt_username(), self.prompt_password())

        if self.user_login(self.prompt_username(), self.prompt_password()) == True:
            logger.log(USER_LEVEL, f"[User Authentication] User {self.active_user['username']} logged in successfully.")
            #redirect to main chat loop here#
        else:
            logger.log(USER_LEVEL, f"[User Authentication] User {self.active_user['username']} login failed.")
            self.user_logout()



    #--# user auth bank verify, load, save func #--#
    def load_userbank(self):
        if not os.path.exists(userbank_path):
            with open(userbank_path, "w") as f:
                json.dump({}, f)
        with open(userbank_path, "r") as f:
            return json.load(f)

    def save_userbank(self):
        with open(userbank_path, "w") as f:
            json.dump(self.userbank, f, indent=2)
            logger.log(USER_LEVEL, f"[User Authentication] User bank saved to {userbank_path}")
        logger.log(USER_LEVEL, f"[User Authentication] User bank loaded from {userbank_path}")
        return self.userbank
    #--#


    #--# generate user id func #--#
    def generate_user_id(self): 
        return str(uuid.uuid4())
    #--#


    #--# username and password prompt funcs #--#
    def prompt_username(self):
        username = input("Enter your username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return self.prompt_username()
        return username
    
    def prompt_password(self):
        password = getpass.getpass("Enter your password: ").strip()
        if not password:
            print("Password cannot be empty.")
            return self.prompt_password()
        return password
    #--#


    #--# login/logout funcs #--#
    def check_user_exists(self, username):
        if username in self.userbank:
            return True
        else:
            return False

    def user_login(self, username, password):
        if self.check_user_exists(self, username=username) == True:
            if self.userbank[username]["password"] == password:
                self.active_user = self.userbank[username]
                print(f"Welcome back, {username}!")
                logger.log(USER_LEVEL, f"[User Authentication] User {username} logged in successfully.")
                return True
            else:
                print("Incorrect password.")
                logger.log(USER_LEVEL, f"[User Authentication] User {username} login failed: Incorrect password.")
                return False
        elif self.check_user_exists(self, username=username) == False:
            print("User not found, creating new user. Welcome to Iris!")
            logger.log(USER_LEVEL, f"[User Authentication] User {username} not found, creating new user.")
            self.create_user(username, password)
            return True 
        
    def user_logout(self): 
        if self.active_user:
            print(f"Goodbye, {self.active_user['username']}!")
            logger.log(USER_LEVEL, f"[User Authentication] User {self.active_user['username']} logged out.")
            self.active_user = {}
        else:
            logger.log(USER_LEVEL, "[User Authentication] No user is currently logged in.")


