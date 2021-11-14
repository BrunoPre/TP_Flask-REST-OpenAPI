import grpc
import showtime_pb2
import showtime_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)
        '''
        print("-------------- GetListTimes --------------")
        get_list_times(stub)

        print("-------------- GetScheduleByDate --------------")
        date = showtime_pb2.Date(date='20151130')
        get_schedule_byDate(stub,date)
        '''


def get_list_times(stub):
    alltimes = stub.GetListTimes(showtime_pb2.Empty())
    for time in alltimes:
        print(f'-- Date : {time.date} --')
        for movieid in time.scheduled_movies:
            print(f' Movie : {movieid}')

def get_schedule_byDate(stub, date):
    time = stub.GetScheduleByDate(date)
    print(f'-- Date : {time.date} --')
    for movieid in time.scheduled_movies:
            print(f' Movie : {movieid}')
    


if __name__ == '__main__':
    run()

