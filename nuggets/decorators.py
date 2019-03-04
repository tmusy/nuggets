#!flask/bin/python
import functools
from flask import url_for, request


def marshal(schema):
    """Serialize the python object for the REST response.

    :param schema:
    :return:
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            # invoke the wrapped function
            res_object = f(*args, **kwargs)
            res_object['_embedded']['items'] = schema.dump(res_object['_embedded']['items']).data
            return res_object
        return wrapped
    return decorator


def paginate(page_size=20):
    """Generate a paginated response for a resource collection.

    Routes that use this decorator must return a SQLAlchemy query as a
    response.

    The output of this decorator is a Python dictionary with the paginated
    results. The application must ensure that this result is converted to a
    response object, either by chaining another decorator or by using a
    custom response object that accepts dictionaries."""
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            # invoke the wrapped function
            query = f(*args, **kwargs)

            # obtain pagination arguments from the URL's query string
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('pageSize', page_size, type=int)

            # run the query with Flask-SQLAlchemy's pagination
            p = query.paginate(page, per_page)


            # build the pagination
            res_dict = {
                '_links': {
                    'self': {'href': request.url},
                    'first': {'href': url_for(request.endpoint, _external=True, **kwargs)},
                    'prev': {'href': None},
                    'next': {'href': None},
                    'last': {'href': url_for(request.endpoint, page=p.pages, pageSize=per_page, _external=True, **kwargs)}
                },
                '_embedded': {
                    'items': p.items
                },
                'total': p.total,
                'count': len(p.items),
                'page_count': p.pages
            }

            if p.has_prev:
                res_dict['_links']['prev']['href'] = url_for(request.endpoint, page=p.prev_num, pageSize=per_page, _external=True, **kwargs)
            if p.has_next:
                res_dict['_links']['next']['href'] = url_for(request.endpoint, page=p.next_num, pageSize=per_page, _external=True, **kwargs)

            # return a dictionary as a response
            return res_dict
        return wrapped
    return decorator
