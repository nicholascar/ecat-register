# eCat Register
A RESTful API to deliver the register of datasets and services contained in eCat for Linked Data system consumption

## Deployment web address
This is a Python Flask web app that can be tested anywhere but needs to be deployed at the URI register endpoint for eCat's datasets and services. As of 2016, eCat's datasets are deployed at [http://pid.geoscience.gov.au/dataset/{ECAT-ID}](http://pid.geoscience.gov.au/dataset/{ECAT-ID}) and services at [http://pid.geoscience.gov.au/service/{ECAT-ID}](http://pid.geoscience.gov.au/service/{ECAT-ID}) thus the corresponding dataset and services registers are [http://pid.geoscience.gov.au/dataset/](http://pid.geoscience.gov.au/dataset/) & [http://pid.geoscience.gov.au/service/](http://pid.geoscience.gov.au/service/) and that this application must respond to calls to those addresses.

To respond to calls to those addresses, this application must be proxied to by the web server managing the [http://pid.geoscience.gov.au](http://pid.geoscience.gov.au) domain name which is currently a [Persistent ID Service](https://www.seegrid.csiro.au/wiki/Siss/PIDService) web server managed by GA and located in the Data Platforms & Strategy Team's Amazon root account.

## Deployment configuration
This Flask app is configured to be deployed using Apache web server and mod_wsgi. The STATIC_SERVER variable in settings.py is used to bypass the proxy servers for static content such as GA branding images and stylesheets.

## Offline functions
This app contains a series of offline functions that are used to get the data it delivers via HTTP calls. All the information delivered is plublicly available from GA's eCat catalogue using [Catalog Service for the Web](https://en.wikipedia.org/wiki/Catalog_Service_for_the_Web) requests to the eCat Public endpoint (http://ecat.ga.gov.au/geonetwork/srv/eng/csw/).

The offline functions are either pure Python functions or Python functions that call Linux BASH shell scripts to process data from the CSW requests. These functions are use to update this application's list of dataset & service URIs which are sources from eCat Public which is always considered the point of truth. 

All the offline functions can be run separately (see functions.py) or all together which is done each night to update the datasets and services indexes. 

## Author
Nicholas Car
