from setuptools import setup

setup(name='act',
    version='0.3',
    description='Python Distribution Utilities',
    entry_points = {
        'console_scripts': [
            'act = act:main',                  
        ],              
    },
    install_requires=[
        'psutil',
    ],
    py_modules=['act'],
)
