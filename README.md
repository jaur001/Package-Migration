# PR-049633 - SD.ZURICH INSURANCE COMPANY LTD

Python script which migrates MSTR objects from one environment to another.


### Requirements
* Python 3.9+
* 2 environments with MicroStrategy 2021 Update 4.1 available.


### MicroStrategy version: 
MSTR 2021 Update 4.1


### Current version: 
1.1

### Publisher: 
* MicroStrategy Profesional Services (Embedded Analytics Team)


### Latest release date: 
April 6th, 2022

### Changes made:
Version 1.1
* Changed order of arguments between project and environment
* Added session login to try-except, so it will log the errors (in case it happens).

Version 1.0
* Create package (mmp)
* Import package
* Rollback package
* Migrate package (consumes create package and import package)

### Build steps
* Clone the repository in your machine.
* Open the folder where is located from the command line
* Run the package migration script passing the arguments required

### deployment and configuration steps
* Open config.json file
* Configure the environments and projects available
* Save changes

