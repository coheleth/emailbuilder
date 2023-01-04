from setuptools import find_packages, setup
README = open('README.md').read()

setup(
    name='emailbuilder',
    packages=find_packages(exclude=['test']),
    python_requires='>3.7',
    version='0.1.0',
    description='Simple HTML e-mail generator',
    long_description_content_type="text/markdown",
    long_description=README,
    author='Coheleth',
    license='MIT',
    url='https://github.com/coheleth/emailbuilder',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    # test_suite='tests'
)
