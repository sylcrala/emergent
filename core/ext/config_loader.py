import json
import os

#--# defining config path via path expanduser for portability #--#
CONFIG = os.path.expanduser('/home/sym/VSC/iris/core/config.json')




#--# function for reading/loading configuration file #--#
def load_config():
    with open(CONFIG, "r") as f:
        return json.load(f)
