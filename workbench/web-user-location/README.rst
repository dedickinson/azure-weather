=============================
Getting a web user's location
=============================

.. contents:: Contents

Overview
--------

For the web UI I wanted to have a static site calling into APIs.

The user requirement can be described in the following user story:

**As a user I want to locate my nearest weather station so that I can access
observations and forecasts relevant to me**

User location
-------------

We're likely to be able to determine the user's location via either :

- Use the `HTML 5 Geolocation API <https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API>`_
- Ask the user to enter their postcode or town
- Ask the user to click on a map (e.g. to select a station or area)

Weather station location
------------------------

Various weather agencies list their station details - e.g.:

* `Australian BoM <http://www.bom.gov.au/climate/data/stations/>`_
* `UK Met Office <https://www.metoffice.gov.uk/public/weather/climate-network/#?tab=climateNetwork>`_

These will have the GPS co-ordinate of the station.

Weather forecast location
-------------------------

These appear to mainly utilise a town/area name (e.g. "Brisbane") but can also
have an associated `shape file <https://en.wikipedia.org/wiki/Shapefile>`_ that
designates the forecast area.

The Australian BoM describes the forecast spatial data in `a brief
guide <http://reg.bom.gov.au/catalogue/spatialdata.pdf>`_. The shape files are
available via the `BOM's FTP site
<ftp://ftp.bom.gov.au/anon/home/adfd/spatial/>`_ under the ``IDM00001.*`` files.

Bringing the data together
--------------------------

Once I know where the user is, I could use the `Haversine
formula <https://en.wikipedia.org/wiki/Haversine_formula>`_ to determine their
nearest weather station. The trouble with the Haversine approach is that I'll
need to limit the stations in some manner (e.g. using a lat/long box based on
some calculation). I could assume that if there's nothing within 100km of the
user then the system will need to let the user know that there's no available
data. Alternatively, I could use a map/GIS service to do the heavy lifting for
me.

For forecasts, I'd like to try and work out the user's forecast area by placing
them within the shapefile. I don't know how to do this so that'll be a big
challenge.

The Challenges
--------------

This workbench aims to explore the following:

* How do I get the user's current location via the HTML 5 Geolocation API?
* Can I use the GeoNames data to locate a user?
* Can I Azure Maps data to locate a user?
* Can I use a postcode listing to locate a user?
* Once I have the location, can I work out their closest weather station?
* Once I have the location, can I work out their forecast region?

Spike solution
--------------

GeoLocation API
^^^^^^^^^^^^^^^

The API worked as advertised (hardly surprising). 

The very basic code is in ``site/index.html``.

To get the demo site up and running, make sure you have Node & NPM installed and
run::

    npm i
    npm start

Data sources
^^^^^^^^^^^^

A few small python scripts in the ``scripts`` directory provide data wrangling
from source formats into JSON.

Get started by changing into the ``web-user-location`` directory and running::

  virtualenv venv
  . venv/bin/activate
  pip install -r requirements.txt

I don't include the source data in the Git repository as they're large and
easily accessible should you wish to use them yourself.

GeoNames: Places
""""""""""""""""

For the GeoNames work, I downloaded the `Australian data 
<http://download.geonames.org/export/dump/AU.zip>`_, extracted the data file
(``.txt``), renamed it to ``geonames.txt`` and placed it in ``scripts/data/``.
The data fields are described in the `GeoNames readme
<http://download.geonames.org/export/dump/readme.txt>`_.

Data handling script: ``scripts/geoname-extract-places.py``

The JSON output looks as follows::

  [
    {
      "name": "Zanthus",
      "lat": -31.03511,
      "long": 123.57749,
      "feature_class": "P",
      "feature_code": "PPL",
      "country_code": "AU",
      "timezone": "Australia/Perth",
      "country": "Australia"
    },
    {
      "name": "Yunta",
      "lat": -32.58333,
      "long": 139.55,
      "feature_class": "P",
      "feature_code": "PPL",
      "country_code": "AU",
      "timezone": "Australia/Adelaide",
      "country": "Australia"
    },

GeoNames: Post codes
""""""""""""""""""""

I got the `Australian postcodes from GeoNames 
<http://download.geonames.org/export/zip/AU.zip>`_, extracted the data
file(``.txt``), renamed it to ``postcodes.txt`` and placed it in
``scripts/data/``. The fields are as follows:

* country code      : iso country code, 2 characters
* postal code       : varchar(20)
* place name        : varchar(180)
* admin name1       : 1. order subdivision (state) varchar(100)
* admin code1       : 1. order subdivision (state) varchar(20)
* admin name2       : 2. order subdivision (county/province) varchar(100)
* admin code2       : 2. order subdivision (county/province) varchar(20)
* admin name3       : 3. order subdivision (community) varchar(100)
* admin code3       : 3. order subdivision (community) varchar(20)
* latitude          : estimated latitude (wgs84)
* longitude         : estimated longitude (wgs84)
* accuracy          : accuracy of lat/lng from 1=estimated to 6=centroid

Data handling script: ``scripts/geoname-extract-postcodes.py``

The JSON output looks like::

  [
    {
      "country_code": "AU",
      "postal_code": "0221",
      "place_name": "Barton",
      "state": "Australian Capital Territory",
      "lat": -35.3049,
      "long": 149.1412,
      "accuracy": "4",
      "country": "Australia"
    },
    {
      "country_code": "AU",
      "postal_code": "2540",
      "place_name": "Wreck Bay",
      "state": "Australian Capital Territory",
      "lat": -35.1627,
      "long": 150.6907,
      "accuracy": "4",
      "country": "Australia"
    },

Australian Bureau of Meteorology (BOM)
""""""""""""""""""""""""""""""""""""""

The Australian Bureau of Meteorology `weather station
list <ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/stations.zip>`_
contains a fixed-width text file. I extracted this and placed it in
``scripts/data/stations.txt``.

Data handling script: ``scripts/bomstations-extract-full.py``

The JSON output looks like::

  [{
    "id": "001000",
    "dist": "01",
    "name": "KARUNJIE",
    "start": "1940",
    "end": "1983",
    "lat": "-16.2919",
    "lon": "127.1956",
    "source": null,
    "state": "wa",
    "height": "320.0",
    "bar_ht": null,
    "wmo_id": null,
    "country": "australia",
    "country_code": "AU",
    "provider": "bom"
  }, {
    "id": "001001",
    "dist": "01",
    "name": "OOMBULGURRI",
    "start": "1914",
    "end": "2012",
    "lat": "-15.1806",
    "lon": "127.8456",
    "source": "GPS",
    "state": "wa",
    "height": "2.0",
    "bar_ht": null,
    "wmo_id": null,
    "country": "australia",
    "country_code": "AU",
    "provider": "bom"
  }

Azure Maps
""""""""""

