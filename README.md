# briefme-invoices
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-270/) 
[![Django 2.2](https://img.shields.io/badge/django-2.2-blue.svg)](https://docs.djangoproject.com/en/2.2/)
[![Build Status](https://travis-ci.org/briefmnews/briefme-invoices.svg?branch=master)](https://travis-ci.org/briefmnews/briefme-invoices)
[![codecov](https://codecov.io/gh/briefmnews/briefme-invoices/branch/master/graph/badge.svg)](https://codecov.io/gh/briefmnews/briefme-invoices)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) 

Generate and download invoices for briefme apps.  
***Caution***: this app requires a custom user model (see below)

## Installation
Install with [pip](https://pip.pypa.io/en/stable/):
```shell
pip install -e git://github.com/briefmnews/briefme-invoices.git@master#egg=briefme_invoices
```

## Setup
In order to make `briefme-invoices` works, you'll need to follow the steps below.


### Settings
First you need to add the following configuration to your settings:
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',

    'briefme_invoices',
    ...
)
```

### Url
Then you need to add the urls to your `urls.py`
```python
urlpatterns = [
    ...,
    path('compte/factures/', include('briefme_invoices.urls')),
    ...
]
```

### Migrations
Next, you need to run the migrations in order to update your database schema.
```shell
python manage.py migrate
```

### Mandatory settings
`INVOICES_PREFIX` will be used as the prefix of the invoice number
when generating an invoice.  
`INVOICES_PDF_ATTACHMENT` is whether or not you want to display (if set to `False`)
or download (if set to `True`) an invoice.


## Cutom user model
The user model needs to have at least the following fields:
```python
first_name,
last_name,
organization,
address,
zip,
city,
country
```

## Usage
You can now use the `briefme_invoices` in any other app. The following shows an example.

### Views
You can extends the views by doing the following.
```python
from briefme_invoices import views as invoices_views

class DownloadInvoiceView(invoices_views.DownloadInvoiceView):
    pass


class InvoicesListView(invoices_views.InvoicesListView):
    pass


class UpdateInvoicingInfoView(invoices_views.UpdateInvoicingInfoView):
    pass
```

### Urls
Then on the `urls.py`.
```python
from django.urls import path, include

from .views import (
    InvoicesListView,
    UpdateInvoicingInfoView,
    DownloadInvoiceView,
)

invoices_patterns = [
    path("", InvoicesListView.as_view(), name="list"),
    path("informations/", UpdateInvoicingInfoView.as_view(), name="update_info"),
    path("<int:statement_id>/download/", DownloadInvoiceView.as_view(), name="download"),
]

urlpatterns = [
    path("factures/", include(invoices_patterns)),
]
```

### Templates
All templates can be extended or overridden.


## Tests
Testing is managed by `pytest`. Required package for testing can be installed with:
```shell
pip install -r test_requirements.txt
```
To run testing locally:
```shell
pytest
```
