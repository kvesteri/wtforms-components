import functools

try:
    from html import escape as html_escape
except ImportError:
    from cgi import escape as _cgi_escape
    html_escape = functools.partial(_cgi_escape, quote=True)
