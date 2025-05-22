### ---- ### independent config loader ### ---- ###

import json
import os



config_path="/home/sym/VSC/iris/config/"

def load_config(config_path):
    path = os.path.join(config_path,"config.json")
    with open(path, "r") as f:
        return json.load(f)

main_config = load_config(config_path)