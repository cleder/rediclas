import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'redisbayes',
    ]

setup(name='rediclas',
      version='0.0',
      description='A ridiculously naive bayesian classifier using redis',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Christian Ledermann',
      author_email='christian.ledermann@gmail.com',
      url='',
      keywords='web pyramid pylons bayes redis classification',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="rediclas",
      entry_points="""\
      [paste.app_factory]
      main = rediclas:main
      """,
      )
