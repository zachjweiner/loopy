import os

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = "1.0"

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named "sphinx.ext.*") or your custom ones.
extensions = [
        "sphinx.ext.autodoc",
        "sphinx.ext.intersphinx",
        "sphinx.ext.linkcode",
        "sphinx.ext.doctest",
        "sphinx_copybutton",
        ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
#source_encoding = "utf-8-sig"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "loopy"
copyright = "2016, Andreas Klöckner"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
ver_dic = {}
_version_source = "../loopy/version.py"
with open(_version_source) as vpy_file:
    version_py = vpy_file.read()

os.environ["AKPYTHON_EXEC_IMPORT_UNAVAILABLE"] = "1"
exec(compile(version_py, _version_source, "exec"), ver_dic)
version = ".".join(str(x) for x in ver_dic["VERSION"])
# The full version, including alpha/beta/rc tags.
release = ver_dic["VERSION_TEXT"]
del os.environ["AKPYTHON_EXEC_IMPORT_UNAVAILABLE"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

html_theme = "furo"

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ("index", "loopy", "loopy Documentation",
     ["Andreas Kloeckner"], 1)
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "https://docs.python.org/3": None,
    "https://numpy.org/doc/stable/": None,
    "https://documen.tician.de/pytools": None,
    "https://documen.tician.de/islpy": None,
    "https://documen.tician.de/pyopencl": None,
    "https://documen.tician.de/cgen": None,
    "https://documen.tician.de/pymbolic": None,
    "https://documen.tician.de/pytools": None,
    "https://pyrsistent.readthedocs.io/en/latest/": None,
    }

autoclass_content = "class"

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

import sys
import inspect
import pkg_resources

linkcode_revision = "main"
linkcode_url = f"https://github.com/inducer/{project}/blob/" \
               + linkcode_revision + "/{filepath}#L{linestart}-L{linestop}"


def linkcode_resolve(domain, info):
    if domain != 'py' or not info['module']:
        return None

    modname = info['module']
    topmodulename = modname.split('.')[0]
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    try:
        modpath = pkg_resources.require(topmodulename)[0].location
        filepath = os.path.relpath(inspect.getsourcefile(obj), modpath)
        if filepath is None:
            return
    except Exception:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except OSError:
        return None
    else:
        linestart, linestop = lineno, lineno + len(source) - 1

    return linkcode_url.format(
        filepath=filepath, linestart=linestart, linestop=linestop)
