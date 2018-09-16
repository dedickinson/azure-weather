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

1. How do I get the user's current location via the HTML 5 Geolocation API?
1.
