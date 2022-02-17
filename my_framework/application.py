from my_framework.framework_requests import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 Page not found'


class Application:
    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):
        # Забираем адрес по которому пользователь выполнил переход
        path: str = environ['PATH_INFO']

        # Если в конце адреса нет /, то добавляем его
        if not path.endswith('/'):
            path = f'{path}/'

        request: dict = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method
        requests_params = None

        if method == 'GET':
            requests_params = GetRequests().get_request_params(environ)

        if method == 'POST':
            requests_params = PostRequests().get_request_params(environ)

        if requests_params:
            request['request_params'] = requests_params
            print(f'Параметры {method} запроса: {requests_params}')


        # Находим нужный контроллер
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        # Запускаем контроллер
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
