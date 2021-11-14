import grpc
import movie_pb2
import movie_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)

        print("-------------- GetMovieByID --------------")
        movieid = movie_pb2.MovieID(id = "a8034f44-aee4-44cf-b32c-74cf452aaaae")
        get_movie_by_id(stub, movieid)
        
        print("-------------- GetListMovies --------------")
        get_list_movies(stub)
        

        print("-------------- GetMovieByTitle --------------")
        movietitle = movie_pb2.MovieTitle(title = "The Good Dinosaur")
        get_movie_bytitle(stub, movietitle)
        

        print("-------------- GetMovieByDirector --------------")
        director = movie_pb2.MovieDirector(director = "Peter Sohn")
        get_movie_bydirector(stub, director)
        

        print("-------------- AddMovie --------------")
        movietoadd = movie_pb2.MovieData(title="Dune", rating=8.6, director="Denis Villeneuve", id="d556f1a6-80d1-4990-9117-3dbf411b42e2")
        add_movie(stub, movietoadd)
        

        print("-------------- DeleteMovieByID --------------")
        movietodelete = movie_pb2.MovieID(id = "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab" )
        delete_movie_byID(stub, movietodelete)
        get_list_movies(stub) # check the updated DB
        

        print("-------------- UpdateMovieRate --------------")
        movietoupdate = movie_pb2.MovieID(id = "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab" )
        rating = movie_pb2.MovieRate(rating=8.0)
        couple = movie_pb2.MovieIDAndRate(id=movietoupdate, rating=rating)
        update_movie_rate(stub, couple)
        

        print("-------------- DeleteMovieByRate --------------")
        rate = movie_pb2.MovieRate(rating=7.0)
        delete_movie_byRate(stub, rate)
        


def get_movie_by_id(stub,id):
    movie = stub.GetMovieByID(id)
    print(movie)

def get_list_movies(stub):
    allmovies = stub.GetListMovies(movie_pb2.Empty())
    for movie in allmovies:
        print("Movie called %s" % (movie.title))

def get_movie_bytitle(stub,title):
    movie = stub.GetMovieByTitle(title)
    print(movie)

def get_movie_bydirector(stub,director):
    directors_movies = stub.GetMovieByDirector(director)
    for movie in directors_movies:
        print("Director's movie called %s" % (movie.title))

def add_movie(stub,movietoadd):
    response = stub.AddMovie(movietoadd)
    # print the updated DB
    for movie in response:
        print("Movie called %s" % (movie.title))

def delete_movie_byID(stub, movieid):
    response = stub.DeleteMovieByID(movieid)
    # nothing to print or return (log is printed in the stub's rpc)

def update_movie_rate(stub, movieid_and_rate):
    updated_movie = stub.UpdateMovieRate(movieid_and_rate)
    print(updated_movie)

def delete_movie_byRate(stub, rate):
    response = stub.DeleteMovieByRate(rate)
    # print the updated DB
    get_list_movies(stub)
    

if __name__ == '__main__':
    run()

