# -*- coding: utf-8 -*-

html_theme_options = {
    'logo': 'logo.jpg',
    'github_user': 'jdost',
    'github_repo': 'wingcommander',
    'travis_button': True,
}

import sys
import os
import alabaster

sys.path.insert(0, os.path.abspath('../src'))
from wingcommander import __version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'alabaster',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

# General information about the project.
project = u'Wing Commander'
copyright = u'2015, jdost'

version = __version__
release = __version__

exclude_patterns = ['build']
html_theme = 'alabaster'
html_theme_path = [alabaster.get_path()]
pygments_style = 'sphinx'
highlight_language = "python"

# html_title = None
# html_short_title = None
# html_logo = None
# html_favicon = None

html_static_path = ['static']
html_sidebars = {
    "**": ["about.html", "navigation.html", "searchbox.html"]
}
# html_additional_pages = {}
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True
htmlhelp_basename = 'WingCommanderdoc'


latex_documents = [
    ('index', 'WingCommander.tex', u'Wing Commander Documentation',
     u'jdost', 'manual'),
]

man_pages = [
    ('index', 'wingcommander', u'Wing Commander Documentation',
     [u'jdost'], 1)
]

texinfo_documents = [
    ('index', 'WingCommander', u'Wing Commander Documentation',
     u'jdost', 'WingCommander', 'One line description of project.',
     'Miscellaneous'),
]
