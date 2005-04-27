#!/bin/sh

#
# a wrapper script to run destar with proper environment
#

PYDIR=/usr/share/destar/python

if [ "$PYTHONPATH" = '' ]; then
	PYTHONPATH=$PYDIR
else
	PYTHONPATH="$PYTHONPATH:$PYDIR"
fi

CONFIGLETS_DIR=${CONFIGLETS_DIR:-${PYDIR}}
STATICPAGES_DIR=${STATICPAGES_DIR:-/usr/share/destar/static}

export PYTHONPATH CONFIGLETS_DIR STATICPAGES_DIR

exec $PYDIR/destar.py "$@"
