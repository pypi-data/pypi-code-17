import os
import logging
import hashlib

from sqlalchemy import and_, or_, desc

from eva.conf import settings
from eva.utils.translation import ugettext_lazy as _

from .models import OSSObject, OSSUserObject


def save_single_file(db, filedata, user):

    # TODO: fix me!
    tp = os.path.join(settings.OSS_PATH, str(user.uid))
    if not os.path.isdir(tp):
        try:
            os.makedirs(tp)
            logging.info('create oss storage path: %s', tp)
        except Exception as e:
            logging.error('create oss path failed: %s', e)
            return None, _("Create OSS path failed!")

    for f in filedata:
        h = hashlib.sha1()
        h.update(f['body'])
        checksum = h.hexdigest()

        save_to = os.path.join(settings.OSS_PATH, "{0}".format(checksum))

        # OOSObject 是否存在
        obj = db.query(OSSObject).filter_by(checksum=checksum).first()
        if obj:
            logging.debug('OSSObject %s is existed, pass create', checksum)
        else:
            # 创建 obj
            try:
                open(save_to, 'wb').write(f['body'])
                logging.debug('save OSSObject %s success', save_to)
            except Exception as e:
                logging.error('save OSSObject failed: %s', e)
                return None, _("save OSSObject failed!")

            obj = OSSObject(size=len(f['body']), checksum=checksum)
            obj.uid = OSSObject.gen_uid(db)
            db.add(obj)
            db.commit()

        # OSSUserObject 关联是否存在
        user_obj = db.query(OSSUserObject).filter(
            and_(OSSUserObject.user_id == user.id,
                 OSSUserObject.obj_id == obj.id)).first()
        if user_obj:
            logging.warning('OSSUserObject %s is existed', user_obj.uid)
        else:
            # 创建用户关联
            user_obj = OSSUserObject(user=user, obj=obj, filename=f['filename'])
            user_obj.uid = OSSUserObject.gen_uid(db)
            db.add(user_obj)
            db.commit()

            # 创建硬连接
            user_obj_save_to = os.path.join(tp, "{0}_{1}".format(obj.checksum, user_obj.filename))
            os.link(save_to, user_obj_save_to)

        return user_obj, None

    return None, _("Can not find any files!")
