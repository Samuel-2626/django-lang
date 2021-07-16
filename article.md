# Add multiple language support to your Django project

Django offers multiple language support. In fact, Django is translated into more than fifty languages. In this tutorial, you will learn how to add multiple language support to your Django project.

## Objectives

By the end of this tutorial you should be able to:

1. understand the difference between internationalization and localization
1. add language prefix to URLs
1. translate templates
1. allow users to switch between languages
1. translate models
1. add locale-support

## Project Setup and Overview

This is what you will be creating from this tutorial. Though simple it would cover basic concepts to get you comfortable with adding internationalization with Django.

![Home Page](https://github.com/Samuel-2626/django-lang/blob/main/images/homepage.png)

To start, clone down the [base](https://github.com/Samuel-2626/django-lang/tree/base) branch from the [django-lang](https://github.com/Samuel-2626/django-lang) repo:

```bash
$ git clone https://github.com/Samuel-2626/django-lang --branch base --single-branch
$ cd django-lang
```

Next, install project dependencies, apply migrations and create a superuser:

```bash
$ pipenv install -r requirements.txt
$ pipenv shell
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

Take note of the `Course` model in _course/models.py_:

```python
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField()
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
```

Run the following management command to add some data to your database:

```bash
$ python manage.py add_courses
```

In the next section, we will be discussing briefly **Internationalization** and **Localization**.

## Internationalization vs localization

**Internationalization** and **localization** are rather two different terms. While **internationalization** represented by i18n enables our web application to be language agnostic (i.e it isn't fixed to any particular language) but can be used by different languages and locales, **localization** represented by l10n on the other hand is the process of translating our web application to a particular language and locale.

Recall that Django using its international framework has been translated into more than 50 languages.

> Through the international framework, we can easily mark strings for translation, both in Python code and in our templates. It makes use of the GNU gettext toolkit to generate and manage a plain text file that represents a language known as the **message file**. The message file ends with `.po` as its extension. Another file is generated for each language once the translation is done which ends with the `.mo` extension. This is known as the compiled translation.

To use this gettext toolkit, it needs to be installed. On macOS, a simple way is to install it using [Homebrew](https://brew.sh/), by running the following commands.

```bash
$ brew install gettext
$ brew link --force gettext
```

For most Linux distributions, it comes pre-installed. And finally, for Windows, the steps to install can be found [here](https://djangoproject.com/en/3.0/topics/i18n/translation/#gettext-on-windows).

In the next section, we will be preparing our project for internationalization and localization.

## Preparing your project to use Django Internationalization Framework

Django comes with some default settings when we created a new project. This can be found inside the `settings.py` file of our project under the **internationalization** section.

The first setting is the `LANGUAGE_CODE`. By default, Django set it's to the United States English (en-us). This is a locale-specific name. Let's update it to a generic name, English (en).

```py
LANGUAGE_CODE = 'en' # new
```

Others include the `USE_I18N`, `USE_L10N`, `USE_TZ` all set by default to **True** i.e. Django's translation system is enabled, the Localized format is enabled and Django is timezone aware respectively. Since they are all set to True no changes needs to be made.

Let's add some additional settings to complement the existing ones:

```py
from django.utils.translation import gettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
)
```

**What's happening here?**

1. We are specifying the languages we want our project to be available in. If this is not specified Django will assume our project to be available in all of its supported languages.

1. This LANGUAGE setting consist of the language code and the language name. Recall that the language codes can be locale-specific, such as **en-gb** or generic such as **en**.

1. Also, take note of the imports we will be using the **gettext_lazy** function to translate the language names instead of the **gettext** function. This, therefore, prevents circular imports.

Add `django.middleware.locale.LocaleMiddleware` to the MIDDLEWARE settings list. This middleware should come after the SessionMiddleware because the LocaleMiddleware needs to use the session data. It should also be placed before the CommonMiddleware because the CommonMiddleware needs will be needing active language to resolve the URLs been requested. Hence, the order is very crucial.

```py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

This middleware is used to determine the current language based on the request data.

Add a locale path directory for your application where message files will reside.

```py
import os

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)
```

> Django now looks at the LOCALE_PATHS setting for translation files. Note that, Locale paths that appear first have the highest precedence.

You need to create the `locale` directory inside of your root project and a new folder for each language (en, es and fr).

Open the shell and run the following command from your project directory:

```bash
$ django-admin makemessages --all
```

A .po message file has been created for each language.

**What to know?**

1. msgid: This represents the translation string as it appears in the source code.
1. msgstr: This represents the language translation, which is empty by default. You will have to supply the actual translation for any given string.

Currently, only the `LANGUAGES` from our settings.py file have been marked for translation. Therefore for each msgstr under the **fr** directory enter the French equivalent of the word likewise for the **es** directory (Spanish equivalent).

Next, let's compile the messages by running the following commands.

```bash
$ django-admin compilemessages
```

A .mo compiled message file has been generated for each language.

## Translating templates, model fields and forms

We can translate model fields names and forms by marking them for translation using either **gettext** or **gettext_lazy** function.

Edit the `models.py` file:

```py
from django.db import models

from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    title = models.CharField(_('title'), max_length=90)
    description = models.TextField(_('description'))
    date = models.DateField(_('date'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
```

```bash
$ django-admin makemessages --all
```

Fill in the following **msgstr** translations for the French and Spanish directory and then compile the messages

```bash
$ django-admin compilemessages
```

We can also do this for forms by adding a label.

For instance:

```py
from django import forms
from django.utils.translation import gettext_lazy as _

class ExampleForm(forms.Form):
    first_name = forms.CharField(label=_('first name'))
```

To translate our templates, Django offers the `{% trans %}` and `{% blocktrans %}` template tags to translate strings. You have to add `{% load i18n %}` at the top of the HTML file to use the translation templates tags.

The `{% trans %}` template tag allows you to mark a literal for translation. How it works is that Django executes **gettext** function on the given text internally.

The `{% trans %}` tag is useful for simple translation strings, but it can't handle content for translation that includes variables.

Enter the ``{% blocktrans %}` template tag which allows you to mark content that includes literals and variables.

> Use the {% blocktrans %} tag instead of {% trans %} when you need to include variable context in your HTML file.

Update the `index.html` file inside the templates folder to see this in action:

```html
<!-- # new -->
<title>{% trans "TestDriven.io" %}</title>

<!-- # new -->
<h1>{% "TestDriven.io Courses" %}</h1>
```

```bash
$ django-admin makemessages --all
```

Fill in the following **msgstr** translations for the French and Spanish directory and then compile the messages

```bash
$ django-admin compilemessages
```

## Using Rosetta Translation Interface

We will be using a third-party library called **Rosseta**. Rosetta is a third-party application that allows you to edit translations using the same interface as the Django administration site. It makes it easy to edit .po files and it updates compiled translation files automatically for you.

Rosetta has already been installed as part of the dependencies, therefore, all you need to do is to add it as part of your installed apps

```py
INSTALLED_APPS = [
    'rosetta', # new
]
```

You will also need to add Rosetta's URL to your main URL configuration. Edit the main `urls.py` file of your project and add the following URL pattern to it. Make sure it comes after the admin.

```py
path('rosetta/', include('rosetta.urls')), # new
```

Navigate to [http://127.0.0.1:8080/rosetta/](http://127.0.0.1:8080/rosetta/) in your browser.

![Rosetta Homepage](https://github.com/Samuel-2626/django-lang/blob/main/images/rosetta-homepage.png)

Under the projects, click on each application to edit translations.

![Rosetta French](https://github.com/Samuel-2626/django-lang/blob/main/images/rosetta-french.png)

When you finish editing translations, click the **Save and translate next block** button to save the translations to the .po file.

Rosetta compiles the message file when you save translations, so there is no need for you to run the compilemessages command.

> Note that after you add new translations in a production environment you will have to reload your server after running the compilemessages command, or after saving the translations with Rosetta, for changes to take effect.

## Add language prefix to URLs

Django using its internationalization framework gives us the ability to serve each language version under a different URL extension. For instance, the English version of your site can be served under **/en/**, the French version can be served under **/fr/** and so on. This approach makes our site optimized for search engines as each URL will be indexed for each language which in turn will rank better for each language. To use this Django internationalization framework needs to identify the current language from the requested URL, therefore, the **LocalMiddleware** needs to be added in the MIDDLEWARE setting of your project, this has been done before.

Edit the main `urls.py` file of the `django-lang` project and add the `i18n_patterns` function:

```py
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('', include('course.urls')),
)
```

Run the development server and open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. you will be redirected to the requested URL, including the language prefix. Take a look at the URL in your browser; it should now look like [http://127.0.0.1:8000/en/](http://127.0.0.1:8000/en/).

> Change the requested URL from **en** to **fr** or to **es** and see as the heading changes.

## Translating our models

Django internationalization framework doesn't support translating our models out of the box, therefore we will be using a third-party library called `django-parler`. There are a plethora number of plugins that performs this function, however, this is one of the most popular plugins that allow us to translate our models.

**How does it work?**

`django-parler` will create a separate database table for each model that contains translations. This table includes all the translated fields. It also has a foreign key to link to the original object.

`django-parler` has already been installed as part of the dependencies, therefore, all you need to do is to add it as part of your installed apps

```py
INSTALLED_APPS = [
    # new
    'parler',
]
```

Also, add the following code to your settings:

```py
PARLER_LANGUAGES = {
    None: (
        {'code': 'en',}, # English
        {'code': 'fr',}, # French
        {'code': 'es',}, # Spanish
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}
```

You defined the available languages (English, French, Spanish) for `django-parler`. You also specify English to be the default language and finally indicate that `django-parler` should not hide untranslated content.

**What to know?**

1. `django_parler` provides a **TranslatableModel** model class and a **TranslatedFields** wrapper to translate model fields.

1. `django_parler` manages translations by generating another model for each translatable model.

> Note that, because Django uses a separate table for translations, there will be some Django features that you can't use.

Also, this migration will delete the previous records in your database. Edit the `models.py` file to look like this.

```py
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Course(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=90),
        description=models.TextField(),
        date=models.DateField(),
        price=models.DecimalField(max_digits=10, decimal_places=2),
    )

    def __str__(self):
        return self.title
