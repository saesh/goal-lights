import cv2
import numpy as np

import requests as req
import json
import time

from util import Util

class GoalWatcher:
    def __init__(self, watcher_conf):
        self._settings = watcher_conf
        self.previous_img = None

    def process(self, screen):
        arr = np.array(screen)
        arr = arr.astype(np.uint8)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        blurred = cv2.medianBlur(gray, 5)
        threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 4)
        img = threshold.copy()

        if self.previous_img is None:
            self.previous_img = img
            return

        comp_result = cv2.compare(self.previous_img, img, cv2.CMP_NE)
        changed_pixels = cv2.countNonZero(comp_result)

        percent = round((changed_pixels / (img.size * 1.0)), 2)

        #print "change in pixels: {percent}%, current threshold for goal detection: {threshold}".format(percent=percent, threshold=self._settings["change_threshold"])

        if percent > self._settings["change_threshold"]:
            print "Goal detected!"
            average_color_per_row = np.average(arr, axis=0)
            average_color = np.average(average_color_per_row, axis=0)

            try:
                import copy
                damp_factor = 0.3
                rgb = [int(average_color[2] * (1 - damp_factor)),
                       int(average_color[1] * (1 - damp_factor)),
                       int(average_color[0] * (1 - damp_factor))]

                settings_copy = copy.deepcopy(self._settings)

                for index, request in enumerate(settings_copy["requests"]):
                    for payload, value in request["payloads"].items():
                        if value == "RGB_PLACEHOLDER":
                            settings_copy["requests"][index]["payloads"][
                                payload] = rgb

                    if request["method"].upper() == "POST":
                        api_call = req.post(
                            request["endpoint"],
                            data=json.dumps(request["payloads"]))
                    if request["method"].upper() == "GET":
                        api_call = req.get(
                            request["endpoint"],
                            data=request["payloads"])

                    if api_call:
                        Util.log("RESTful response %s" % api_call)

                    time.sleep(float(request["delay"]))
            except Exception, exc:
                 Util.log("Error firing an event for %s, event: %s" % (self._settings["name"], exc))

        self.previous_img = img
