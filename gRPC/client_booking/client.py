import grpc
import booking_pb2
import booking_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        print("-------------- GetScheduleByDate --------------")
        get_list_bookings(stub)

        print("-------------- GetListBookings --------------")
        date = booking_pb2.BookingDate(date = '20151201')
        get_movies_by_date(stub, date)

        print("-------------- GetUsersBook --------------")
        user = booking_pb2.UserID(id = 'garret_heaton')
        get_users_book(stub, user)

        print("-------------- AddBook --------------")
        date = booking_pb2.BookingDateAndMovieID(date="20151202",scheduled_movies=["7daf7208-be4d-4944-a3ae-c1c2f516f3e6","267eedb8-0f5d-42d5-8f43-72426b9fb3e6"] )
        book = booking_pb2.Book(userid= "chris_rivers", date=date)
        add_book(stub,book)

def get_list_bookings(stub):
    bookings = stub.GetListBookings(booking_pb2.BookingEmpty())
    for book in bookings:
        print(f'UserID : {book.userid}, Date : {book.date.date}, Booked movies : {book.date.scheduled_movies}')
    
def get_movies_by_date(stub, date):
    movies = stub.GetMoviesByDate(date)
    print(f'Date : {movies.date}, Scheduled movies : {movies.scheduled_movies}')

def get_users_book(stub, user):
    bookings = stub.GetUsersBook(user) # Book array
    for book in bookings:
        print(f'UserID : {book.userid}, Date : {book.date.date}, Booked movies : {book.date.scheduled_movies}')
    
def add_book(stub, book):
    res_book = stub.AddBook(book)
    print(f'UserID : {res_book.userid}, Date : {res_book.date.date}, Booked movies : {res_book.date.scheduled_movies}')

if __name__ == '__main__':
    run()

