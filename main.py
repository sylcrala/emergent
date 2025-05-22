### ---- ### Iris Entry Point ### ---- ###
## 
#
# Main entry point for launching and initializing Iris.
#
# Invoked via the GUI or a command line interface.




import argparse
from core.core import initialize_iris
from core.parser import parse_args 
from core.ext._logger import logger, SYSTEM_LEVEL
from core.routing import Router






#NEED TO TIE OTHER MODULES INTO THIS, THIS REPLACES OLD MAIN.PY


def start_cli(route):
    print("Iris is starting...\n\nSay 'bye iris' or 'exit' to shut down.\n\n")

    while True:
        user_input = input("You > \n").strip()

        if user_input.lower() in ("exit", "quit", "bye iris"):
            print("Iris shutting down... see you later! ")
            logger.log(SYSTEM_LEVEL, f"[SYSTEM SHUTDOWN]")
            break

        try:
            response = route(user_input)
            print(f"Iris > {response}\n")
            logger.log(SYSTEM_LEVEL, f"[Iris Response] - final - {response}")
        except Exception as e:
            print(f" error {e}")
            logger.log(SYSTEM_LEVEL, f"[Iris Response] - final - error {e}")







def main():
    args = parse_args()   
    mode = "GUI" if args.gui else "CLI" if args.cli else "no_mode"

    
    #beginning intialization
    environment = initialize_iris(args)


    if mode == "CLI":
        start_cli(environment["router"])
    elif mode == "GUI":
        print("🧪 GUI mode not yet implemented.")
        # from gui import launch_gui
        # launch_gui(runtime)
    else:
        print("No mode specified, please use --cli or --gui")
        logger.log(SYSTEM_LEVEL, f"failed sys launch with no mode")

    

if __name__ == "__main__":
    main()
