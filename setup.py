from setuptools import find_packages, setup
setup(
    name='emailbuilder',
    packages=find_packages(exclude=['test']),
    python_requires='>3.7',
    version='0.1.0',
    description='Simple HTML e-mail generator',
    author='Coheleth',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
