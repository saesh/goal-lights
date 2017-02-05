# goal-lights

Let your IoT lights flash in your team colors when you hit a goal in Rocket League.

## Attribution

goal-lights is heavily based on [lifelights](https://github.com/jjensn/lifelights) made by [jjensn](https://github.com/jjensn).
I had the idea to let my desk lamp flash whenever I hit a goal in Rocket League. When I saw jjsesn solution I had to adapt it
to work Rocket League. All I did was switch the watcher to detect changes in the goal display.
If you need flashing IoT lights for your game health bars head over to [lifelights](https://github.com/jjensn/lifelights)!

### Requirements
- Microsoft Windows
- Python 2.7 [(link)](https://www.python.org/ftp/python/2.7/python-2.7.msi)

### First time installation
- Clone this repository to a directory on your machine [(how-to)](https://help.github.com/desktop/guides/contributing/cloning-a-repository-from-github-to-github-desktop/)
- Start > cmd > cd to the source code directory
- ```pip install -r requirements.txt```

### Known limitations
- Not compatible with OSX
- Game must be run as "windowed fullscreen" or "windowed"
- API POST requests will always be in JSON format
- Rocket League scale factor has to be `1.0`

### Configuration details
Currently there is no input sanitation or verification, so drifting from the guidelines below will likely break the script.

- **window_title** (string): Title of the window that will be monitored
- **scan_interval** (float): Interval in seconds to take a screenshot

- **watchers**: List of different 'watchers' to calculate.
  - **name** (string): Common name of what you are monitoring. Used for logging but can be anything that makes sense to you
  - **change_threshold** (float): Percentage (0.0 - 1.0) that determines when a goal is detected and an API request should fire off. If there is change in 8% (0.08) of the pixels to the previous capture of the goal number it is considered to be a goal.
  - **requests**: List of RESTful events that should be fired when the ```change_threshold``` is passed
    - **endpoint** (string): API endpoint
    - **method** (string): POST or GET
    - **delay** (float): Interval in seconds to sleep after sending the API request. Use 0.0 for no delay.
    - **payloads**: Collection of keys/values to send to the API endpoint. Currently supports the following special values:
      - *RGB_PLACEHOLDER*: Array of an RGB color (is set automatically to your team color)

### Implementation

The program takes a screenshot of the left goal number, displayed on the top of the ingame screen. It cannot detect
if a game has started or not, so it will take screenshots even when you are in the menu. It compares the number of
changed pixels to the previous screenshot. If the percentage of changed pixels is higher than the configured threshold
it is considered to be a goal.

To compare the changed pixels the screenshot is converted to grayscale, blurred, a threshold is applied and compared to the previous image.

For example when you play and no goal is detected the images of the steps look like this:

![Background noise detected](http://i.imgur.com/nlST3y3.png)

When the number changes from 1 to 2 the difference is significant:

![Significant change in pixels](http://i.imgur.com/dMu8Taa.png)

If a goal is detected the average color of the screenshot is calculated to get the team color. Then an API call is made to
Home Assistant to trigger the lights.
