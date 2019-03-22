from sanic import Sanic, response
from jinja2 import Environment, PackageLoader, select_autoescape

from utils import Webcam


def stream(webcamId):
    name = "streaming_{}".format(webcamId)
    app = Sanic(name)
    webcam = Webcam(webcamId)

    @app.route("/")
    async def root(request):
        return response.stream(
            webcam.stream,
            content_type='multipart/x-mixed-replace; boundary=frame'
        )

    app.run(host='0.0.0.0', port=8001 + webcamId)


def index(count):
    app = Sanic()
    app.static('/static', './static')
    env = Environment(
        loader=PackageLoader('core.video', '../template/html'),
        autoescape=select_autoescape(['html', 'xml', 'tpl']),
        enable_async=True)

    async def template(tpl, **kwargs):
        template = env.get_template(tpl)
        rendered_template = await template.render_async(**kwargs)
        return response.html(rendered_template)

    @app.route("/")
    async def root(request):
        return await template('index.html', count=count)

    app.run(host='0.0.0.0', port=8000)
