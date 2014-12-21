download_pinboard
=================

Download your pinboard bookmarks as webloc files with Mac OS X tags. By default, the script will only download new bookmarks.

## Setup

Create a settings file

    `cp settings.py{.example,}`

with the following information

    _PINBOARD_TOKEN = 'YOUR TOKEN HERE'
    _SAVE_PATH = HOME + '/Bookmarks/'

In settings.py set your Pinboard token and the path where you want your bookmarks to be saved. Your token can be found at [https://pinboard.in/settings/password](https://pinboard.in/settings/password). The path must exist where you save your bookmarks and must end with a traling /.


## Running the script

To start the script, you can simply do

    python main.py

### Optional arguments

`-v, --verbose` Shows output as stdout  
`--reset [optional num of days]` Resets your last updated time. If you don't specifiy a number, it will reset to 999 days.  
`-t` Filters the bookmarks you want to download by tag. You can pass multiple -t tags, but no more than 3. Multiple tags are AND not OR  
`--skip-update` Lets you bypass the last downloaded time. Nice for redownloading everything.  
