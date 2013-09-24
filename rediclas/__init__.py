from pyramid.config import Configurator
import redis
import rediclas.utils as utils

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    utils.redis_server = utils.redis_from_config(config)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('stopwords', '/stopwords')
    config.add_route('classify', '/classify')
    config.add_route('train', '/train')
    config.scan()
    return config.make_wsgi_app()
