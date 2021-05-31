from utils.http.responses import Response


def handle_server_error(error):
    return Response.get_error(500, str(error))


def handle_400_error(error):
    return Response.get_error(400, str(error))


def handle_404_error(error):
    return Response.get_error(404, str(error))
