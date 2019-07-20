# sharedlists

[![Build Status](https://travis-ci.org/pylover/sharedlists.svg?branch=master)](https://travis-ci.org/pylover/sharedlists)
[![Coverage Status](https://coveralls.io/repos/github/pylover/sharedlists/badge.svg?branch=master)](https://coveralls.io/github/pylover/sharedlists?branch=master)

A set of REST APIs to create shared lists which can manipulated by anyone.


```bash
pip install -r requirements-dev.txt
pip install -e .
sharedlists db create -m
```


```bash
. client.sh
l.login oscar 12345
l.append oscar/foo/bar
l.append oscar/foo/baz
l.list oscar/foo
l.list
```
