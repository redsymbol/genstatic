genstatic - Generate and maintain large sets of static HTML files, without going insane

Genstatic is a tool for generating and managing sets of static HTML
files using the Django template system.  It's quite useful when you
need to create a set of HTML files that share structural similarities,
in a low-maintenance way.  It's EXTREMELY useful when, as a web
designer, you are serving a client who hands you a very messy folder
of static files for their existing website, and you need to modify or
work with them, without going crazy.

Genstatic is not limited to HTML files.  You can use it to generate
CSS, Javascript, plain text, or whatever you need.

Genstatic is based on Django templates, and lets you leverage some of
its powerful features: template inheritance, template variables, and a
rich built-in template library (of "tags" and "filters").  Learn more
at http://docs.djangoproject.com/en/1.2/topics/templates/ .

OVERVIEW

Usage:
  genstatic.py [options] srcdir destdir

For a full list of options, execute "genstatic.py -h".

srcdir and destdir are directories.  srcdir contains static files and
Django templates.  It normally also contains a magic subdirectory,
named "_" (underscore), that can contain inheritable base templates.
These are files you create.

Every file in srcdir, other than those in "_", is rendered as a Django
template, and written into destdir (which is created, and by default,
not overwritten.  Override that with the --clobber option.)

Often, you will like to set variable names and values that are
available to the templates.  Create a python file that defines these
variables - for example, "myparams.py" .  The pass this file name with
the -d option to genstatic.

(You will have to use Python syntax, which most IT workers
find very straightforward.  See Appendix A for a primer.)

HOW ABOUT AN EXAMPLE

Suppose srcdir contains the files index.html, about.html, and
_/base.html, with the following contents:

_/base.html:
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <link rel="stylesheet" href="/widget.css">
    <script src="/widgets.js" type="text/javascript"></script>
    <title>{% block title %}{% endblock %}</title>
  </head>
  <body>
    <div id="content">
      {% block content %}
      <!-- page content goes here -->
      {% endblock %}
    </div>
    <div id="footer">Copyright {{copydate}} Joe's Widget Shop</div>
  </body>
</html>
# end of _/base.html

index.html:
{% extends "_/base.html" %}
{% block title %}Welcome to Joe's Widget Shop{% endblock %}
{% block content %}
<h1>Joe's Widget Shop</h1>
<p>Welcome to Joe's Widget Shop, serving the greater Gotham, Idaho area!</p>
{% endblock %}
# end of index.html

about.html:
{% extends "_/base.html" %}
{% block title %}About Joe's Widget Shop{% endblock %}
{% block content %}
<h1>About Joe's Widget Shop</h1>
<p>One warm summer night in '76, Joe had a vision: A clean and well-lit shop,
with widgets as far as the eye could see. It wasn't long before...</p>
{% endblock %}
# end of about.html

You also create a file named vars.py that just contains this line:
copydate=2010

Simply invoke on the command line:
  genstatic.py -d copydate.py srcdir destdir

destdir is created, containing index.html and about.html, and that's
it - base.html is omitted.  Here's what those files will contain:

index.html:
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <link rel="stylesheet" href="/widget.css">
    <script src="/widgets.js" type="text/javascript"></script>
    <title>Welcome to Joe's Widget Shop</title>
  </head>
  <body>
    <div id="content">
<h1>Joe's Widget Shop</h1>
<p>Welcome to Joe's Widget Shop, serving the greater Gotham, Idaho area!</p>
    </div>
    <div id="footer">Copyright 2010 Joe's Widget Shop</div>
  </body>
</html>
# end of index.html

about.html:
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <link rel="stylesheet" href="/widget.css">
    <script src="/widgets.js" type="text/javascript"></script>
    <title>About Joe's Widget Shop</title>
  </head>
  <body>
    <div id="content">
<h1>About Joe's Widget Shop</h1>
<p>One warm summer night in '76, Joe had a vision: A clean and well-lit shop,
with widgets as far as the eye could see. It wasn't long before...</p>
    </div>
    <div id="footer">Copyright 2010 Joe's Widget Shop</div>
  </body>
</html>
# end of about.html

LICENSE

Genstatic is licensed under the GPL version 3.

This source code is copyright 2009-2010 Aaron Maxwell.  All rights reserved.

INSTALL

Genstatic depends on Python 2.6 or later, and Django 1.2.  Install
both of these on your system, and make sure Django is in the python
path. (i.e. is one of the directories in the PYTHONPATH environment
variable).

THANKS

Thanks to Mobile Web Up (http://mobilewebup.com) for sponsoring
genstatic development.  If you or someone you know needs to upgrade a
website for mobile phones, or start a mobile marketing campaign,
contact Mobile Web Up today.

APPENDIX A: PYTHON VARIABLES

To make varibles available to genstatic (with the -d option), you'll
have to create a small Python file that defines some variables and
their values.  It's not too hard.

The official Python tutorial has a section, "Using Python as a
calculator", that is very nice, and can teach you all you'll need to
know.  Read it here:
http://docs.python.org/tutorial/introduction.html#using-python-as-a-calculator

Short version: you can just create a file named "something.py", and
put in some lines like this:

name = value

... where 'name' is a variable name, and 'value' is what the variable
is set to.  'value' can be a whole number (integer), a floating-point
number, or a string (surrounded by either single or double quotes).
Single and double quotes are equivalent in python, and they both
interpolate.  So you'll need to backslash-escape any special
characters.