The `Azure Maps service <https://azure.microsoft.com/en-au/services/azure-maps/>`_ provides a number of useful APIs.

The following query for the suburb of "Burpengary"::

    https://atlas.microsoft.com/search/address/json?api-version=1.0&query=burpengary&countrySet=AU&subscription-key=<KEY>

Yielded the response below::

  {
    "summary": {
      "query": "burpengary",
      "queryType": "NON_NEAR",
      "queryTime": 22,
      "numResults": 6,
      "offset": 0,
      "totalResults": 6,
      "fuzzyLevel": 1
    },
    "results": [
      {
        "type": "Geography",
        "id": "AU/GEO/p0/9961",
        "score": 4.5,
        "info": "search:ta:036043075000418-AU",
        "entityType": "MunicipalitySubdivision",
        "address": {
          "municipalitySubdivision": "Burpengary",
          "municipality": "Brisbane",
          "countrySecondarySubdivision": "Brisbane",
          "countrySubdivision": "Queensland",
          "countryCode": "AU",
          "country": "Australia",
          "countryCodeISO3": "AUS",
          "freeformAddress": "Brisbane Burpengary, Queensland"
        },
        "position": {
          "lat": -27.15282,
          "lon": 152.97663
        },
        "viewport": {
          "topLeftPoint": {
            "lat": -27.12433,
            "lon": 152.91752
          },
          "btmRightPoint": {
            "lat": -27.18634,
            "lon": 152.98447
          }
        },
        "boundingBox": {
          "topLeftPoint": {
            "lat": -27.12433,
            "lon": 152.91752
          },
          "btmRightPoint": {
            "lat": -27.18634,
            "lon": 152.98447
          }
        },
        "dataSources": {
          "geometry": {
            "id": "00005831-3200-1200-0000-00007d320280"
          }
        }
      },
      ...
    ]
  }

Entering just a postcode gives a reasonable result:

    https://atlas.microsoft.com/search/address/json?api-version=1.0&query=4000&countrySet=AU&subscription-key=<KEY>

with the properties listing the suburbs covered by the postcode::

  "municipalitySubdivision": "Spring Hill, Petrie Terrace, Brisbane CBD"

Azure Search
""""""""""""

The GeoNames data was easily wrangled and gave a list of towns as well as
postcodes for towns. These could be put into a service such as Azure Search for easy lookups. There's a `webcast regarding Geo-spatial search with Azure Search <https://azure.microsoft.com/en-us/resources/videos/azure-search-and-geospatial-data/>`_ with the ```EDM.GeographyPoint`` data type<https://docs.microsoft.com/en-gb/rest/api/searchservice/Supported-data-types>`_ in the index.


Outcomes
--------

The work undertaken here helped me determine a direction for fulfilling the user story being explored:

**As a user I want to locate my nearest weather station so that I can access observations and forecasts relevant to me**

The following approach will be taken:

- Store the BOM weather station data in CosmosDB and feed these into Azure Search.
- Store the GeoNames postcode and locations data in CosmosDB and feed these into Azure Search.
- Provide the user with various UI inputs to help them find their closest
  weather station:
  - Pre-set weather stations for capital cities
  - HTML 5 GeoLocation API
  - Postcode lookup
  - Suburb/town lookup (we don't need their full address)
- Use Azure Search's Geo Spatial functionality to find nearby weather stations.

Citations
---------

- The GeoNames data is licensed under a `Creative Commons Attribution 3.0
  License <http://creativecommons.org/licenses/by/3.0/>`_

- The Australian Bureau of Meteorology data is `Copyright Commonwealth of Australia 2018, Bureau of Meteorology <http://www.bom.gov.au/other/copyright.shtml?ref=ftr>`_
