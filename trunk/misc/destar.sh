#!/bin/sh

#
# a wrapper script to run destar with proper environment
#

PYDIR=/usr/lib/destar/python

if [ "$PYTHONPATH" = '' ]; then
	PYTHONPATH=$PYDIR
else
	PYTHONPATH="$PYTHONPATH:$PYDIR"
fi

CONFIGLETS_DIR=${CONFIGLETS_DIR:-/usr/lib/destar/python}
STATICPAGES_DIR=${STATICPAGES_DIR:-/usr/share/destar/pages}

export PYTHONPATH CONFIGLETS_DIR STATICPAGES

exec $PYDIR/destar.py "$@"
