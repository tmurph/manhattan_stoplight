import setuptools as tools


def readme():
    with open('README.md') as f:
        return f.read()


tools.setup(
    name='manstop',
    version='0.0.0',
    description='manhattan distance with stoplights',
    url='https://github.com/tmurph/manhattan_stoplight',
    license='AGPL-3.0',
    # classifiers=['CLASSIFY ME'],
    long_description=readme(),
    author='Trevor Murphy',
    author_email='trevor.m.murphy@gmail.com',
    packages=tools.find_packages(),
    zip_safe=False,
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
