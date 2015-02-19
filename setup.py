from distutils.core import setup

setup(
    name='GosuGamers-API',
    version='0.2',
    packages=['gosu_gamers', 'gosu_gamers.data', 'gosu_gamers.utils'],
    package_data={'': ['*.txt'],
                  'data': ['*.txt']},
    url='https://github.com/Granitas/GosuGamers-API/',
    license='GNU GENERAL PUBLIC LICENSE',
    author='https://github.com/Granitas',
    author_email='bernardas.alisauskas@gmail.com',
    description='Unofficial API/Scraper for gosugamers.com website.'
)
