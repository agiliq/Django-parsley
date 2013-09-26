django-parsley
==============

.. image:: https://travis-ci.org/agiliq/Django-parsley.png?branch=master
   :target: https://travis-ci.org/agiliq/Django-parsley
   :alt: Build Status

.. image:: https://coveralls.io/repos/agiliq/Django-parsley/badge.png?branch=master
   :target: https://coveralls.io/r/agiliq/Django-parsley
   :alt: Coverage Status

What is it?
-----------

`Parsleyjs`_ is a JavaScript library to do client side data validations.
It does this in a non-intrusive way via adding a ``data-*`` attributes to form fields.

When you define a Django form, you get server side validations for free using
the form field attributes. Django-parsley adds these validations to client side, by tagging your form with ``data-*`` attributes.

Parsley plays well with ``crispy-forms`` et all.

Installation
------------

1. pip install ``django-parsley`` (or add to your requirements.txt)
2. add ``parsley`` to your ``INSTALLED_APPS`` (required for static files added by mixin)

Usage
-----

``parsley`` provides a single class decorator called ``parsleyfy``. Decorate your ``Form`` with ``parsleyfy`` to get the validations.

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

    <p><label for="id_name">Name:</label> <input data-required="true" data-minlength="3" maxlength="30" type="text" data-maxlength="30" id="id_name" name="name" /></p>
    <p><label for="id_url">Url:</label> <input type="text" data-required="true" data-type="url" name="url" id="id_url" /></p>
    <p><label for="id_url2">Url2:</label> <input type="text" data-type="url" name="url2" id="id_url2" /></p>
    <p><label for="id_email">Email:</label> <input type="text" data-required="true" data-type="email" name="email" id="id_email" /></p>
    <p><label for="id_email2">Email2:</label> <input type="text" data-type="email" name="email2" id="id_email2" /></p>
    <p><label for="id_age">Age:</label> <input type="text" data-required="true" data-type="digits" name="age" id="id_age" /></p>
    <p><label for="id_income">Income:</label> <input type="text" data-required="true" data-type="number" name="income" id="id_income" /></p>

Note the ``data-*`` attributes.

You could also do

.. code-block:: python

    FieldTypeForm = parsleyfy(FieldTypeForm)

Which is the same thing.

Put this form inside a

.. code-block:: html

    <form data-validate="parsley">
        {{ form.as_p }}
    </form>

Include the parsleyjs and you are good to go.


Admin
-----

To add parsley validations to admin, use the ``ParsleyAdminMixin`` with your ``ModelAdmin`` like so:

.. code-block:: python

    class StudentAdmin(ParsleyAdminMixin, admin.ModelAdmin):
        pass

Note that the above mixin adds two scripts: ``parsley-standalone.min.js`` and ``parsley.django-admin.js`` to the admin media.

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

License
-------

3 Clause BSD.

Bug report and Help
-------------------

For bug reports open a github ticket. Patches gratefully accepted. Need help? `Contact us here`_

.. _parsleyjs: http://parsleyjs.org/
.. _contact us here: http://agiliq.com/contactus
