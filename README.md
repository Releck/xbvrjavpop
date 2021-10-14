XBVR JAV Populator
===

Automatically scrapes files with the JAVR scraper in XBVR


Setup
---
- Change `XBVR_HOST` to where your XBVR instance is located
- Install dependencies with `pip install -r requirements.txt`
- Run the script


Running
---
This script assumes everything in your library that hasn't been matched is JAV 
and should be matched with the JAVR scraper. It will try and figure out what code each
file should be matched up with, scrape the scene for that code and pair the file
to the scene in XBVR.


Limitations
---
As XBVR's JAV scraper only uses R18 only titles from R18 will be matched. Any titles
that are not on R18 (like SOD, Rookie) won't be matched.
