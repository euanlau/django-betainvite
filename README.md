django-betainvite
=================

This is an application that restricts a beta site to invited users only,
lets potential users to subscribe to a waiting list for invitations,
and allows existing users to invite their friends to join the service.

This application is written based on django-invitation and django-privatebeta.

Overview
-------------------------
This application has 3 features that are common on a private beta site.

1. Access is restricted to invited or registered users only.
2. Sign-up waitlist subscription
3. Existing users can invite friends to join the service. 

Requirements
-------------------------
In order to use django-betainvite, you will need to have a
functioning installation of Django 1.4 or newer;

**The django-registration application is required in order to use 
django-betainvite.**

Installation
-------------------------
Install latest stable version into your python path using pip or easy_install:

```Shell
pip install --upgrade django-betainvite
```

Add betainvite to your INSTALLED_APPS in settings.py:

```Shell
INSTALLED_APPS = (
    ...
    'betainvite',
)
```

Add 'betainvite.middleware.BetaMiddleware' to your MIDDLEWARE_CLASSES in settings.py:

```Shell
MIDDLEWARE_CLASSES = (
    ...
    'betainvite.middleware.BetaMiddleware',
)
```

Configurations
-------------------------
WIP
