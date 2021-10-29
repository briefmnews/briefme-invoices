from setuptools import setup

setup(
    name="briefme-invoices",
    version="1.1.0",
    description="Generate and download invoices",
    url="https://github.com/briefmnews/briefme-invoices",
    author="Brief.me",
    author_email="tech@brief.me",
    packages=[
        "briefme_invoices",
        "briefme_invoices.migrations",
        "briefme_invoices.templatetags",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Django>=2.2",
        "django-weasyprint>=0.5",
        "weasyprint==52.5",
        "requests>=2.25",
        "python-dateutil>=2.8",
        "django-model-utils>=4.1",
        "django-braces>=1.14",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    zip_safe=False,
)
