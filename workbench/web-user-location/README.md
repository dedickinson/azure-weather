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
guide](http://reg.bom.gov.au/catalogue/spatialdata.pdf). The shape files are
available via the [BOM's FTP site](ftp://ftp.bom.gov.au/anon/home/adfd/spatial/)
under the `IDM00001.*` files.

### Bringing the data together

Once I know where the user is, I could use the [Haversine
formula](https://en.wikipedia.org/wiki/Haversine_formula) to determine their
nearest weather station.

The trouble with the Haversine approach is that I'll need to limit the stations
in some manner (e.g. using a lat/long box based on some calculation).
I'll assume that if there's nothing within 100km of the
user then the system will need to let the user know that there's no available
data. Alternatively, I could use a map/GIS service to do the heavy lifting for me.

For forecasts, I'd like to try and work out the user's forecast area by placing
them within the shapefile. I don't know how to do this so that's be a big challenge.

## The Challenges

This workbench aims to explore the following:

- [x] How do I get the user's current location via the HTML 5 Geolocation API?
- [ ] Can I use the GeoNames data to locate a user?
- [ ] Can I Azure Maps data to locate a user?
- [ ] Can I use a postcode listing to locate a user?
- [ ] Once I have the location, can I work out their closest weather station?
- [ ] Once I have the location, can I work out their forecast region?

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

I also got the [Australian postcodes from
GeoNames](http://download.geonames.org/export/zip/AU.zip), extracted the data file
(`.txt`), renamed it to `postcodes.txt` and placed it in `scripts/data/`.

The Australian Bureau of Meteorology (weather station
list)[ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/stations.zip]
contains a fixed-width text file. I extracted this and placed it in
`scripts/data/stations.txt`.

To run the scripts, `cd` into the `scripts` directory and:

    virtualenv -p python3.6 venv
    . venv/bin/activate
    pip install -r requirements.txt

Then you can just run each script as required.

The processed `json` data files used in the workbench site are placed under `site/data`.

### Accessing location

#### GeoLocation API

Worked as advertised. Demo in `site/userlocation.html`.

#### GeoNames data

The GeoNames data was easily wrangled and gave a list of towns as well as
postcodes for towns.

These could be put into a service such as Azure Search for easy lookups. There's
a [webcast regarding Geo-spatial search with Azure
Search](https://azure.microsoft.com/en-us/resources/videos/azure-search-and-geospatial-data/)
with the [`EDM.GeographyPoint` data
type](https://docs.microsoft.com/en-gb/rest/api/searchservice/Supported-data-types)
in the index.

#### Azure Maps

The following query for the suburb of "Burpengary:

    https://atlas.microsoft.com/search/address/json?api-version=1.0&query=burpengary&countrySet=AU&subscription-key=<KEY>

Yielded the response below:

```json
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
```

Entering just a postcode gives a reasonable result:

    https://atlas.microsoft.com/search/address/json?api-version=1.0&query=4000&countrySet=AU&subscription-key=<KEY>

with the properties listing the suburbs covered by the postcode:

```json
"municipalitySubdivision": "Spring Hill, Petrie Terrace, Brisbane CBD"
```

## Outcomes

For weather observations, we need to locate weather stations:

- Store the weather station, postcode, and locations data into CosmosDB and feed these into Azure Search
- Provide the user with various UI inputs to help them find their closest
  weather station:
  - Pre-set weather stations for capital cities
  - HTML 5 GeoLocation API
  - Postcode lookup
  - Suburb/town lookup (we don't need their full address)
- Use Azure Search's Geo Spatial functionality to find nearby weather stations.

## Citations

- The GeoNames data is licensed under a [Creative Commons Attribution 3.0
  License](http://creativecommons.org/licenses/by/3.0/)

- The Australian Bureau of Meteorology data is [Copyright Commonwealth of Australia 2018, Bureau of Meteorology](http://www.bom.gov.au/other/copyright.shtml?ref=ftr)
