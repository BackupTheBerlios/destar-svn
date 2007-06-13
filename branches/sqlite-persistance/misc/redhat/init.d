#!/bin/bash
#
# chkconfig: 35 99 00
# description: destar.

# Source the function library.
. /etc/init.d/functions

PIDFILE="/var/run/destar.pid"
RETVAL=0

start() {
        # Start daemons.
        echo -n $"Starting destar: "
        /usr/sbin/destar > /dev/null 2>&1 &
        RETVAL=$?
        echo $! > $PIDFILE
        echo
        [ $RETVAL = 0 ] && touch /var/lock/subsys/destar
}

stop() {
        # Stop daemons.
        echo -n $"Shutting down destar: "
	PID=`cat $PIDFILE`
	kill $PID
        RETVAL=$?
        echo
        [ $RETVAL = 0 ] && rm -f /var/lock/subsys/destar
}

restart() {
        stop
        start
}

# See how we were called.
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart)
        restart
        ;;
  condrestart)
        [ -f /var/lock/subsys/destar ] && restart || :
        ;;
  status)
        ;;
  *)
        echo $"Usage: exim {start|stop|restart|status|condrestart}"
        exit 1
esac

exit $RETVAL
