django-parsley
==============

.. image:: https://img.shields.io/pypi/dm/django-parsley.svg
    :target: https://pypi.python.org/pypi/django-parsley
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/django-parsley.svg
    :target: https://pypi.python.org/pypi/django-parsley
    :alt: Latest Release

.. image:: https://travis-ci.org/agiliq/Django-parsley.png?branch=master
    :target: https://travis-ci.org/agiliq/Django-parsley
    :alt: Build Status

.. image:: https://coveralls.io/repos/agiliq/Django-parsley/badge.png?branch=master
    :target: https://coveralls.io/r/agiliq/Django-parsley
    :alt: Coverage Status

What is it?
-----------

`Parsleyjs`_ is a JavaScript library to do client side data validations.
It does this in a non-intrusive way via adding a ``data-parsley-*`` attributes to form fields.

When you define a Django form, you get server side validations for free using
the form field attributes. Django-parsley adds these validations to client side, by tagging your form with ``data-parsley-*`` attributes.

Parsley plays well with ``crispy-forms`` et all.

Demo
----
`Demo`_ at https://agiliq.com/demo/parsley/


Installation
------------

1. pip install ``django-parsley`` (or add to your requirements.txt)
2. add ``parsley`` to your ``INSTALLED_APPS`` (required for static files)

Upgrading
---------

Upgrading from 0.2 to 0.3:
..........................

If you're using parsley.js 1.x, make sure to set the ``parsley_namespace`` Meta attribute
to ``parsley`` for backward compatibility.

.. code-block:: python

    class Meta:
        parsley_namespace = 'parsley'

Usage
-----

``parsley`` provides a single class decorator called ``parsleyfy``. Decorate your ``Form`` or ``ModelForm`` with ``parsleyfy`` to get the validations.

Eg.

.. code-block:: python

    from parsley.decorators import parsleyfy


    @parsleyfy
    class FieldTypeForm(forms.Form):
        name = forms.CharField(min_length=3, max_length=30)
        url = forms.URLField()
        url2 = forms.URLField(required=False)
        email = forms.EmailField()
        email2 = forms.EmailField(required=False)
        age = forms.IntegerField()
        income = forms.DecimalField()

Your rendered form's HTML will look like this

.. code-block:: html

    <p><label for="id_name">Name:</label> <input data-parsley-required="true" data-parsley-minlength="3" maxlength="30" type="text" data-parsley-maxlength="30" id="id_name" name="name" /></p>
    <p><label for="id_url">Url:</label> <input type="text" data-parsley-required="true" data-parsley-type="url" name="url" id="id_url" /></p>
    <p><label for="id_url2">Url2:</label> <input type="text" data-parsley-type="url" name="url2" id="id_url2" /></p>
    <p><label for="id_email">Email:</label> <input type="text" data-parsley-required="true" data-parsley-type="email" name="email" id="id_email" /></p>
    <p><label for="id_email2">Email2:</label> <input type="text" data-parsley-type="email" name="email2" id="id_email2" /></p>
    <p><label for="id_age">Age:</label> <input type="text" data-parsley-required="true" data-parsley-type="digits" name="age" id="id_age" /></p>
    <p><label for="id_income">Income:</label> <input type="text" data-parsley-required="true" data-parsley-type="number" name="income" id="id_income" /></p>

Note the ``data-parsley-*`` attributes.

You could also do

.. code-block:: python

    FieldTypeForm = parsleyfy(FieldTypeForm)

Which is the same thing.

Put this form inside a

.. code-block:: html

    <form data-parsley-validate>
        {{ form.as_p }}
    </form>

.. note:: Make sure `jquery.js` and `parsley.js` are included in the template.

Admin
-----

To add parsley validations to admin, use the ``ParsleyAdminMixin`` with your ``ModelAdmin`` like so:

.. code-block:: python

    class StudentAdmin(ParsleyAdminMixin, admin.ModelAdmin):
        pass

.. note:: Use the `parsley.django-admin.js` helper from parsley static to auto-validate admin forms.

Advanced Usage
--------------

In addition to the default validators if you want to add extra client side validations
or if you want to add custom validators, add a ``parsley_extras`` Meta attribute. For e.g
if you wanted to add ``minlength`` and ``equalto`` validations on a ``PasswordChangeForm``:

.. code-block:: python

    @parsleyfy
    class PasswordChangeForm(BasePasswordChangeForm):
        class Meta:
            parsley_extras = {
                'new_password1': {
                    'minlength': "5",
                },
                'new_password2': {
                    'equalto': "new_password1",
                    'error-message': "Your passwords do not match.",
                },
            }

To use a custom namespace for parsley (e.g when using parsley with the ``data-parsley-namespace``
option) you can provide a namespace by using the ``parsley_namespace`` Meta attribute.

.. code-block:: python

    class Meta:
        parsley_namespace = 'custom'

License
-------

3 Clause BSD.

Bug report and Help
-------------------

For bug reports open a github ticket. Patches gratefully accepted. Need help? `Contact us here`_

.. _parsleyjs: http://parsleyjs.org/
.. _contact us here: http://agiliq.com/contactus
.. _demo: http://agiliq.com/demo/parsley/
