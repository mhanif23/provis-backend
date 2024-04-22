use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use mysql::*;
use mysql::prelude::*;

// Struktur untuk menyimpan data pengguna
#[derive(Debug)]
struct User {
    id: u32,
    username: String,
    password: String,
}

// Struktur untuk menyimpan data dokter
#[derive(Debug)]
struct Doctor {
    id: u32,
    name: String,
    specialty: String,
}

// Koneksi ke database MySQL
fn establish_connection() -> Pool {
    let url = "mysql://username:password@localhost/database_name";
    Pool::new(url).expect("Failed to connect to database")
}

// Fungsi untuk mendaftar (signup)
fn signup(username: String, password: String) -> Result<(), &'static str> {
    let pool = establish_connection();
    let mut conn = pool.get_conn().unwrap();

    let query = "INSERT INTO users (username, password) VALUES (?, ?)";
    conn.exec_drop(query, (username, password)).unwrap();

    Ok(())
}

// Fungsi untuk login
fn login(username: String, password: String) -> Result<(), &'static str> {
    let pool = establish_connection();
    let mut conn = pool.get_conn().unwrap();

    let query = "SELECT * FROM users WHERE username = ? AND password = ?";
    let result: Vec<User> = conn.query_map(query, (username, password), |(id, username, password)| {
        User { id, username, password }
    }).unwrap();

    if result.is_empty() {
        Err("Invalid username or password")
    } else {
        Ok(())
    }
}

// Fungsi untuk mendapatkan daftar dokter
fn get_doctors() -> Vec<Doctor> {
    let pool = establish_connection();
    let mut conn = pool.get_conn().unwrap();

    let query = "SELECT * FROM doctors";
    conn.query_map(query, (), |(id, name, specialty)| {
        Doctor { id, name, specialty }
    }).unwrap()
}

// Handler untuk endpoint signup
async fn signup_handler(data: web::Json<User>) -> impl Responder {
    match signup(data.username.clone(), data.password.clone()) {
        Ok(_) => HttpResponse::Ok().json("User signed up successfully"),
        Err(err) => HttpResponse::BadRequest().json(err),
    }
}

// Handler untuk endpoint login
async fn login_handler(data: web::Json<User>) -> impl Responder {
    match login(data.username.clone(), data.password.clone()) {
        Ok(_) => HttpResponse::Ok().json("User logged in successfully"),
        Err(err) => HttpResponse::Unauthorized().json(err),
    }
}

// Handler untuk endpoint fetching list dokter
async fn get_doctors_handler() -> impl Responder {
    let doctors = get_doctors();
    HttpResponse::Ok().json(doctors)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Menginisialisasi server Actix
    HttpServer::new(|| {
        App::new()
            // Endpoint signup
            .route("/signup", web::post().to(signup_handler))
            // Endpoint login
            .route("/login", web::post().to(login_handler))
            // Endpoint untuk fetching list dokter
            .route("/doctors", web::get().to(get_doctors_handler))
    })
    .bind("127.0.0.1:3000")?
    .run()
    .await
}
