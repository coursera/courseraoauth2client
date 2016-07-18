from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='courseraoauth2client',
      version='0.0.1',
      description='An OAuth2 client for the Coursera App Platform.',
      long_description=readme(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2.7',
      ],
      keywords='coursera sdk cli tool oauth2',
      url='https://github.com/coursera/courseraoauth2client',
      author='Chris Liu',
      author_email='cliu@coursera.org',
      license='Apache',
      entry_points={
          'console_scripts': [
              'courseraoauth2client = courseraoauth2client.main:main',
          ],
      },
      packages=['courseraoauth2client', 'courseraoauth2client.commands'],
      install_requires=[
          'requests>=2.7.0',
          'semver>=2.2.0',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      zip_safe=False)
