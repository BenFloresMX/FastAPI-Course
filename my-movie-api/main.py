from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = 'Application with FastAPI'
app.version = '0.0.1'

class Movie(BaseModel):
	id: Optional[int] = None # Another way to express this is id: int | None = None
	title: str = Field(min_length=5, max_length=15)
	overview: str = Field(min_length=15, max_length=50)
	year: int = Field(le=2022)
	rating: float = Field(ge=0, le=10)
	category: str = Field(min_length=3, max_length=10)

	#This class replaces the use of default in the attributes of the movie
	model_config = {
     "json_schema_extra": {
            "example":
                {
                    "id": 1,
                    "title": "Mi Película",
                    "overview": "Descripcion de la pelicula",
                    "year": 2022,
                    "rating": 10,
					"category": "Romance"
                }
        }
    }

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
        {
		"id": 2,
		"title": "Emoji: La Película",
		"overview": "Todos los utilizan; de hecho, los emojis son casi imprescindibles ...",
		"year": "2017",
		"rating": 5.5,
		"category": "Animación"
	},
    {
		"id": 3,
		"title": "El Padrino",
		"overview": "Don Vito Corleone es el respetado y temido jefe de una de las cinco ...",
		"year": "1972",
		"rating": 8.7,
		"category": "Drama"
	}
]


@app.get('/', tags =['home'])
def message():
    return HTMLResponse('<h1> Hello World <h1/>')

@app.get('/movies', tags = ['movies'], response_model= List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code= 200, content=movies)

@app.get('/movies/{id}', tags = ['movies'], response_model=Movie)
def get_movie_id(id: int = Path(ge=1, le=2000)) ->Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code= 404, content=[])

@app.get('/movies/', tags = ['movies'], response_model= List[Movie])
def get_movies_by_category(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]:
	data = [ item for item in movies if item['category'] == category ]
	return JSONResponse(content= data)

@app.post('/movies',tags = ['movies'], response_model= dict, status_code= 201)
def create_movie(movie: Movie) -> dict:
	movies.append(movie)
	return JSONResponse(status_code= 201, content={"message": "Se ha registrado/creado la película"})

@app.put('/movies/{id}', tags = ['movies'], response_model= dict, status_code= 200)
def update_movie(id: int, movie: Movie) -> dict:
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(status_code= 200, content={"message": "Se ha registrado/modificado la película"})
            
@app.delete('/movies/{id}', tags = ['movies'], response_model= dict, status_code= 200)
def delete_movie(id: int) -> dict:
	for item in movies:
		if item["id"] == id:
			movies.remove(item)
			return JSONResponse(status_code= 200, content={"message": "Se ha eliminado la película"})
		