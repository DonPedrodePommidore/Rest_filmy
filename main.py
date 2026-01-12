from fastapi import FastAPI
from typing import Any
import sqlite3
app = FastAPI()
@app.get('/movies')
def get_movies():
    db = sqlite3.connect('movies.db')
    data = db.execute("SELECT * FROM movies").fetchall()
    output = []
    for x in data:
        output.append({
            "id": x[0],
            "title": x[1],
            "year": x[2],
            "actors": x[3]
        })
    return output

@app.get('/movies/{movie_id}')
def get_single_movie(movie_id:int):
    db = sqlite3.connect('movies.db')
    data = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    db.commit()
    return data

@app.post("/movies")
def add_movie(params: dict[str, Any]):
    db = sqlite3.connect('movies.db')
    cursor = db.execute("INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",(params['title'], params['year'], params['actors']))
    db.commit()
    return {"message": f"Movie added successfully", "id": cursor.lastrowid}

#testowanie w konsoli: curl.exe --header "Content-Type: application/json" --request POST --data '{\"title\":\"Skazani na Shawshank\",\"year\":1994, \"actors\":\"Tim Robbins\"}' http://localhost:8000/movies
@app.delete("/movies/{movie_id}")
def del_movie(movie_id:int):
    db = sqlite3.connect('movies.db')
    db.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    db.commit()
    return {"message": f"Movie deleted successfully", "id": movie_id}

@app.put("/movies/{movie_id}")
def update_movie(movie_id:int, params: dict[str, Any]):
    db = sqlite3.connect('movies.db')
    db.execute("UPDATE movies SET title = ?, year = ?, actors = ? WHERE id = ? ",(params['title'], params['year'], params['actors'], movie_id))
    db.commit()
    return {"message": f"Movie updated successfully", "id": movie_id}
#testowanie: curl.exe --% -X PUT http://localhost:8000/movies/4 -H "Content-Type: application/json" -d "{\"title\":\"Ojciec Chrzestny\",\"year\":1972,\"actors\":\"Al Pacino\"}"
@app.delete("/movies")
def del_movies():
    db = sqlite3.connect('movies.db')
    db.execute("DELETE FROM movies")
    db.commit()
    return {"message": "Movie deleted successfully"}