#! /bin/sh
# Starts and stops the Destar, Asterisk Web GUI


PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/sbin/destar
NAME=destar
DESC="Asterisk Web GUI DeStar"
PIDFILE=/var/run/$NAME/$NAME.pid
DAEMON_OPTS="--daemonize --pid=$PIDFILE"

test -x $DAEMON || exit 0

# Include destar defaults if available
if [ -f /etc/default/destar ] ; then
	. /etc/default/destar
fi

set -e

case "$1" in
  start)
	echo -n "Starting $DESC: "
	start-stop-daemon --start --quiet --pidfile $PIDFILE \
		--chuid asterisk --exec $DAEMON -- $DAEMON_OPTS >/dev/null 
	echo "$NAME."
	;;
  stop)
	echo -n "Stopping $DESC: "
	start-stop-daemon --stop --oknodo --quiet --pidfile $PIDFILE >/dev/null
	echo "$NAME."
	;;
  restart|force-reload)
	echo -n "Restarting $DESC: "
	start-stop-daemon --stop --oknodo --quiet --pidfile $PIDFILE >/dev/null
	sleep 1
	start-stop-daemon --start --quiet --pidfile $PIDFILE \
          	--chuid asterisk --exec $DAEMON -- $DAEMON_OPTS >/dev/null 
	echo "$NAME."
	;;
  *)
	N=/etc/init.d/$NAME
	echo "Usage: $N {start|stop|restart|force-reload}" >&2
	exit 1
	;;
esac

exit 0
