from sqlalchemy import desc, asc

from eva.utils.translation import ugettext_lazy as _
from eva.exceptions import EvaError


def get_order_obj(model, args):

    sort_by = args.get('sort_by')
    if sort_by != 'id' and sort_by not in model.__table__.columns:
        raise EvaError(_("unknown order_by: %s") % sort_by)

    sort_direction = args.get('sort_direction')
    if sort_direction not in ['asc', 'desc']:
        raise EvaError(_("unknown sort_direction: %s") % sort_direction)

    order_obj = desc(sort_by) if sort_direction == 'desc' else asc(sort_by)
    return order_obj


def get_like_obj(model, args):

    like_k = args.get('like_k')
    if not like_k:
        return

    if like_k and like_k not in model.__table__.columns:
        raise EvaError(_("unknown like_k: %s") % like_k)

    like_v = args.get('like_v')
    if not like_v:
        raise EvaError(_("like_v is needed by like_k"))

    return getattr(model.__table__.columns, like_k).like("%" + like_v + "%")


def get_limit_objects(handler, model, q, args):
    '''获取对象列表

    通过过滤参数查询对象列表，如文章列表、用户列表

    列表过滤参数有：
    - sort_by, sort_direction
    - like_k, like_v
    - after, before (表示位置, 参考 graphql)
    - limit (表示范围，对象个数)
    - TODO: 使用 page ?
    '''

    # LIKE
    like_obj = get_like_obj(model, args)
    if like_obj is not None:
        q = q.filter(like_obj)

    # ORDER BY
    order_obj = get_order_obj(model, args)
    q = q.order_by(order_obj)

    # TODO: 检查 after , before 规则

    # AFTER
    after = args.get('after')
    if after:
        I = handler.db.query(model).filter_by(id=after).first()
        if I:
            q = q.filter(model.id > I.id)

    # BEFORE
    before = args.get('before')
    if before:
        I = handler.db.query(model).filter_by(id=before).first()
        if I:
            q = q.filter(model.id < I.id)

    # LIMIT
    limit = args.get('page_size')

    # Start / Stop
    if not after and not before:
        p = args.get('current_page')
        if p < 1:
            raise EvaError(_("No such page!"))

        start = (p - 1) * limit
        stop = p * limit
        q = q.slice(start, stop)

    return q.limit(limit)


def simple_list_objects(handler, model, q):
    filters = get_filters(handler)
    total = q.count()
    q = get_limit_objects(handler, model, q, filters)

    return {
        'article': [x.iuser for x in q.all()],
        'total': total,
        'filter': filters,
    }

# TODO: owner_list_objects 与 simple_list_objects 仅差显示属性 iowner vs iuser


def owner_list_objects(handler, model, q):
    filters = get_filters(handler)
    total = q.count()
    q = get_limit_objects(handler, model, q, filters)

    return {
        'data': [x.iowner for x in q.all()],
        'total': total,
        'filter': filters,
    }


def admin_list_objects(handler, model, q):
    filters = get_filters(handler)
    total = q.count()
    q = get_limit_objects(handler, model, q, filters)

    return {
        'data': [x.iadmin for x in q.all()],
        'total': total,
        'filter': filters,
    }


def get_filters(handler):
    d = {
        'sort_by': handler.get_argument('sb', "id"),
        'sort_direction': handler.get_argument('sd', "desc"),
        'like_k': handler.get_argument('lk', None),
        'like_v': handler.get_argument('lv', None),
        'after': handler.get_argument('after', None),
        'before': handler.get_argument('before', None),
        'page_size': int(handler.get_argument('lm', 12)),
        'current_page': int(handler.get_argument('p', 1)),
    }
    return {x: d[x] for x in d if d[x]}
