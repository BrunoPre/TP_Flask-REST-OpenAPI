import json
import grpc
from concurrent import futures

from werkzeug.wrappers import response
import movie_pb2
import movie_pb2_grpc

class MovieServicer(movie_pb2_grpc.MovieServicer):

    def __init__(self):
        with open('{}/../databases/movies.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["movies"]
            
    def GetMovieByID(self, request, context):
        for movie in self.db:   
            if movie['id'] == request.id:
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating="", director="", id="")
    
    def GetListMovies(self, request, context):
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])

    def GetMovieByTitle(self, request, context): # takes a MovieTitle and returns a MovieData
        for movie in self.db:
            if movie['title'] == request.title:
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        print("Movie not found.")
        return movie_pb2.MovieData(title="", rating="", director="", id="")

    def GetMovieByDirector(self, request, context): # takes a MovieDirector and returns a stream of MovieData

        atLeastOneMovieFound = False # debugging purpose
        
        for movie in self.db:
            if movie["director"] == request.director:
                print("Director's movie found!")
                atLeastOneMovieFound = True
                yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        
        if not atLeastOneMovieFound:
            print("No movie found for this director.")
            yield movie_pb2.MovieData(title="", rating="", director="", id="")


    def AddMovie(self, request, context): # takes a MovieData and returns a stream of MovieData
        
        # check if it already exists
        for movie in self.db:
            if movie["id"] == request.id:
                print("Movie ID already exists.")
                yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        
        # else : append it to BD
        req_json = {"title" : request.title, "rating" : request.rating, "director" : request.director, "id" : request.id}
        self.db.append(req_json)

        # stream all MovieData from updated BD
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])

    def DeleteMovieByID(self, request, context): # takes a MovieID and returns an Empty
        for movie in self.db:
            if movie['id'] == request.id:
                print("Movie found and deleted!")
                self.db.remove(movie)
                return movie_pb2.Empty()
        
        print('Movie ID not found in BD.')
        return movie_pb2.Empty()

    def UpdateMovieRate(self, request, context): # takes a MovieIDAndRate and returns a MovieData
        req_movieid = request.id    # MovieID
        req_rating = request.rating # MovieRate

        for movie in self.db:
            if movie['id'] == req_movieid.id:
                movie['rating'] = req_rating.rating
                print('Movie found and rating has been updated!')
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])

        print('Movie ID not found.')
        return movie_pb2.MovieData(title="", rating="", director="", id="")
    
    def DeleteMovieByRate(self, request, context): # takes a MovieRate and returns an Empty
        rate_threshold = float(request.rating)
        for movie in self.db:
            if movie['rating'] <= rate_threshold:
                self.db.remove(movie)
                print('Movie deleted!')
        
        return movie_pb2.Empty()

        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

