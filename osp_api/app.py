"""OSP REST API."""

import flask
import flask_limiter
import flask_restful
from webargs.flaskparser import (use_args, parser)
from webargs.fields import (DateTime, Str, Int, List)
from flask_cache import Cache

from . import config
from . import util


__API_VERSION__ = 'v1'


app = flask.Flask(__name__)
app.config.from_object(config)
cache = Cache(app, config=config.FLASK_CACHE)
# TODO: custom errors (set through instantiation of Api)
api = flask_restful.Api(app, prefix='/' + __API_VERSION__)
limiter = flask_limiter.Limiter(
    app,
    key_func=flask_limiter.util.get_remote_address,
)


class Title(flask_restful.Resource):
    """A singular, specific title (see TitleList).

    """

    # NOTE, TODO, XXX: cache this and all other queries, even if minimal like this one?
    def get(self, title_id):
        """Get a specific title by ID.

        Arguments:
            title_id (int): Internally-assigned identifier which will
                locate a specific title. Produced as a Flask route
                argument.

        Returns:
            json entity: A JSON entity representing the title
                which corresponds to the supplied title_id.

        """

        # FIXME
        return {'lol': True}


class TitleList(flask_restful.Resource):
    """List of titles; academic work, texts, journal article, book, paper, etc.

    NOT a Syllabus. A title is something that would be cited by other
    titles, or used as material in a Syllabus.

    See Also:
        :class:`Title` (resource).

    """

    # FIXME: flask_cache issue: if the query args are in a different order it   
    # creates a new cache entry...
    #
    # TODO: This use_args dict is applicable to pretty much all resources that
    # can be queried (returning a list of entities) so KISS
    #
    # TODO: Need to invalidate based on args that aren't in the schema?
    @cache.cached(key_prefix=util.make_cache_key)
    @use_args(
        dict(
            offset = Int(validate=lambda n: n >= 0),
            limit = Int(validate=lambda n: 1 <= n <= 100, missing=25),
            order = Str(validate=lambda s: s in ['asc', 'desc',]),
            pub_date_start = DateTime(),
            pub_date_end = DateTime(),  # XXX: do i want default to now()?
            authors = List(Int(validate=lambda n: n>=0)),
            schools = List(Int(validate=lambda n: n>=0)),
            fields = List(Int(validate=lambda n: n>=0)),
            # XXX: isn't `titles` supposed to do like-match on a series of strings?
            titles = List(Int(validate=lambda n: n>=0)),
            countries = List(Int(validate=lambda n: n>=0)),
            publisher = Int(validate=lambda n: n >= 0),
        ),
        locations=('querystring',),
    )
    def get(self, args):
        """Query all titles based on criteria from querystring.

        Arguments:
            args (dict): Dictionary injected from use_args, which
                ensures that `args` herein is valid according to
                the schema specified in the @use_args decorator.

        Returns:
            json "task" entity: ...

        """

        # FIXME: elasticsearch. this is but a demo of caching.
        import random
        args['random'] = random.randint(0, 1000)
        return args


@parser.error_handler
def handle_arg_schema_error(error):
    """RESTful error regarding webarg schema mismatch (invalidation).

    Arguments:
        error (???): An error object from webargs, passed to this
        function when a request's arguments are not valid according to
        the specified webargs schema (a dict, see: use_args decorator).

    Returns:
        json "error" entity: ...

    """

    flask_restful.abort(400, validation_error=error.messages)


# Map resources to routes!
api.add_resource(TitleList, '/titles')
api.add_resource(Title, '/titles/<int:title_id>')
