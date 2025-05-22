### ---- ### Iris Entry Point ### ---- ###
## 
#
# Main entry point for launching and initializing Iris.
#
# Invoked via the GUI or a command line interface.




import argparse
from core import initialize_iris
from core.parser import parse_args 




#NEED TO TIE OTHER MODULES INTO THIS, THIS REPLACES OLD MAIN.PY



def main():
    args = parse_args()

    
    initialize_iris(gui=args.gui, lazy_submodel=args.lazy_submodel)

if __name__ == "__main__":
    main()
