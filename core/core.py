### ---- ### Centralized Iris Launch hub ### ---- ###






import os
import json
from core._logger import logger, MEMORY_LEVEL, WARN_LEVEL, SYSTEM_LEVEL
from pathlib import Path





#--# declarations



#-# functions

# function for reading/loading configuration file 
def load_config(config_path="/iris/config/config.json"):
    with open(config_path, "r") as f:
        return json.load(f)

# function for launching the CLI
def launch_cli(model_config):
    from iris.core.cli.main import run_cli
    run_cli(model_config)
    # CREATE CLI DIRECTORY AND SCRITPS ***************

# function for launching the GUI
def launch_gui(model_config):
    from iris.core.gui.qt_gui import iris_gui
    app = iris_gui(model_config)
    app.run()
    # CREATE GUI DIRECTORY AND SCRITPS ***************

# function for initializing iris
def initialize_iris(gui: bool = False, lazy_submodel: bool = False):
    config = load_config()
    model_config = config["model"]


    #checking whether sys calls for lazy_submodel:
    if lazy_submodel:
        model_config["subconscious"]["enabled"] = False

    
    if gui or config["settings"].get("default_to_gui", False):
        launch_gui(model_config)
    else:
        launch_cli(model_config)