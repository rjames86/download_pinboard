download_pinboard
=================

Download your Pinboard bookmarks as webloc files with Mac OS X tags.

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

By default, the script will only download new bookmarks from the last time the script was run.

### Optional arguments

`-v, --verbose` Shows output as stdout  
`--reset [optional num of days]` Resets your last updated time. If you don't specifiy a number, it will reset to 10000 days.  
`-t` Filters the bookmarks you want to download by tag. You can pass multiple -t tags, but no more than 3. Multiple tags are AND not OR  
`--skip-update` Lets you bypass the last downloaded time. Nice for redownloading everything.  
`-m, --markdown` Let's you download bookmarks as Markdown using Heckyesmarkdown.com  

## Notes

**2015-01-19**

- Added Spotlight comments with the URL and full description

**2014-12-23**  
- I don't have a lot of bookmarks (~150) and so I don't know what Pinboard will do if you request a ton of bookmarks for the initial download. If you have a lot of bookmarks and hit any weird errors, please let me know. 

