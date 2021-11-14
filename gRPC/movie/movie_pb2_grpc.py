# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import movie_pb2 as movie__pb2


class MovieStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetMovieByID = channel.unary_unary(
                '/Movie/GetMovieByID',
                request_serializer=movie__pb2.MovieID.SerializeToString,
                response_deserializer=movie__pb2.MovieData.FromString,
                )
        self.GetListMovies = channel.unary_stream(
                '/Movie/GetListMovies',
                request_serializer=movie__pb2.Empty.SerializeToString,
                response_deserializer=movie__pb2.MovieData.FromString,
                )
        self.GetMovieByTitle = channel.unary_unary(
                '/Movie/GetMovieByTitle',
                request_serializer=movie__pb2.MovieTitle.SerializeToString,
                response_deserializer=movie__pb2.MovieData.FromString,
                )
        self.GetMovieByDirector = channel.unary_stream(
                '/Movie/GetMovieByDirector',
                request_serializer=movie__pb2.MovieDirector.SerializeToString,
                response_deserializer=movie__pb2.MovieData.FromString,
                )
        self.AddMovie = channel.unary_stream(
                '/Movie/AddMovie',
                request_serializer=movie__pb2.MovieData.SerializeToString,
                response_deserializer=movie__pb2.MovieData.FromString,
                )
        self.DeleteMovieByID = channel.unary_unary(
                '/Movie/DeleteMovieByID',
                request_serializer=movie__pb2.MovieID.SerializeToString,
                response_deserializer=movie__pb2.Empty.FromString,
                )
        self.UpdateMovieRate = channel.unary_unary(
                '/Movie/UpdateMovieRate',
                request_serializer=movie__pb2.MovieIDAndRate.SerializeToString,
                response_deserializer=movie__pb2.MovieData.FromString,
                )
        self.DeleteMovieByRate = channel.unary_unary(
                '/Movie/DeleteMovieByRate',
                request_serializer=movie__pb2.MovieRate.SerializeToString,
                response_deserializer=movie__pb2.Empty.FromString,
                )


class MovieServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetMovieByID(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetListMovies(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMovieByTitle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMovieByDirector(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddMovie(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteMovieByID(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateMovieRate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteMovieByRate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MovieServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetMovieByID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMovieByID,
                    request_deserializer=movie__pb2.MovieID.FromString,
                    response_serializer=movie__pb2.MovieData.SerializeToString,
            ),
            'GetListMovies': grpc.unary_stream_rpc_method_handler(
                    servicer.GetListMovies,
                    request_deserializer=movie__pb2.Empty.FromString,
                    response_serializer=movie__pb2.MovieData.SerializeToString,
            ),
            'GetMovieByTitle': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMovieByTitle,
                    request_deserializer=movie__pb2.MovieTitle.FromString,
                    response_serializer=movie__pb2.MovieData.SerializeToString,
            ),
            'GetMovieByDirector': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMovieByDirector,
                    request_deserializer=movie__pb2.MovieDirector.FromString,
                    response_serializer=movie__pb2.MovieData.SerializeToString,
            ),
            'AddMovie': grpc.unary_stream_rpc_method_handler(
                    servicer.AddMovie,
                    request_deserializer=movie__pb2.MovieData.FromString,
                    response_serializer=movie__pb2.MovieData.SerializeToString,
            ),
            'DeleteMovieByID': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteMovieByID,
                    request_deserializer=movie__pb2.MovieID.FromString,
                    response_serializer=movie__pb2.Empty.SerializeToString,
            ),
            'UpdateMovieRate': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateMovieRate,
                    request_deserializer=movie__pb2.MovieIDAndRate.FromString,
                    response_serializer=movie__pb2.MovieData.SerializeToString,
            ),
            'DeleteMovieByRate': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteMovieByRate,
                    request_deserializer=movie__pb2.MovieRate.FromString,
                    response_serializer=movie__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Movie', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Movie(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetMovieByID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Movie/GetMovieByID',
            movie__pb2.MovieID.SerializeToString,
            movie__pb2.MovieData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetListMovies(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Movie/GetListMovies',
            movie__pb2.Empty.SerializeToString,
            movie__pb2.MovieData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMovieByTitle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Movie/GetMovieByTitle',
            movie__pb2.MovieTitle.SerializeToString,
            movie__pb2.MovieData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMovieByDirector(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Movie/GetMovieByDirector',
            movie__pb2.MovieDirector.SerializeToString,
            movie__pb2.MovieData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddMovie(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Movie/AddMovie',
            movie__pb2.MovieData.SerializeToString,
            movie__pb2.MovieData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteMovieByID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Movie/DeleteMovieByID',
            movie__pb2.MovieID.SerializeToString,
            movie__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateMovieRate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Movie/UpdateMovieRate',
            movie__pb2.MovieIDAndRate.SerializeToString,
            movie__pb2.MovieData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteMovieByRate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Movie/DeleteMovieByRate',
            movie__pb2.MovieRate.SerializeToString,
            movie__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
