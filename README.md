# Brewing Stats Server

## What is this?

This project is the ongoing development of my brewing status server. This code is designed to 
control, monitor and document the temperature of a brewing vessel during fermentation.


## Current Status

All code commited works (for me!) but your milage may vary.

## Database

The database in use is mysql with the following details:

create database beer;

use beer;

CREATE TABLE beers
(
  brew_temp_max             FLOAT(9),                     # Max Brew temp
  brew_temp_min             FLOAT(9),                     # Min Brew temp
  brew_temp_now             FLOAT(9),                     # Current Brew temp
  brew_temp_target          FLOAT(9),                     # Brew target temp
  heater_status             BOOL,                         # Status of heater
  name                      VARCHAR(150) NOT NULL,        # Name of the beer
  brew_day_notes            TEXT(10000),                  # Brewday notes
  tasting_notes             TEXT(10000),                  # Tasting notes
  beer_temp_data            MEDIUMTEXT,                   # Brewing temp data for beer(max length 16,777,215 chars)
  ambient_temp_data         MEDIUMTEXT,                   # Brewing temp data for room(max length 16,777,215 chars)
  pre_boil_gravity          FLOAT(8),                     # PBG of the beer
  original_gravity          FLOAT(8),                     # OG of the beer
  final_gravity             FLOAT(8),                     # FG of the beer
  brew_date                 DATE,                         # Brewday date of the beer
  bottling_date             DATE,                         # Bottling date of the beer
  PRIMARY KEY               (name)                        # Make the name the primary key 
);


## Python Backend Heat Controller

### /heatController

This code is for the Raspberry Pi running controlling the heating and data logging of our brewing vessel.

#### temper.py 

This is the controller class for our temperature probes and is based on Scott Campbell's code (link to which can be found in the license section of the code).

#### hotboi.py

This is the original code I wrote that stands alone and will run without a database or CSV input.

#### datHotBoi.py

This file takes a heating profile as input and outputs to a CSV.

#### datDataBasedHotBoi.py

The (probable) final form!

This maintains a given temperature and periodically spits out data to the terminal and to the Database. The heat data is written in JSON for ease of consuption by the graph plotting software.
I use the pymysql library to connect to the MySQL Databasse.

## Rust Rocket Front End Web Server

This project uses Rust and the Rocket and Handlebars frameworks to stand up a web server to display our data in a consumable manner.

### /src

#### main.rs

This is the main function and defines the routes for the web server and our only input, the desired beer to view data about.

#### dbaccess.rs

This module is written to interface with our MYSQL server and uses the mysql library to do so. It takes in the user input, sanitizes it, joins it to a query to fetch the beer and finally maps the results of the query to a predefined "Beer" struct.

### /static

The code supports static info and currently I use this to server the header SVG for some asthetic flare. In the future I will also include links to recipies here for easy acces and for others who are interested.

#### /css

This is where the css is stored.

#### /images

This is where our header SVG is stored.

### /templates

This is the folder containing our handlebars templates. This is mostly boring HTML. The part of note however is the use of chart.js to display our data. I have included a specific version together with an integrity hash but it would be nice to have a non JavaScript and Libre way of displaying dta nicely.

## License

    This file is part of Brewing Stats Server.

    Brewing Stats Server is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Brewing Stats Server is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Brewing Stats Server.  If not, see <https://www.gnu.org/licenses/>.
