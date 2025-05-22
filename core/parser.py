### ---- ### Argument Parsing Module ### ---- ###


import argparse






def parse_args():
    parser = argparse.ArgumentParser(description="Launch Iris with configurable model loading.")
    parser.add_argument("--cli", action="store_true", help="Force CLI mode.")
    parser.add_argument("--gui", action="store_true", help="Force GUI mode.")
    parser.add_argument("--lazy-submodel", action="store_true", help="Do not load subconscious model at startup.")
    parser.add_argument("--profile", type=str, default="default_cli", help="Selected User Profile")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging in current mode.")
    parser.add_argument("--fallbck", type=str, default="no_mode", help="No mode selected.")
    return parser.parse_args()
