#!/bin/bash
#
# chkconfig: 35 99 00
# description: destar.

# Source the function library.
. /etc/init.d/functions

PIDFILE="/var/run/destar.pid"
RETVAL=0

# See how we were called.
case "$1" in
  start)
	/usr/sbin/destar > /dev/null 2>&1 &
	echo $! > $PIDFILE
	RETVAL=0
	;;
  stop)
	PID=`cat $PIDFILE`
	kill $PID
	;;
  *)
	echo $"Usage: $0 {start|stop}"
	RETVAL=1
esac

exit $RETVAL
