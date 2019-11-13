from setuptools import setup

setup(
    name="briefme-invoices",
    version="0.1.1",
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
    install_requires=["Django>=2.2", "django-weasyprint>=0.5"],
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
