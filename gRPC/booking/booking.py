import json
import grpc
from concurrent import futures

from werkzeug.wrappers import response
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/../databases/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetListBookings(self, request, context): # takes an Empty and returns a stream of Book
        for book in self.db:
            for date in book['dates']:
                    yield booking_pb2.Book(userid = book['userid'],
                                            date = booking_pb2.BookingDateAndMovieID(
                                                date = date['date'],
                                                scheduled_movies = date['movies'])
                                        )

    def GetMoviesByDate(self, request, context): # takes a BookingDate and returns BookingDateAndMovieID
        with grpc.insecure_channel('localhost:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            response = stub.GetScheduleByDate(showtime_pb2.Date(date=request.date))
            return booking_pb2.BookingDateAndMovieID(date=response.date, scheduled_movies=response.scheduled_movies)

    def GetUsersBook(self, request, context): # takes a UserID and returns a stream of Book
        user_found = False

        for book in self.db:
            if book['userid'] == request.id:
                print('User found !')
                for date in book['dates']:
                    yield booking_pb2.Book(userid = book['userid'],
                                            date = booking_pb2.BookingDateAndMovieID(
                                                date = date['date'],
                                                scheduled_movies = date['movies']
                                            )
                                        )
                user_found = True
        
        if not user_found:
            print('UserID not found.')
            yield booking_pb2.Book(userid = '', date = booking_pb2.BookingDateAndMovieID(date='',scheduled_movies=[]))

    def AddBook(self,request, context): # takes a Book and returns a Book

        with grpc.insecure_channel('localhost:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            response = stub.GetScheduleByDate(showtime_pb2.Date(date=request.date.date)) # returns a DateAndMovieID

            response_movies = response.scheduled_movies # array of string (movieids)

            req_movies = request.date.scheduled_movies # array of string (movieids)

            # check if all requested movies are scheduled
            check_avail_movies = all(movie in response_movies.scheduled_movies for movie in req_movies)

            if check_avail_movies:
                for book in self.db: # come across all the bookings

                    if book['userid'] == request.userid: # user exists
                        for date in book["dates"]:

                            if date['date'] == request.date.date: # if there's already a booking at the same date
                                date['movies'].extend(req_movies)
                                return request
                            
                        # if there is no booking at the request date, then the full request is added
                        book['dates'].append({'date' : request.date.date, 'movies' : req_movies})
                        return request
                
                # user ID does not exist --> add the full request
                new_user_booking = {
                    "userid" : request.userid,
                    "dates" : [{'date' : request.date.date, 'movies' : req_movies}]
                }
                self.db.append(new_user_booking)
                return booking_pb2.Book(userid=request.userid, 
                                        date=booking_pb2.BookingDateAndMovieID(date=request.date.date, scheduled_movies=req_movies)
                                        )

            # if all requested movies are not scheduled
            print('Not all the request movies are scheduled on this date.')
            return  booking_pb2.Book(userid=request.userid, date=booking_pb2.BookingDateAndMovieID(date='', scheduled_movies=[]))

        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

