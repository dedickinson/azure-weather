# Getting a web user's location

## Overview

For the web UI I wanted to have a static site calling into APIs. The
requirement can be described in the following user story:

**As a user I want to locate my nearest weather station so that I can access
observations and forecasts relevant to me**

### User location

We're likely to be able to determine the user's location via either :

- Use the [HTML 5 Geolocation
  API](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API)
- Ask the user to enter their postcode or town
- Ask the user to click on a map (e.g. to select a station or area)

For the latter we could use the [GeoNames database](http://www.geonames.org/) to
determine their co-ordinates.

### Weather station location

Various weather agencies list their station details - e.g.:

- [Australian BoM](http://www.bom.gov.au/climate/data/stations/)
- [UK Met
  Office](https://www.metoffice.gov.uk/public/weather/climate-network/#?tab=climateNetwork)

These will have the GPS co-ordinate of the station.

### Weather forecast location

These appear to mainly utilise a town/area name (e.g. "Brisbane") but can also
have an associated [shape file](https://en.wikipedia.org/wiki/Shapefile) that
designates the forecast area.

The Australian BoM describes the forecast spatial data in [a brief
guide](http://reg.bom.gov.au/catalogue/spatialdata.pdf).

### Bringing the data together

Once I know where the user is, I can use the [Haversine
formula](https://en.wikipedia.org/wiki/Haversine_formula) to determine their
nearest weather station. I'll assume that if there's nothing within 100km of the
user then the system will need to let the user know that there's no available
data.

For forecasts, I'd like to try and work out the user's forecast area by placing
them within the shapefile. I don't know how to do this so that's be a big challenge.

## The Challenges

This workbench aims to explore the following:

- [x] How do I get the user's current location via the HTML 5 Geolocation API?
- [ ] Can I use the GeoNames data to locate a user?
- [ ] Once I have the location, can I work out their closest weather station

### Run the demo site

To get the demo site up and running, make sure you have Node & NPM installed and
run:

    npm i
    npm start

## Discussion

### Data treatment

I don't include the source data in the Git repository as they're large and
easily accessible should you wish to use them yourself.

For the GeoNames work, I downloaded the [Australian
data](http://download.geonames.org/export/dump/AU.zip), extracted the data file
(`.txt`), renamed it to `geonames.txt` and placed it in `scripts/data/`. The
data fields are described in the [GeoNames
readme](http://download.geonames.org/export/dump/readme.txt).

The Australian Bureau of Meteorology (weather station
list)[ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/stations.zip]
contains a fixed-width text file. I extracted this and placed it in
`scripts/data/stations.txt`.

To run the scripts

    virtualenv -p python3.6 venv
    . venv/bin/activate
    pip install -r requirements.txt

The processed `json` data files used in the workbench site are placed under `site/data`.

# Citations

- The GeoNames data is licensed under a [Creative Commons Attribution 3.0
  License](http://creativecommons.org/licenses/by/3.0/)

- The Australian Bureau of Meteorology data is [Copyright Commonwealth of Australia 2018, Bureau of Meteorology](http://www.bom.gov.au/other/copyright.shtml?ref=ftr)