```

Next, apply makemigraions:

```bash
$ python manage.py makemigrations
```

Before proceeding, edit the file migrations/002_translations.py of the course application and replace this code:

```py
bases = (parler.models.TranslatableFieldsModelMixin, models.Model) # old
```

with the following one:

```py
bases = (parler.models.TranslatableModel, models.Model) # new
```

> There happen to be a minor issue found in `django-parler` that we just resolved. Failing to do this will prevent migrations from applying.

Next, apply migrations :

```bash
$ python manage.py migrate
```

One of the awesome features of `django_parler` is that it integrates smoothly with the Django administration site. It includes a **TranslatableAdmin** class that overrides the ModelAdmin class provided by Django to manage translations. T

Edit the `admin.py` of the course directory to look like this.

```py
from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Course

admin.site.register(Course, TranslatableAdmin)
```

Run the following management command to add some data again to your database:

```bash
$ python manage.py add_courses
```

Navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in your browser.

![Admin 1](https://github.com/Samuel-2626/django-lang/blob/main/images/admin-1.png)

For each data, a separate field for each language is created. Add the different translations for each language and save them.

![Admin 2](https://github.com/Samuel-2626/django-lang/blob/main/images/admin-2.png)

## Allowing users to switch languages

In this section, we will be allowing users the ability to switch between languages from our homepage.

Edit the `index.html` file to look like this:

```html
{% load i18n %}

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
            rel="stylesheet"
            integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
            crossorigin="anonymous"
        />
        <title>{% trans "TestDriven.io" %}</title>
        <style>
            h1, h3 {
                color: tomato;
            }
            li {
                display: inline;
                text-decoration: none;
                padding: 5px;
            }
            a {
                text-decoration: none;
                color: brown;
            }
            .active {
                background-color: tomato;
                padding: 2px;
                text-align: center;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{% trans "TestDriven.io Courses" %}</h1>

            {% get_current_language as LANGUAGE_CODE %}
            {% get_available_languages as LANGUAGES %}
            {% get_language_info_list for LANGUAGES as languages %}
            <div class="languages">
                <p>{% trans "Language" %}:</p>
                <ul class="languages">
                {% for language in languages %}
                    <li>
                    <a href="/{{ language.code }}/"
                    {% if language.code == LANGUAGE_CODE %} class="active"{% endif %}>
                        {{ language.name_local }}
                    </a>
                    </li>
                {% endfor %}
                </ul>

            {% for course in courses %}
            <h3>
                {{ course.title }}
                <em style="font-size: small">{{ course.date }}</em>
            </h3>
            <p>{{ course.description }}</p>
            <strong>
                Price: $ {{ course.price }}
            </strong>
            <hr />
            {% empty %}
            <p>Database is empty</p>
            {% endfor %}
        </div>
    </body>
</html>
```

> Make sure that no template tag is split across multiple lines.

**What's happening here?**

1. you loaded the internationalization tags using {% load i18n %}
1. you used the {% get_current_language %} tag to retrieve the current language.
1. you also got the languages defined in the LANGUAGES setting by using the {% get_available_languages %} template tag.
1. you then use the tag {% get_language_info_list %} to enable you with easy access to the language attributes.
1. and finally, you build an HTML list to display all available languages and you also added an active class attribute to the currently active language to highlight the active language.

Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to see the changes. Switch between the multiple languages and also note how the URL prefix changes for each language. In the next section, we will wrap up this tutorial by taking a look at locale-specific-support

## Add Locale-Support

In the previous section, you have seen localization. When `USE_L10N` is enabled which is enabled by default, Django will try to use a locale-specific format whenever it outputs a value in a template. Therefore, dates, times and numbers will be in different formats based on the user's locale.

Navigate back to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to see the changes and you will notice that the date format changes, as well as the decimal numbers in the English version of your site, are displayed with a dot separator for decimal places, while in the Spanish and French version, they are displayed using a comma. This is due to the locale formats specified for the es locale by Django.

## Conclusion

In this tutorial, you learnt about internationalization and localization. How to make strings for translation. We also used third-party packages like Rosetta to make updating and compiling message files easy and django-parler to translate our models.

Grab the complete code from the [repo](https://github.com/Samuel-2626/django-lang).
