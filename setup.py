import setuptools

setuptools.setup(
    name="bestplace",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'flask==1.1.4',
        'flask_script',
        'flask-restx',
        'python-dotenv'
    ]
)