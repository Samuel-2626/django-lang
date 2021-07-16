# Add multiple language support to your Django project

Django offers multiple language support. In fact, Django is translated into more than fifty languages. In this tutorial, you will learn how to add multiple language support to your django project.

## Objectives

By the end of this tutorial you should be able to:

1. understand the difference between internationalization and localization.
1. add language prefix to URL patterns.
1. translating templates
1. allow users to switch languages.
1. translating models.
1. format localization.

## Project Setup and Overview

This is what you will be aiming to achieve from this tutorial.

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

Run the following management command to add some data to your databasee:

```bash
$ python manage.py add_courses
```

In the next section, we will be discussing briefly about **Internationalization** and **Localization**.

## Internationalization vs localization

`Internationalization` and `localization` are rather two different terms. While **internationalization** (i18n) enables our web application to be language agnostic (i.e it isn't hard wired to a particular language), but can be used by different languages and locales, **localization** (l10n) on the other hand is the process of translating our web application to a particular language and locale.

Recall that `Django` using its international framework has being translated into more than 50 languages.

Through the international framework, we can easily mark strings for translation, both in Python code and in our templates. It makes use of GNU gettext toolkit to generate and manage a plain text file that represents a language known as the **message file**. The message file ends with `.po` as its extension. Another file is generated for each language once translation is done which ends with the `.mo` extension. This is known as the compiled translation.

To use this gettext toolkit, it needs to be installed. On macOS a simple way is to install it using [Homebrew](https://brew.sh/), by running the following commands.

```bash
brew install gettext
brew link --force gettext
```

For most Linux distributions, it comes pre-installed. And finally for Windows, the steps to install can be found [here](https://djangoproject.com/en/3.0/topics/i18n/translation/#gettext-on-windows).

In the next section, we will be preparing our project for internationalization and localization.

## Preparing your project for internationalization

Django comes with some default settings when we created a new project. This can be found inside the `settings.py` file of our project under the **internationalization** section.

The first setting is the `LANGUAGE_CODE`. By default, Django set it's to the United States English (en-us). This is a locale specific name. Let's update it to a generic name, English (en).

```py
LANGUAGE_CODE = 'en' # new
```

You also have `USE_I18N`, `USE_L10N`, `USE_TZ` all set default to **True** i.e. Django's translation system is enabled, Localized format is enabled and Django is timezone aware respecitvely.

You will be adding a few additional settings to complement the existing ones:

```py
from django.utils.translation import gettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
)
```

What's happening here?

1. We are specifying the languages we want our project to be available in. If this is not specified Django will assume our project to be available in all of it's supported languages.

1. This LANGUAGE setting contains two tuples that consist of a language code and a name. Recall that the language codes can be locale-specific, such as **en-gb** or generic such as **en**.

1. Also, take note of the imports we will be using the **gettext_lazy** function to mark strings for translation. When using the lazy function, strings are translated when the value is accessed, rather than when the function is called. They are useful when strings marked for translation are in paths that are executed when modules are loaded.

Add `django.middleware.locale.LocaleMiddleware` to the MIDDLEWARE setting. Make sure that this middleware comes after SessionMiddleware because LocaleMiddleware needs to use session data. It also has to be placed before CommonMiddleware because the latter needs an active language to resolve the requested URL. The MIDDLEWARE setting should now look as follows:

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

Create a locale path direcotry. The locale directory is the place where message files for your application will reside. Edit the settings.py file again and add the following settings to it:

```py
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)
```

The LOCALE_PATHS setting specifies the directories where Django has to look for translation files. Locale paths that appear first have the highest precedence.

When you use the makemessages command from your project directory, messaage files will be generated in the locale/ path you created. However, for applications that contain a locale/ directory, message files will be generated in that directory.

Next, create a new directory inside of your root project called **locale** inside a new folder for each language (en, es and fr).

Open the shell and run the following command from your project directory:

```bash
django-admin makemessages --all
```

A .po message file has been created for each language.

What to know?

1. msgid: The translation string as it appears in the source code.
1. msgstr: The language translation, which is empty by default. This is where you have to enter the actual translation for the given string.

```bash
django-admin compilemessages
```

You can see that a .mo compiled message file has been generated for each language.

## Translating fields name

We can translate model fields name and forms my marking them for translation using either **gettext** or **gettext_lazy** function.

Edit the `models.py` file:

```py
from django.db import models

from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    title = models.CharField(_('title'), max_length=90)
    description = models.TextField(_('descriptio'))
    date = models.DateField(_('date'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
```

```bash
django-admin makemessages --all
django-admin compilemessages
```

You have still not translated anything we just marked them for translation, we can also do this for forms by adding a label. In the next section, we will start translating using a third-party package for simplicity.

## Using the Rosetta translation interface

We will be using a third-party library called **Rosseta**. Rosetta is a third-party application that allows you to edit translations using the same interface as the Django administration site. Rosetta makes it easy to edit .po files and it updates compiled translation files.

Rosseta as already been installed as part of the dependencies, therefore, all you need to do is to add it as part of your installed apps

```py
INSTALLED_APPS = [

    'rosetta', # new
]
```

You will also need to add Rosetta's URL to your main URL configuration. Edit the main `urls.py` file of your project and add the following URL pattern to it. Make sure it comes after the admin.

```py
path('rosetta/', include('rosetta.urls')), # new
```

Navigate the to [http://127.0.0.1:8080/rosetta/](http://127.0.0.1:8080/rosetta/) in your browser.

![Rosetta Homepage](https://github.com/Samuel-2626/django-lang/blob/main/images/rosetta-homepage.png)

![Rosetta French](https://github.com/Samuel-2626/django-lang/blob/main/images/rosetta-french.png)

When you finish editing translations, click the **Save and translate next block** button to save the translations to the .po file.

Rosetta compiles the message file when you save translations, so there is no need for you to run the compilemessages command.

Note that when you add new translations to your production environment, if you server Django with a real web server, you will have to reload your server after running the compilemessages command, or after saving the translations with Rosetta, for changes to take effect.

## Add language prefix to URL patterns

Django offers internationalization capabilities for URLs. It allow us to serve each language version under a different base URL. A reason for tanslating URLs is to optimize your site for seacrch engines. By adding a language prefix to your patterns, you will be able to index a URL for each language instead of a single URL for all of them. Furthermore, by translating URLs intoeach language, you will provide search engines with URLs that will rank better for each language.

Django allows you to add a language prefix to your URL patterns. For examp,e, the English version of your site can be served under a path starting /en/, and the Spanish version under /es/. To use languages in URL patterns, you have to use **LocalMiddleware** provided by Django. The framework will use it to identify the current language from the requested URL. You added it previously to the MIDDLEWARE setting of your project, so you don't need to do it now.

Edit the main `urls.py` file of the `django-lang` project and add `i18n_patterns()`, as follows:

```py
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('', include('course.urls')),
)
```

Run the development server and open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. you will be redirectd to the requested URL, including the language prefix. Take a look at the URL in your browser; it should now look like [http://127.0.0.1:8000/en/](http://127.0.0.1:8000/en/)

## Translating our models

Django doesn't not support translating our models out of box, therefore we will be using a third-party library called `django-parler`. This package is one of the most popular plugins that allows us to translate our models.

How does it work?
`django-parler` generates a separate database table for each model that contains translations. This table includes all the translated fields and a foreign key for the original object that the translation belongs to. It also contains a language field, since each row stores the content for a single language.

Edit the settings.py file of your project and add `parler` to the INSTALLED_APPS setting, as follows:

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

The setting defines the available languages, en and es, for `django-parler`. You specify the default language `en` and indicate that `django-parler` should not hide untranslated content.

**django_parler** provides a TranslatableModel model class and a TranslatedFields wrapper to translate model fields.

**django_parler** manages translations by generating another model for each translatable model.

Since, Django uses a separate table for translations, then are some features that you can't use.

**django_parler** integrates smoothly with the Django administration site. It includes a TranslatableAdmin class that overrides the ModelAdmin class provided by Django to manage translations.

It's important to note that this migration deletes the previous existing fields from your models.

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

Next, apply makemigraions :

```bash
$ python manage.py makemigrations
```

However, Edit the file migrations/002_translations.py of the course application and replace the two occurences of the following line:

```py
bases = (parler.models.TranslatableFieldsModelMixin, models.Model)
```

with the following one:

```py
bases = (parler.models.TranslatableModel, models.Model)
```

This is a fix for a minor issue found in the django-parler version you are using. This change is necessary to prevent the migration from failing when applying it.

Next, apply migrations :

```bash
$ python manage.py migrate
```

```py
from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Course

admin.site.register(Course, TranslatableAdmin)
```

Run the following management command to add some data to your databasee:

```bash
$ python manage.py add_courses
```

Navigate the to [http://127.0.0.1:8080/admin/](http://127.0.0.1:8080/admin/) in your browser.

![Admin 1](https://github.com/Samuel-2626/django-lang/blob/main/images/admin-1.png)

![Admin 2](https://github.com/Samuel-2626/django-lang/blob/main/images/admin-2.png)

## Translating Templates

Django offers the {% trans %} and {% blocktrans %} template tags to translate strings in templates. In order to use the translation template tags, you have to add {% load i18n %} at the top of your template to load them.

The {% trans %} template tag allows you to mark a literal for translation. Internally Django executes gettext() on the given text.

The {% trans %} tag is useful for a simple translation strings, but it can't handle content for tanslation that includes variables.

The {% blocktrans %} template tag allows you to mark content that includes literals and variable contenr using placeholders.

Use the {% blocktrans %} tag instead of {% trans %} when you need to include variable content in your translation string.

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
		<title>Company</title>
	</head>
	<body>
		<div class="container">
			<h1>{% trans "Top Tech Companies" %}</h1>

			{% get_current_language as LANGUAGE_CODE %}
			{% get_available_languages as LANGUAGES %}
			{% get_language_info_list for LANGUAGES as languages %}
			<div class="languages">
				<p>{% trans "Language" %}:</p>
				<ul class="languages">
				{% for language in languages %}
					<li>
					<a href="/{{ language.code }}/"
					{% if language.code == LANGUAGE_CODE %} class="selected"{% endif %}>
						{{ language.name_local }}
					</a>
					</li>
				{% endfor %}
				</ul>

			{% for company in companies %}
			<h3>
				{% blocktrans with code=company %}

						{{ code }} -
				{% endblocktrans %}

				<em style="font-size: small">{{ company.founded }}</em>
			</h3>
			<p>{{ company.description }}</p>
			<hr />
			{% empty %}
			<p>Database is empty</p>
			{% endfor %}
		</div>
	</body>
</html>
```

## Allowing users to switch languages

Since you are serving content that is available in multiple languages, you should let users switch the sites language.

You are going to add a language selector to your site. The language selector will consist of a list of available languages displayed using links.

....

Make sure that no template tag is split into multiple lines.

What's happening here?

1. load the internationaliation tags using {% load i18n %}
1. You use the {% get_current_language %} tag to retrieve the current language.
1. You get the languages defined in the LANGUAGES setting using the {% get_available_languages %} template tag.
1. You use the tag {% get_language_info_list %} to provide easy access to the language attributes.
1. You build an HTML list to display all available languages and you add a selected class atrribute to the current active language.

## Format Localization

Depending on the user's locale, you might want to display dates, times, and numbers in different formats. Localized formatting can be activated by changing the `USE_L10N` setting to True.

When `USE_L10N` is enabled, Django will try to use a locale-specific format whenever it outputs a value in a template.

You can see that decimal numbers in the English version of youe site are displayed witha dot separator for decimal places, while in the Spanish version, they are displayed using a comma. This is due to the locale formats specified for the es locale by Django.

## Conclusion

Grab the complete code from the [repo](https://github.com/Samuel-2626/django-lang).

## Addition:

Translating URL pattenrs

Django support tanslated strings in URL patterns. You can use a different translation for each language for a single URL pattern. You can mark URL patterns for translation in the same way as you would with literals, using the gettext_lazy() function.

Open the shell and run the next command to update the message files with the new translations:

django-admin makemessages --all
