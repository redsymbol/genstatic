genstatic - Generate and maintain large sets of static HTML files, without going insane

Genstatic is a tool for generating sets of static HTML files using the
Django template system.  It's quite useful when you need to create a
set of HTML files that share structural similarities, in a
low-maintenance way.  It's EXTREMELY useful when, as a web designer,
you are serving a client who hands you a very messy folder of static
files for their existing website, and you need to modify them all
without going crazy.

Genstatic is not limited to HTML files.  You can use it to generate
CSS, Javascript, README.txt, or whatever you want.

OVERVIEW

Usage:
  genstatic [options] srcdir destdir

srcdir and destdir are directories.  srcdir contains static files and
Django templates.  It probably also contains a magic subdirectory,
named "_" (underscore), that can contain inheritable base templates.

Every file in srcdir, other than those in "_", is rendered as a Django
template, and written into destdir (which is created, and by default,
not overwritten.  Override that with the --clobber option.)

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
<p>One warm summer night, Joe had a vision: A clean and well-lit shop,
with widgets as far as the eye could see. It wasn't long before...</p>
{% endblock %}
# end of about.html

Simply invoke on the command line:
  genstatic srcdir destdir

destdir is created, containing index.html and about.html, the way you need 'em.

