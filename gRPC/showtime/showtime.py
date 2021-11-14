import json
import grpc
from concurrent import futures

from werkzeug.wrappers import response
#import booking_pb2
#import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/../databases/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetListTimes(self, request, context): # takes an Empty and returns a stream of DateAndMovieID
        for schedule in self.db:
            yield showtime_pb2.DateAndMovieID(date=schedule['date'], scheduled_movies=schedule['movies'])

    def GetScheduleByDate(self, request, context): # takes a Date and returns a DateAndMovieID
        date = request.date
        for schedule in self.db:
            if schedule['date'] == date:
                print('Schedule found for the requested date!')
                return showtime_pb2.DateAndMovieID(date=schedule['date'], scheduled_movies=schedule['movies'])
        
        print('No schedule for the requested date.')
        return showtime_pb2.DateAndMovieID(date='', scheduled_movies=[])


    

        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

