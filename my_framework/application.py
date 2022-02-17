class PageNotFound404:
    def __call__(self):
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

        # Находим нужный контроллер
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        # Запускаем контроллер
        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
