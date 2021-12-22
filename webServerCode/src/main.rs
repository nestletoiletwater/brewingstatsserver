#![feature(proc_macro_hygiene, decl_macro)]

extern crate mysql;
#[macro_use] extern crate rocket;
use rocket::response::Redirect;
use rocket_contrib::templates::Template;
use rocket_contrib::serve::StaticFiles;
use chrono::prelude::*;

//load the db;
mod dbaccess;

//define our current beer selection struct
#[derive(serde::Serialize)]
struct CurrentBeer {
    beer_info: dbaccess::Beer,
    parent: &'static str
}

#[derive(serde::Serialize)]
struct AboutContext {
    parent: &'static str
}

//Add in some routes!

#[get("/")]
fn index() -> Redirect {
    Redirect::to("/beer/Test")
}

#[get("/beer/<a_beer_name>")]
fn beer_data(a_beer_name: String) -> Option<Template> {
    Some(Template::render("index", &CurrentBeer {
        beer_info: dbaccess::get_beer(a_beer_name)?,
        parent: "layout"
    }))
}

#[get("/about")]
fn about() -> Template {
    Template::render("about", &AboutContext {
        parent: "layout"
    })
}

//Light the ignition and stand back?
fn main() {
    rocket::ignite()
        .mount("/", routes![index, beer_data, about])
        .mount("/static", StaticFiles::from("static"))
        .attach(Template::fairing())
        .launch();
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
