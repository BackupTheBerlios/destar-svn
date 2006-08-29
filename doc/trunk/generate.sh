#!/bin/sh

#
# a wrapper script to run trunk/docs.py with proper enviroment
#

PYDIR=../../trunk

if [ "$PYTHONPATH" = '' ]; then
	PYTHONPATH=$PYDIR
else
	PYTHONPATH="$PYTHONPATH:$PYDIR"
fi

CONFIGLETS_DIR=${CONFIGLETS_DIR:-${PYDIR}}
DESTAR_DOC_DIR=./autogenerated

export PYTHONPATH CONFIGLETS_DIR DESTAR_DOC_DIR

exec $PYDIR/docs.py "$@"
