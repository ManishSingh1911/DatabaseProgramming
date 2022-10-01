import pymongo as pymongo
from flask import Flask, request, jsonify

app = Flask(__name__)

mongo = None
netflix_database = None
try:
    mongo = pymongo.MongoClient(
        host='localhost',
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo["local"]
    netflix_database = db["netflix"]
    mongo.server_info()
except:
    print("Error -connect to db")


@app.route('/api', methods=['POST'])
def post():
    movie_request = request.get_json()
    movie_id = movie_request["id"]
    movie_title = movie_request["title"]
    movie_desc = movie_request["description"]
    movie_type = movie_request["type"]
    movie_release_year = movie_request["release_year"]
    movie_runtime = movie_request["runtime"]
    movie_age_certification =movie_request["age_certification"]
    movie_genres =movie_request["genres"]
    movie_production_countries = movie_request["production_countries"]
    try:
        object = {'id': movie_id, 'title': movie_title, 'description': movie_desc,
                             'type': movie_type,
                             'runtime':movie_runtime,
                             'release_year':movie_release_year,
                             'age_certification':movie_age_certification,
                             'genres':movie_genres,
                             'production_countries':movie_production_countries,
                             }
        print(object)
        netflix_database.insert_one(object)
    except Exception as e:
        print(e)

    return f'Movie has been inserted into the list by title.'


@app.route('/api/<string:movieTitle>', methods=['PATCH'])
def update(movieTitle):
    movie_request = request.get_json()
    movie_title = movieTitle
    movie_description = movie_request['description']
    netflix_database.update_many({'title': movieTitle}, {"$set": {
        "title": movie_request['title'],
        "description": movie_description,
        "imdb_score": movie_request['imdb_score']
    }})
    return f'{movie_title} has been updated.'


@app.route('/api/<string:movieTitle>', methods=['DELETE'])
def delete(movieTitle):
    netflix_database.delete_one({"title": movieTitle})
    return 'Movie has been deleted'


def parseMovie(movie):
    if movie is None:
        return {}
    return {'film_id': movie['id'], 'title': movie['title'], 'description': movie['description'],
            'type':movie['movie_type'],
                         'runtime':movie['movie_runtime'],
                         'release_year': movie['movie_release_year'],
                         'age-certification':movie['movie_age_certification'],
                         'genres':movie['movie_genres'],
                         'production_countries':movie['movie_production_countries'],}


@app.route('/api', methods=['GET'])
def getAll():
    movies_object = []
    for movie in netflix_database.find({}, {"_id":0}):
        movies_object.append(movie)
    return jsonify(movies_object)



@app.route('/api/<string:movieTitle>', methods=['GET'])
def getMovieByTitle(movieTitle):
    response = []
    for x in netflix_database.find({"title": movieTitle}, {"_id": 0}):
        response.append(x)
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=7000)
