import setuptools

setuptools.setup(
    name="bestplace",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'flask',
        'flask_script',
        'flask-restx',
    ]
)