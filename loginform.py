#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from collections import defaultdict
from lxml import html


__version__ = '0.9' # also update setup.py


def _form_score(form):
    score = 0
    if len(form.inputs.keys()) in (2, 3): # user/pass or user/pass/remember-me
        score += 10

    typecount = defaultdict(int)
    for x in form.inputs:
        type = x.type if isinstance(x, html.InputElement) else "other"
        typecount[type] += 1

    if typecount['text'] > 1:
        score += 10
    if not typecount['text']:
        score -= 10

    if typecount['password'] == 1:
        score += 10
    if not typecount['password']:
        score -= 10

    if typecount['checkbox'] > 1:
        score -= 10
    if typecount['radio']:
        score -= 10

    return score


def _pick_form(forms):
    """Return the form most likely to be a login form"""
    return sorted(forms, key=_form_score, reverse=True)[0]


def _pick_fields(form):
    """Return the most likely field names for username and password"""
    userfield = passfield = emailfield = None
    for x in form.inputs:
        if not isinstance(x, html.InputElement):
            continue

        type = x.type
        if type == 'password':
            if passfield is not None:
                raise ValueError("Unrecognized login form: %s" % dict(form.inputs))
            passfield = x.name
        elif type == 'text':
            if userfield is not None:
                raise ValueError("Unrecognized login form: %s" % dict(form.inputs))
            userfield = x.name
        elif type == 'email':
            if emailfield is not None:
                raise ValueError("Unrecognized login form: %s" % dict(form.inputs))
            emailfield = x.name

    return userfield or emailfield, passfield

def submit_value(form):
  """Returns the value for the submit input, if any"""
  values = []
  for x in form.inputs:
    if x.type == "submit" and x.name:
      values.append((x.name, x.value))
  return values


def fill_login_form(url, body, username, password):
    doc = html.document_fromstring(body, base_url=url)
    form = _pick_form(doc.xpath('//form'))
    userfield, passfield = _pick_fields(form)
    form.fields[userfield] = username
    form.fields[passfield] = password
    form_values = form.form_values() + submit_value(form)
    return form_values, form.action or form.base_url, form.method


def main():
    ap = ArgumentParser()
    ap.add_argument('-u', '--username', default='username')
    ap.add_argument('-p', '--password', default='secret')
    ap.add_argument('url')
    args = ap.parse_args()

    try:
        import requests
    except ImportError:
        print('requests library is required to use loginform as a tool')

    r = requests.get(args.url)
    values, action, method = fill_login_form(args.url, r.text, args.username, args.password)
    print('url: {0}\nmethod: {1}\npayload:'.format(action, method))
    for k, v in values:
        print('- {0}: {1}'.format(k, v))


if __name__ == '__main__':
    sys.exit(main())
