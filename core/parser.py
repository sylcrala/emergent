### ---- ### Argument Parsing Module ### ---- ###


import argparse






def parse_args():
    parser = argparse.ArgumentParser(description="Launch Iris with configurable model loading.")
    parser.add_argument("--gui", action="store_true", help="Force GUI mode.")
    parser.add_argument("--lazy-submodel", action="store_true", help="Do not load subconscious model at startup.")
    return parser.parse_args()
