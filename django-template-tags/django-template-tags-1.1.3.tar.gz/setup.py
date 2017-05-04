from setuptools import setup, find_packages

setup(
    name='django-template-tags',
    version='1.1.3',
    url='https://github.com/vikingco/django-template-tags',
    license='BSD',
    description='Some general, useful template tags.',
    long_description=open('README', 'r').read(),
    author='Jonathan Slenders, Unleashed NV',
    author_email='operations@unleashed.be',
    packages=find_packages('.'),
    package_data={'django_template_tags': ['static/css/*.css', ],},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
