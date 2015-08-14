#!/usr/bin/env python
import json
import glob
import requests
import optparse
from loginform import fill_login_form


def parse_opts():
    op = optparse.OptionParser(usage="%prog [-w NAME] url | -l")
    op.add_option("-w", dest="write", metavar="NAME", help="write new sample")
    op.add_option("-l", dest="list", action="store_true", help="list all samples")
    opts, args = op.parse_args()
    if not opts.list and len(args) != 1:
        op.error("incorrect number of args")
    return opts, args


def list_samples():
    return [fn.split('/')[1][:-5] for fn in glob.glob('samples/*.json')]


def sample_html(name):
    return 'samples/%s.html' % name


def sample_json(name):
    return 'samples/%s.json' % name


def check_sample(name):
    with open(sample_json(name), 'rb') as f:
        url, expected_values = json.loads(f.read().decode('utf8'))
    with open(sample_html(name), 'rb') as f:
        body = f.read().decode('utf-8')
    values = fill_login_form(url, body, "USER", "PASS")
    values = json.loads(json.dumps(values))  # normalize tuple -> list
    assert values == expected_values


def test_samples():
    for name in list_samples():
        yield check_sample, name


def main():
    opts, args = parse_opts()
    if opts.list:
        print("\n".join(list_samples()))
    else:
        url = args[0]
        r = requests.get(url)
        values = fill_login_form(url, r.text, "USER", "PASS")
        values = (url, values)
        print(json.dumps(values, indent=3))
        if opts.write:
            with open(sample_html(opts.write), 'wb') as f:
                f.write(r.text.encode('utf-8'))
            with open(sample_json(opts.write), 'wb') as f:
                json.dump(values, f, indent=3)


if __name__ == "__main__":
    main()
