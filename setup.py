from setuptools import setup, find_packages

setup(
    name='django-betainvite',
    version='0.9',
    install_requires = [
        'django-crispy-forms>=1.1.1',
        'django-registration>=0.8',
    ],
    description='An application that handles beta invitations and restricts access to a private beta site.',
    author='Euan Lau',
    author_email='euanlau@gmail.com',
    url='https://github.com/euanlau/django-betainvite/',
    download_url='https://github.com/euanlau/django-betainvite/downloads',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    zip_safe=False,
)
