from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = 'Application with FastAPI'
app.version = '0.0.1'


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

@app.get('/movies', tags = ['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags = ['movies'])
def get_movie_id(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return id

@app.get('/movies/', tags = ['movies'])
def get_movies_by_category(category: str, year: int):
    return list(filter(lambda item: item['category'] == category , movies))

@app.post('/movies',tags = ['movies'])
def create_movie(id: int = Body(), title: str= Body(), overview: str= Body(), year: int= Body(), rating: float= Body(), category: str= Body()):
	movies.append({
		"id": id,
		"title": title,
		"overview": overview,
		"year": year,
		"rating": rating,
		"category": category
          })
	return movies

@app.put('/movies/{id}', tags = ['movies'])
def update_movie(id: int, title: str= Body(), overview: str= Body(), year: int= Body(), rating: float= Body(), category: str= Body()):
	for item in movies:
		if item["id"] == id:
			item['title'] = title,
			item['overview'] = overview,
			item['year'] = year,
			item['rating'] = rating,
			return movies
            
@app.delete('/movies/{id}', tags = ['movies'])
def delete_movie(id: int):
	for item in movies:
		if item["id"] == id:
			movies.remove(item)
			return movies
		