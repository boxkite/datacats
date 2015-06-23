# datacats

[![Circle CI](https://circleci.com/gh/datacats/datacats.svg?style=svg)](https://circleci.com/gh/datacats/datacats)
[![docs](https://readthedocs.org/projects/docs/badge/?version=latest)](http://docs.datacats.com/)


[CKAN](http://ckan.org), a powerful CMS for publishing datasets, can be quite difficult to develop and deploy, especially for beginners. The aim of datacats is to make this easier and bring CKAN within reach for a much wider audience.

datacats relies on [Docker](https://www.docker.com/) to “containerize” all the components. That gives you a CKAN  environment that is fully self-contained, runs on any platform and can be deployed anywhere (that supports Docker containers) in one command.

There are a few basic terms used throughout datacats:
* **source directory** - an isolated instance of CKAN application code with installed extensions (such as ckan-galleries or [ckanext-spatial](https://ckanext-spatial.readthedocs.org/en/latest/)).
* **"environment"** - all the code and configuration that makes up a working CKAN catalog website. Includes a **source directory**, an isolated python virtualenv (a copy of python interpreter with the necessary python libraries installed), database and search engine (solr) configs. The environment is isolated in a docker container and can be deployed in its intact original shape.
* **CKAN site** - once you deploy and start using an environment, all the user data you load (datasets, user profiles and so on) make up a CKAN site. One can spin off as many CKAN sites as needed from the same environment.

## Install
Please see detailed OS-specific [installation instructions in the docs](http://docs.datacats.com/guide.html#installation).



## Create a CKAN environment

```
datacats create mytown
```

This will create a new environment called "mytown" in the current
directory, new data files in "~/.datacats/mytown" and start
serving your new site locally.

```
Creating environment "mytown"............
Installing ckan requirements
Installing ckan
Installing ckanext-mytowntheme
Initializing database
Starting web server at http://localhost:5306/ ...
admin user password:
```

Open your brower to the address shown to try out your new site.
Enter an admin password at the prompt to create your first sysadmin user.


## Customize your theme

In your environment directory you will find
"ckan" and "ckanext-mytowntheme" subdirectories.
"ckanext-mytowntheme" is a simple example extension that extends
some templates and adds some static files.

Customize your Jinja2 templates in
"ckanext-mytowntheme/ckanext/mytowntheme/templates", using
the files in "ckan/ckan/templates" as a reference.

Full CKAN extension possibilities are covered in the official CKAN
documentation.

The site is run with "paster serve --reload" by default so
changes to templates and source files will be visible almost immediately
after saving them. Refresh your browser window to see the changes.

For changes to configuration files and
new template files added use "reload" to force a site reload.

```
datacats reload mytown
```

You may omit "mytown" when running datacats commands from within the
environment directory or any subdirectory.

## Add CKAN extensions

Many of the [100+ existing CKAN extensions](http://extensions.ckan.org/)
are already compatible with datacats.

First download or clone an extension in to your environment directory.

```
cd myproject
git clone git@github.com:ckan/ckanext-pages.git
```

Then add the plugins and configuration options as required by the extension
to the "development.ini" file.  For ckanext-pages we add "pages" to the list
of plugins.

```
ckan.plugins = mytowntheme datastore image_view pages
```

Reinstall all extensions and reload the site with:
```
datacats install
```

Refresh your browser window to use the new features.


## Deploy your environment

Deploy your customized CKAN site to the DataCats.com cloud service.
```
datacats deploy --create
```

Follow the prompts and your site will be live in minutes.
