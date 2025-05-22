### ---- ### Centralized Iris Launch hub ### ---- ###






import os
import json
from ext.config_loader import main_config
from ext._logger import logger, MEMORY_LEVEL, WARN_LEVEL, SYSTEM_LEVEL
from pathlib import Path
from user import SessionManager
from model_manager import ModelManager
from routing import Router




#--# declarations
config = main_config
model_config = config["model"]
session = SessionManager()




#-# functions



# function for reading/loading configuration file 


# function for initializing iris
def initialize_iris(args):

    session.user_login(args.profile)

    #loading models
    ModelManager.load_model("conscious_model")
    #checking whether sys calls for lazy_submodel:
    if not args.lazy_submodel:
        ModelManager.load_model("subconscious_model")

    
    return {
        "model manager": ModelManager,
        "session": session,
        "router": lambda prompt: Router.route(prompt, ModelManager)
    }