# -*- encoding: utf-8 -*-
"""
django-thumbs by Antonio Melé
http://django.es
"""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.core.files.base import ContentFile

from PIL import Image

def generate_thumb(img, thumb_size, format, exact_size=False, processor=None):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail

    Parameters:
    ===========
    img         File object

    thumb_size  desired thumbnail size, ie: (200,120)

    format      format of the original image ('jpeg','gif','png',...)
                (this format will be used for the generated thumbnail, too)
    """

    img.seek(0) # see http://code.djangoproject.com/ticket/8222 for details
    read_buffer = StringIO()
    read_buffer.write(img.read())
    read_buffer.seek(0, 0)

    image = Image.open(read_buffer)

    # Convert to RGB if necessary
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')

    # get size
    thumb_w, thumb_h = thumb_size
    # If you want to keep the exact size
    if exact_size and thumb_w != thumb_h:
        wsize,hsize = image.size

        ratio_thumb = float(thumb_w) / float(thumb_h)
        ratio_image = float(wsize) / float(hsize)

        if ratio_thumb < ratio_image:
            # crop w, keep h
            ratio = float(hsize) / float(thumb_h)
            xnewsize = int(thumb_w * ratio)
            ynewsize = hsize
        elif ratio_thumb > ratio_image:
            # crop h, keep w
            ratio = float(wsize) / float(thumb_w)
            xnewsize = wsize
            ynewsize = int(thumb_h * ratio)
        else:
            xnewsize = wsize
            ynewsize = hsize

        xcenter = (wsize - xnewsize) / 2
        ycenter = (hsize - ynewsize) / 2

        image2 = image.crop((xcenter, ycenter, xnewsize + xcenter, ynewsize + ycenter))
        image2.load()

        image2.thumbnail(thumb_size, Image.ANTIALIAS)
    # If you want to generate a square thumbnail
    elif thumb_w == thumb_h:
        # quad
        xsize, ysize = image.size
        # get minimum size
        minsize = min(xsize,ysize)
        # largest square possible in the image
        xnewsize = (xsize-minsize) / 2
        ynewsize = (ysize-minsize) / 2
        # crop it
        image2 = image.crop((xnewsize, ynewsize, xsize-xnewsize, ysize-ynewsize))
        # load is necessary after crop
        image2.load()
        # thumbnail of the cropped image (with ANTIALIAS to make it look better)
        image2.thumbnail(thumb_size, Image.ANTIALIAS)
    else:
        # not quad
        image2 = image
        image2.thumbnail(thumb_size, Image.ANTIALIAS)

    # Apply processors now
    # Please not that the funny 'or image2' is put into place for
    # process methods that return None instead of the new image.
    # In this case, the image was edited in place.
    if processor:
        if hasattr(processor, '__iter__'):
            for processor_part in processor:
                image2 = processor_part.process(image2) or image2
        else:
            image2 = processor.process(image2) or image2

    io = StringIO()
    # PNG and GIF are the same, JPG is JPEG
    if format.upper()=='JPG':
        format = 'JPEG'

    image2.save(io, format)
    read_buffer.close()
    return ContentFile(io.getvalue())

class ImageWithThumbsFieldFile(ImageFieldFile):
    """
    See ImageWithThumbsField for usage example
    """
    def _thumbname(self, size, processor=None):
        '''
        Generate the thumbnail name (make name.extension and turn it into
        name.HEIGHTxWIDTH.extension)
        '''
        if self.name == '':
            return ''
        w,h,exact_size = self._parse_size(size)
        name,extension = self.name.rsplit('.',1)
        if processor is None:
            return '%s.%sx%s.%s' % (name, w, h, extension)
        else:
            return '%s.%sx%s.%s.%s' % (name, w, h, processor, extension)

    def _parse_size(self, size):
        'Parse the size make it "width, height, exact size"'
        if len(size) == 3:
            (w,h,exact_size) = size
        elif len(size) == 2:
            (w,h) = size
            exact_size = False
        else:
            raise Exception('Size should be a tuple of 2 or 3 items.')
        return w,h,exact_size

    def __getattr__(self, name):
        if name.startswith('url_'):
            underscore_splitted = name[4:].split('_')
            size = map(int, underscore_splitted[0].split('x'))
            processor = underscore_splitted[1] if len(underscore_splitted) > 1 else None
            try:
                return self.storage.url(self._thumbname(size, processor=processor))
            except:
                return ''
        else:
            return super(ImageWithThumbsFieldFile, self).__getattr__(name)

    @property
    def names(self):
        names = []
        if not self.field.delete_original_file:
            names.append(self.name)
        names.extend([self._thumbname(size) for size in self.field.sizes])
        if self.field.processors:
            for processor in self.field.processors.iteritems():
                names.extend([self._thumbname(size, processor[0]) for size in self.field.sizes])
        return names

    @property
    def files(self):
        return [self.storage.open(n) for n in self.names]

    def _generate_thumbs(self, processor_tuple=None):
        if self.field.sizes:
            content = self.file

            # This used to be open/close, but now it's just open. Why?  Take a seat. Since Django
            # 1.7 this file field can be backed by a InMemoryUploadedFile object. This uses Python's
            # BytesIO instead of an actual file - but here's the thing: it doesn't have an `open()`
            # method, but it has a `close()` method. Django overrides the `open()` with a
            # `seek(0)`. Once it's closed (which is just setting a flag - it's not an actual file)
            # there's no way to open it again or perform any operations. Closing here will cause an
            # error when it is called twice (which happens). In summary, it's all a big mess and
            # it's not our fault.
            content.open()
            for size in self.field.sizes:
                w,h,exact_size = self._parse_size(size)
                name,extension = self.name.rsplit('.',1)
                thumb_name = self._thumbname(size, processor=processor_tuple and processor_tuple[0])

                thumb_content = generate_thumb(content, (w,h), extension, exact_size,
                                               processor=processor_tuple and processor_tuple[1])
                thumb_name_ = self.storage.save(thumb_name, thumb_content)

                if not thumb_name == thumb_name_:
                    raise ValueError('There is already a file named %s' % thumb_name)

            # delete original file if needed
            if self.field.delete_original_file:
                self.storage.delete(self.name)

    def save(self, name, content, save=True):
        super(ImageWithThumbsFieldFile, self).save(name, content, save)

        self._generate_thumbs()
        if self.field.processors:
            for processor_tuple in self.field.processors.iteritems():
                self._generate_thumbs(processor_tuple=processor_tuple)

    def delete(self, save=True):
        name = self.name
        if self.field.sizes:
            for size in self.field.sizes:
                thumb_name = self._thumbname(size)
                try:
                    self.storage.delete(thumb_name)
                except:
                    pass
        super(ImageWithThumbsFieldFile, self).delete(save)

class ImageWithThumbsField(ImageField):
    attr_class = ImageWithThumbsFieldFile
    """
    Usage example:
    ==============
    photo = ImageWithThumbsField(upload_to='images', sizes=((125,125),(300,200),)

    To retrieve image URL, exactly the same way as with ImageField:
        my_object.photo.url
    To retrieve thumbnails URL's just add the size to it:
        my_object.photo.url_125x125
        my_object.photo.url_300x200

    Note: The 'sizes' attribute is not required. If you don't provide it,
    ImageWithThumbsField will act as a normal ImageField

    How it works:
    =============
    For each size in the 'sizes' atribute of the field it generates a
    thumbnail with that size and stores it following this format:

    available_filename.[width]x[height].extension

    Where 'available_filename' is the available filename returned by the storage
    backend for saving the original file.

    Following the usage example above: For storing a file called "photo.jpg" it saves:
    photo.jpg          (original file)
    photo.125x125.jpg  (first thumbnail)
    photo.300x200.jpg  (second thumbnail)

    With the default storage backend if photo.jpg already exists it will use these filenames:
    photo_.jpg
    photo_.125x125.jpg
    photo_.300x200.jpg

    Note: django-thumbs assumes that if filename "any_filename.jpg" is available
    filenames with this format "any_filename.[widht]x[height].jpg" will be available, too.

    To do:
    ======
    Add method to regenerate thubmnails

    """
    def __init__(self, name=None, width_field=None, height_field=None, sizes=None, delete_original_file=False, processors=None, **kwargs):
        self.name=name
        self.width_field=width_field
        self.height_field=height_field
        self.sizes = sizes
        self.delete_original_file = delete_original_file
        self.processors = processors
        super(ImageField, self).__init__(**kwargs)

try:
    import south
except ImportError:
    pass
else:
    rules = [(
        (ImageWithThumbsField,),
        [],
        {
            'sizes': ['sizes', {'default': ()}],
            'delete_original_file': ['delete_original_file', {'default': False}],
            'processors': ['processors', {'default': None}],
            'upload_to': ['upload_to', {'default': None}],
            'height_field': ['height_field', {'default': None}],
            'width_field': ['width_field', {'default': None}],
            'max_length': ['max_length', {'default': 100}],
        }
    )]
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(rules, ["^cl_utils\.thumbs"])
