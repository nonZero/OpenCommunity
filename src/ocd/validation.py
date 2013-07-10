from django.template.defaultfilters import linebreaksbr
import HTMLParser
import bleach
from bleach import ALLOWED_ATTRIBUTES

EXTRA_TAGS = [
              'p',
              'br',
              'span',
              ]

TAGS = bleach.ALLOWED_TAGS + EXTRA_TAGS

BLOCK_TAGS = [
    'p',
    'br',
    'blockquote',
    'li',
    'ol',
    'ul',
]

ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
    'span': ['style'],
}

STYLES = ['text-decoration']


def clean_html(s):
    return bleach.clean(s, TAGS, ATTRIBUTES, STYLES)


def enhance_html(s):
    return bleach.linkify(clean_html(s))


def convert_to_html(s):
    return enhance_html(linebreaksbr(s, True))


def convert_html_to_text(s):
    """ converts html to text. """
    # keep just the block tags
    s = bleach.clean(s, BLOCK_TAGS, [], [], True, True)
    # remove newlines
    s = s.replace('\n', '')
    # replace block ends with newlines
    s = s.replace('/>', '/>\n')
    s = s.replace('<br>', '<br>\n')

    # strip tags
    s = bleach.clean(s, [], [], [], True, True).strip()

    # reconstruct entities
    h = HTMLParser.HTMLParser()
    return h.unescape(s)
