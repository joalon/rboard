from setuptools import setup

setup(
    name='rboard',
    packages=['rboard'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-migrate',
        'flask-wtforms',
        'flask-login',
        'flask-sqlalchemy'
    ]
)
