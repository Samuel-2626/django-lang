# Supporting Multiple Languages in Django

Django offers multiple language support. In fact, Django is translated into more than 100 languages. This tutorial looks at how to add multiple language support to your Django project.

## Objectives

By the end of this tutorial, you should be able to:

1. Explain the difference between internationalization and localization
1. Add language prefix to URLs
1. Translate templates
1. Allow users to switch between languages
1. Translate models
1. Add locale-support

## Project Setup

Here's a quick look at the app you'll be building:

![Home Page](https://github.com/Samuel-2626/django-lang/blob/main/images/homepage.png)

It may look simple, but it will get you comfortable with adding internationalization to Django.

To start, clone down the [base](https://github.com/Samuel-2626/django-lang/tree/base) branch from the [django-lang](https://github.com/Samuel-2626/django-lang) repo:

```bash
$ git clone https://github.com/Samuel-2626/django-lang --branch base --single-branch
$ cd django-lang
```

Next, create and activate a virtual environment, install the project's dependencies, apply migrations, and create a superuser:

```bash
$ python3.9 -m venv env
$ source env/bin/activate

(env)$ pip install -r requirements.txt
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py createsuperuser
```

> Feel free to swap out virtualenv and Pip for [Poetry](https://python-poetry.org/) or [Pipenv](https://pipenv.pypa.io/).

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

In the next section, we'll look briefly at internationalization and localization.

## Internationalization vs Localization

Internationalization and localization represent two sides to the same coin. Together, they allow you to deliver your web application's content to different locales:

-   Internationalization, represented by i18n (18 is the number of letters between i and n), is the processing of developing your application so that it can be used by different locales. This process is generally handled by developers.
-   Localization, represented by l10n (10 is the number of letters between l and n), on the other hand, is the process of translating your application to a particular language and locale. This is generally handled by translators.

> For more, review [Localization vs. Internationalization](https://www.w3.org/International/questions/qa-i18n) from W3C.

Recall that Django using its [internationalization framework](https://github.com/django/django/tree/main/django/utils/translation) has been translated into more than 100 languages:

TODO: can you provide a link to the "internationalization framework"? Done: By the way, I am not too sure if Django is translated to more than 100 languages...curious how you got that fact :)

Through the internationalization framework, we can easily mark strings for translation, both in Python code and in our templates. It makes use of the GNU gettext toolkit to generate and manage a plain text file that represents a language known as the **message file**. The message file ends with `.po` as its extension. Another file is generated for each language once the translation is done which ends with the `.mo` extension. This is known as the compiled translation.

TODO: is the above aside a quote from somewhere? Yes and No, It was from one of my favourite Django books but I did paraphrase and not quote it verbatim. What are your thoughts on this.

Let's start by installing the [gettext](https://www.gnu.org/software/gettext/) toolkit.

On macOS, it's recommended to use [Homebrew](https://brew.sh/):

```bash
$ brew install gettext
$ brew link --force gettext
```

For most Linux distributions, it comes pre-installed. And finally, for Windows, the steps to install can be found [here](https://djangoproject.com/en/3.0/topics/i18n/translation/#gettext-on-windows).

In the next section, we'll prepare our Django project for internationalization and localization.

## Django's Internationalization Framework

Django comes with some default internationalization settings in the _settings.py_ file:

```python
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

The first setting is the `LANGUAGE_CODE`. By default, it's set to United States English (en-us). This is a locale-specific name. Let's update it to a generic name, English (en).

```python
LANGUAGE_CODE = 'en'
```

> See [list of language identifiers](http://www.i18nguy.com/unicode/language-identifiers.html) for more.

For the [LANGUAGE_CODE](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-LANGUAGE_CODE) to take effect, [USE_I18N](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-USE_I18N) must be `True`, which enables Django’s translation system.

Take note of the remaining settings:

```python
TIME_ZONE = 'UTC'

USE_L10N = True

USE_TZ = True
```

Notes:

1. 'UTC' is the default [TIME_ZONE](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-TIME_ZONE)
1. Since [USE_L10N](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-USE_L10N) is set to `True`, Django will display numbers and dates using the format of the current locale
1. Finally, when [USE_TZ](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-USE_TZ) is `True`, datetimes will be timezone-aware

Let's add some additional settings to complement the existing ones:

```python
from django.utils.translation import gettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
)
```

**What's happening here?**

1. We specified the languages we want our project to be available in. If this is not specified, Django will assume our project should be available in all of its supported languages.
1. This [LANGUAGE](https://docs.djangoproject.com/en/3.2/ref/settings/#languages) setting consists of the language code and the language name. Recall that the language codes can be locale-specific, such as 'en-gb' or generic such as 'en'.
1. Also, `gettext_lazy` is used to translate the language names instead of the `gettext` to prevents circular imports.

Add `django.middleware.locale.LocaleMiddleware` to the `MIDDLEWARE` settings list. This middleware should come after the `SessionMiddleware` because the `LocaleMiddleware` needs to use the session data. It should also be placed before the `CommonMiddleware` because the `CommonMiddleware` needs the active language to resolve the URLs being requested. Hence, the order is very important.

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

Add a locale path directory for your application where message files will reside:

```python
LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]
```

> Django now looks at the [LOCALE_PATHS](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-LOCALE_PATHS) setting for translation files. Keep in mind that locale paths that appear first have the highest precedence.

You need to create the "locale" directory inside of your root project and add a new folder for each language:

```bash
locale
├── en
├── es
└── fr
```

Open the shell and run the following command from your project directory to create a _.po_ message file for each language:

```bash
(env)$ django-admin makemessages --all
```

You should now have:

```bash
locale
├── en
│   └── LC_MESSAGES
│       └── django.po
├── es
│   └── LC_MESSAGES
│       └── django.po
└── fr
    └── LC_MESSAGES
        └── django.po
```

Take note of one of the _.po_ message files:

1. `msgid`: represents the translation string as it appears in the source code.
1. `msgstr`: represents the language translation, which is empty by default. You will have to supply the actual translation for any given string.

Currently, only the `LANGUAGES` from our _settings.py_ file have been marked for translation. Therefore, for each `msgstr` under the "fr" and "es" directories, enter the French or Spanish equivalent of the word manually, respectively. Or better still, you can use [Poedit](https://poedit.net/) to edit translations. According to Poedit it was built to handle tanslation using gettext (PO). Download and install it.

Next, click on browse files and navigate to each directory for the French and Spanish .po message files:

![Poedit 1](https://github.com/Samuel-2626/django-lang/blob/main/images/poedit_1.png)

Next, double click on each translation after which you can save it. This should automatically update your .po message files.

![Poedit 2](https://github.com/Samuel-2626/django-lang/blob/main/images/poedit_2.png)

TODO: this is a manual process? Found a better way, check above :]

Next, let's compile the messages by running the following commands:

```bash
(env)$ django-admin compilemessages
```

A _.mo_ compiled message file has been generated for each language:

```bash
locale
├── en
│   └── LC_MESSAGES
│       ├── django.mo
│       └── django.po
├── es
│   └── LC_MESSAGES
│       ├── django.mo
│       └── django.po
└── fr
    └── LC_MESSAGES
        ├── django.mo
        └── django.po
```

TODO: can you provide a quick summary of what we've accomplished thus far?

**What did we achieve from this section**

You prepped out your Django project for internationalization by adding additional settings to our existing settings.py file. You also create a locale directory where all your files that are marked for translations will reside.

> The most important point to take away from the section is we need to first make strings for translation using either the gettext_lazy or gettext function, before compiling our translations.

## Translating Templates, Models, and Forms

You can translate model fields names and forms by marking them for translation using either the `gettext` or `gettext_lazy` function:

Edit the _course/models.py_ file like so:

```python
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
(env)$ django-admin makemessages --all
```

Fill in the following `msgstr` translations for French and Spanish either manually or using the Poedit interface, and then compile the messages

```bash
(env)$ django-admin compilemessages
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

The `{% trans %}` template tag allows you to mark a literal for translation. Django simply executes the `gettext` function on the given text internally.

The `{% trans %}` tag is useful for simple translation strings, but it can't handle content for translation that includes variables.

Enter the ``{% blocktrans %}` template tag which allows you to mark content that includes literals and variables.

> Use the {% blocktrans %} tag instead of {% trans %} when you need to include variable context in your HTML file.

Update the _course/templates/index.html_ file to see this in action:

```html
<!-- # new -->
<title>{% trans "TestDriven.io" %}</title>

<!-- # new -->
<h1>{% "TestDriven.io Courses" %}</h1>
```

TODO: did you mean to use `blocktrans` here? Nope as per the usecase for both, what I am translating doesn't have a variable.

Don't forget to add `{% load i18n %}` to the top of the file.

```bash
(env)$ django-admin makemessages --all
```

Fill in the following `msgstr` translations again and then compile the messages

```bash
(env)$ django-admin compilemessages
```

## Using Rosetta Translation Interface

We'll be using a third-party library called [Rosetta](https://github.com/mbi/django-rosetta) to edit translations using the same interface as the Django administration site. It makes it easy to edit _.po_ files and it updates compiled translation files automatically for you.

Rosetta has already been installed as part of the dependencies; therefore, all you need to do is to add it to your installed apps:

```py
INSTALLED_APPS = [
    'rosetta', # new
]
```

You'll also need to add Rosetta's URL to your main URL configuration in _django_lang/urls.py_:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('', include('course.urls')),
]
```

Create and apply the migrations, and then run the server:

```bash
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

Make sure you're logged in as an admin, and then navigate to [http://127.0.0.1:8000/rosetta/](http://127.0.0.1:8000/rosetta/) in your browser:

![Rosetta Homepage](https://github.com/Samuel-2626/django-lang/blob/main/images/rosetta-homepage.png)

Under the projects, click on each application to edit translations.

![Rosetta French](https://github.com/Samuel-2626/django-lang/blob/main/images/rosetta-french.png)

When you finish editing translations, click the "Save and translate next block" button to save the translations to the respective _.po_ file. Rosetta will then compile the message file, so there's no need to manually run the `django-admin compilemessages` command.

> Note that after you add new translations in a production environment, you'll have to reload your server after running the `django-admin compilemessages` command or after saving the translations with Rosetta, for changes to take effect.

## Add Language Prefix to URLs

With Django's internationalization framework, you can serve each language version under a different URL extension. For instance, the English version of your site can be served under `/en/`, the French version under `/fr/`, and so on. This approach makes the site optimized for search engines as each URL will be indexed for each language, which in turn will rank better for each language. To do this, the Django internationalization framework needs to identify the current language from the requested URL; therefore, the `LocalMiddleware` needs to be added in the `MIDDLEWARE` setting of your project, which we've already done.

Next, add the `i18n_patterns` function to _django_lang/urls.py_:

Edit the main `urls.py` file of the `django-lang` project and add the `i18n_patterns` function:

```py
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('', include('course.urls')),
)
```

Run the development server again, and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. You will be redirected to the requested URL, with the appropriate language prefix. Take a look at the URL in your browser; it should now look like [http://127.0.0.1:8000/en/](http://127.0.0.1:8000/en/).

> Change the requested URL from `en` to `fr` or to `es` and see as the heading and title changes.

## Translating Models with django-parler

Django's internationalization framework doesn't support translating models out-of-the-box, so we'll use a third-party library called [django-parler](https://github.com/django-parler/django-parler). There are a plethora number of [plugins](https://djangopackages.org/grids/g/model-translation/) that performs this function; however, this is one of the more popular ones.

**How does it work?**

`django-parler` will create a separate database table for each model that contains translations. This table includes all of the translated fields. It also has a foreign key to link to the original object.

`django-parler` has already been installed as part of the dependencies, so just add it to your installed apps:

```py
INSTALLED_APPS = [
    # new
    'parler',
]
```

Also, add the following code to your settings:

```python
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

Here, you defined the available languages (English, French, Spanish) for `django-parler`. You also specified English as the default language and indicated that `django-parler` should not hide untranslated content.

TODO: what does "hide untranslated content" mean? Maybe provide a link to the docs? This is it from the docs https://django-parler.readthedocs.io/en/stable/configuration.html#parler-languages. Just noticed that it is even the default behaviour in the first place, so I think that it can be remove; thoughts?

**What to know?**

1. `django_parler` provides a `TranslatableModel` model class and a `TranslatedFields` wrapper to translate model fields.
1. `django_parler` manages translations by generating another model for each translatable model.

> Note that, because Django uses a separate table for translations, there will be some Django features that you can't use.

Also, this migration will delete the previous records in your database.

Update _course/models.py_ again to look like this:

```python
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

Next, create the migrations:

```bash
(env)$ python manage.py makemigrations
```

Before proceeding, replace the following line in the newly created migration file:

```python
bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
```

With the following one:

```python
bases = (parler.models.TranslatableModel, models.Model)
```

> There happens to be a minor [issue](https://github.com/django-parler/django-parler/issues/157) found in django-parler that we just resolved. Failing to do this will prevent migrations from applying. TODO: can you provide a link to the issue?

Next, apply the migrations:

```bash
(env)$ python manage.py migrate
```

One of the awesome features of django_parler is that it integrates smoothly with the Django administration site. It includes a `TranslatableAdmin` class that overrides the `ModelAdmin` class provided by Django to manage translations.

Edit _course/admin.py_ like so:

```python
from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Course

admin.site.register(Course, TranslatableAdmin)
```

Run the following management command to add some data again to your database:

```bash
(env)$ python manage.py add_courses
```

Run the server, and then navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in your browser.

![Admin 1](https://github.com/Samuel-2626/django-lang/blob/main/images/admin-1.png)

For each course, a separate field for each language is now available. Add the different translations for each language and save them.

![Admin 2](https://github.com/Samuel-2626/django-lang/blob/main/images/admin-2.png)

> Note that we barely scratched the surface on what `django-parler` can achieve for us. Please refer to the [docs](https://django-parler.readthedocs.io/en/stable/index.html) to learn more.

## Allowing Users to Switch Languages

In this section, we'll show how to allow users the ability to switch between languages from our homepage.

Edit the _index.html_ file to like so:

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
                color: #266150;
            }
            li {
                display: inline;
                text-decoration: none;
                padding: 5px;
            }
            a {
                text-decoration: none;
                color: #DDAF94;
            }
            a:hover {
                color: #4F4846;
            }
            .active {
                background-color: #266150;
                padding: 5px;
                text-align: right;
                border-radius: 7px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{% trans "TestDriven.io Courses" %}</h1>

            {% get_current_language as CURRENT_LANGUAGE %}
            {% get_available_languages as AVAILABLE_LANGUAGES %}
            {% get_language_info_list for AVAILABLE_LANGUAGES as languages %}
            <div class="languages">
                <p>{% trans "Language" %}:</p>
                <ul class="languages">
                {% for language in languages %}
                    <li>
                    <a href="/{{ language.code }}/"
                    {% if language.code == CURRENT_LANGUAGE %} class="active"{% endif %}>
                        {{ language.name_local }}
                    </a>
                    </li>
                {% endfor %}
                </ul>

            {% for course in courses %}
            <div class="card p-4">
                <h3>
                    {{ course.title }}
                    <em style="font-size: small">{{ course.date }}</em>
                </h3>
                <p>{{ course.description }}</p>
                <strong>
                    Price: $ {{ course.price }}
                </strong>
            </div>

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

We:

1. loaded the internationalization tags using `{% load i18n %}`
1. retrieved the current language using `{% get_current_language %}` tag
1. also obtained the available languages defined in the `LANGUAGES` setting via the `{% get_available_languages %}` template tag
1. then used the tag `{% get_language_info_list %}` to enable you with the language attributes.
1. finally, built an HTML list to display all available languages and added an active class attribute to the currently active language to highlight the active language.

Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to see the changes. Switch between the multiple languages and also note how the URL prefix changes for each language.

## Add Locale-Support

Remember how we set `USE_L10N` to `True`? With this, Django will try to use a locale-specific format whenever it outputs a value in a template. Therefore, dates, times, and numbers will be in different formats based on the user's locale.

Navigate back to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to see the changes and you will notice that the date format changes. Decimal numbers in the English version of your site, are displayed with a dot separator for decimal places, while in the Spanish and French versions, they are displayed using a comma. This is due to the differences in locale formats between each of the languages.

![Home Page 2](https://github.com/Samuel-2626/django-lang/blob/main/images/homepage2.png)

## Conclusion

In this tutorial, you learned about internationalization and localization. How to make strings for translation. We also used third-party packages like Rosetta to make updating and compiling message files easy and django-parler to translate our models.

Grab the complete code from the [repo](https://github.com/Samuel-2626/django-lang).
