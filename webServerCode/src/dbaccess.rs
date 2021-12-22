use mysql::*;
use mysql::prelude::*;
use chrono::prelude::*;

//Define our beer struct with feilds to match our database
#[derive(serde::Serialize)]
pub struct Beer {
  pub brew_temp_max: f32,             
  pub brew_temp_min: f32,             
  pub brew_temp_now: f32,             
  pub brew_temp_target: f32,             
  pub heater_status: bool,                 
  pub name: String,
  pub brew_day_notes: String,          
  pub tasting_notes: String,          
  pub beer_temp_data: String,           
  pub ambient_temp_data: String,           
  pub pre_boil_gravity: f32,             
  pub original_gravity: f32,             
  pub final_gravity: f32,             
  pub brew_date: Option<NaiveDate>,                 
  pub bottling_date: Option<NaiveDate>,                 
}

pub fn get_beer(beer_to_get: String) -> Option<Beer>{
    // Let's select a beeer from the database. 
   
    //But first, thwart any pesky hackers trying to get SQLi 
    let mut the_beer_to_get: String = "".to_string();
    if beer_to_get.chars().all(char::is_alphanumeric) {
        the_beer_to_get = beer_to_get;
    }
    else {
        the_beer_to_get = "Test".to_string();
    }


    //Creds in code boo! Feel free to be better than me or not and just paste in appropriate info below
    //Note: my DB is called "beer" and the table is "beers"
    //Now connect to the DB
    let url: &'static str = "mysql://a_read_user:their_password@127.0.0.1:3306/beer";
    let opts = Opts::from_url(url).unwrap();
    let pool = mysql::Pool::new(opts).unwrap();
    let mut conn = pool.get_conn().unwrap();

    //Join our requested beer into a query and ask.
    let query = format!("{}{}{}","SELECT * FROM beers WHERE name='", the_beer_to_get, "'");
    let mut row: mysql::Row = query.first(&mut conn).unwrap()?;
    
    //Now we build our Beer struct from the DB data.
    //Note that the error handling is effectively "Panic if the DB has an issue and deal with Null values properly"
    Some(Beer {
    brew_temp_max: row.take_opt("brew_temp_max").unwrap().unwrap_or_default(),
    brew_temp_min: row.take_opt("brew_temp_min").unwrap().unwrap_or_default(),             
    brew_temp_now: row.take_opt("brew_temp_now").unwrap().unwrap_or_default(),             
    brew_temp_target: row.take_opt("brew_temp_target").unwrap().unwrap_or_default(),             
    heater_status: row.take_opt("heater_status").unwrap().unwrap_or_default(),                 
    name: row.take_opt("name").unwrap().unwrap_or_default(),
    brew_day_notes: row.take_opt("brew_day_notes").unwrap().unwrap_or_default(),          
    tasting_notes: row.take_opt("tasting_notes").unwrap().unwrap_or_default(),          
    beer_temp_data: row.take_opt("beer_temp_data").unwrap().unwrap_or_default(),           
    ambient_temp_data: row.take_opt("ambient_temp_data").unwrap().unwrap_or_default(),           
    pre_boil_gravity: row.take_opt("pre_boil_gravity").unwrap().unwrap_or_default(),             
    original_gravity: row.take_opt("original_gravity").unwrap().unwrap_or_default(),             
    final_gravity: row.take_opt("final_gravity").unwrap().unwrap_or_default(),             
    brew_date: row.take_opt("brew_date").unwrap().ok(),                 
    bottling_date: row.take_opt("bottling_date").unwrap().ok()                
    })

    //Because this is Rust, the return type is implied by our Beer struct. So no explicit return needed.
}

//    License
//
//    This file is part of Brewing Stats Server.
//
//    Brewing Stats Server is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    Brewing Stats Server is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with Brewing Stats Server.  If not, see <https://www.gnu.org/licenses/>.
