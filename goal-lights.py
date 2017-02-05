import time
import sys
import os
import itertools
from util import Util
from goalwatcher import GoalWatcher
import yaml

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

def main():
    config_file = open('settings.yaml')
    settings = yaml.safe_load(config_file)
    config_file.close()

    spinner = itertools.cycle(['-', '/', '|', '\\'])

    watcher_list = [GoalWatcher(w) for w in settings["watchers"]]

    window = Util.find_window_by_title(settings["window_title"])

    if window is not None:
        window = Util.resize_capture_area(window, settings)

    while True:

        if window is None:
            sys.stdout.write("Waiting for window ... " + spinner.next() + "\r")
            sys.stdout.flush()
            window = Util.find_window_by_title(settings["window_title"])
            if window is not None:
                window = Util.resize_capture_area(window, settings)
            time.sleep(0.3)
            continue

        time.sleep(float(settings["scan_interval"]))

        screen = Util.screenshot(window)

        if not screen.any():
            continue

        for watch in watcher_list:
            watch.process(screen)

if __name__ == '__main__':
    main()
