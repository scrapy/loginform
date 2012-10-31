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

    if typecount.get('text') > 1:
        score += 10
    if not typecount.get('text'):
        score -= 10
    if typecount.get('password') == 1:
        score += 10
    if not typecount.get('password'):
        score -= 10
    if typecount.get('checkbox') > 1:
        score -= 10
    if typecount.get('radio'):
        score -= 10
    return score

def _pick_form(forms):
    """Return the form most likely to be a login form"""
    return sorted(forms, key=_form_score, reverse=True)[0]

def _pick_fields(form):
    """Return the most likely field names for username and password"""
    userfield, passfield = None, None
    for x in form.inputs:
        type = x.type if isinstance(x, html.InputElement) else "other"
        if type == 'password':
            if passfield is not None:
                raise ValueError("Unrecognized login form: %s" % dict(form.inputs))
            passfield = x.name
        elif type == 'text':
            if userfield is not None:
                raise ValueError("Unrecognized login form: %s" % dict(form.inputs))
            userfield = x.name
    return userfield, passfield

def fill_login_form(url, body, username, password):
    doc = html.document_fromstring(body, base_url=url)
    form = _pick_form(doc.forms)
    userfield, passfield = _pick_fields(form)
    form.fields[userfield] = username
    form.fields[passfield] = password
    return form.form_values(), form.action or form.base_url, form.method
