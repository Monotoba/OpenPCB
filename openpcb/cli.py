
import argparse, json, sys
def main():
    ap = argparse.ArgumentParser(prog="onestop-pcb")
    ap.add_argument("--echo", help="echo a message")
    args = ap.parse_args()
    if args.echo:
        print(args.echo)
    else:
        print("OneStop PCB CLI scaffold. See docs/SPEC-1-OneStopPCB.md")
