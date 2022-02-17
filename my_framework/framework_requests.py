from urllib.parse import unquote_plus


class Request:
    @staticmethod
    def parse_input_data(data: str) -> dict:
        result: dict = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
            return result


class GetRequests(Request):
    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


class PostRequests(Request):
    @staticmethod
    def get_wsgi_input_data(environ: dict) -> bytes:
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    @staticmethod
    def get_request_params(environ: dict) -> dict:
        data = PostRequests.get_wsgi_input_data(environ)
        if data:
            data_str = unquote_plus(data.decode(encoding='utf-8'))
            request_params = PostRequests.parse_input_data(data_str)
            return request_params
