from eva.web import APIRequestHandler, authenticated
from eva.utils.translation import ugettext_lazy as _
from eva.sqlalchemy.list import admin_list_objects, get_filters

from app.blog.models import (
    BlogCategory,
)
from .forms import (
    CategoryNewForm,
)


class CategoryHandler(APIRequestHandler):

    @authenticated
    def get(self):
        '''类别列表'''

        q = self.db.query(BlogCategory)
        d = admin_list_objects(self, BlogCategory, q)
        self.success(**d)

    @authenticated
    def post(self):
        '''新建类别'''

        form = CategoryNewForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        parent = None
        if not form.parent_id.is_missing:
            parent = self.db.query(BlogCategory).filter_by(
                uid=form.parent_id.data).first()
            if not parent:
                return self.fail(_("Can not find parent category {0}").format(form.parent_id.data))

        category = BlogCategory(
            name=form.name.data,
            parent=parent,
            summary=form.summary.data,
            body=form.body.data,
            body_markup=form.body_markup.data
        )
        category.uid = BlogCategory.gen_uid(self.db)
        self.db.add(category)
        self.db.commit()

        self.success(uid=category.uid)
