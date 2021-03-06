import sys, os

'''This module is used to fork the current process into a daemon. Almost
none of this is necessary (or advisable) if your daemon is being started by
inetd. In that case, stdin, stdout and stderr are all set up for you to
refer to the network connection, and the fork()s and session manipulation
should not be done (to avoid confusing inetd).  Only the chdir() and umask()
steps remain as useful.

References:

	UNIX Programming FAQ
		1.7 How do I get my program to act like a daemon?
		http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
	
	Advanced Programming in the Unix Environment
		W. Richard Stevens, 1992, Addison-Wesley, ISBN 0-201-56317-7.
'''
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', pidfile='/var/run/destar.pid'):
	'''This forks the current process into a daemon.  The stdin, stdout,
	and stderr arguments are file names that will be opened and be used
	to replace the standard file descriptors in sys.stdin, sys.stdout,
	and sys.stderr.  These arguments are optional and default to
	/dev/null.  Note that stderr is opened unbuffered, so if it shares a
	file with stdout then interleaved output may not appear in the order
	that you expect.'''

	# Finish up with the current stdout/stderr
	sys.stdout.flush()
	sys.stderr.flush()

	# Do first fork.
	try: 
		pid = os.fork() 
		if pid > 0:
			sys.stdout.close()
			sys.exit(0) # Exit first parent.
	except OSError, e: 
		sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror)	)
		sys.exit(1)
		
	# Decouple from parent environment.
	os.chdir("/") 
	os.umask(0022) 
	os.setsid() 
	
	# Do second fork.
	try: 
		pid = os.fork() 
		if pid > 0:
			sys.stdout.close()
			sys.exit(0) # Exit second parent.
	except OSError, e: 
		sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror)	)
		sys.exit(1)
		
	# Now I am a daemon!
	
	# Redirect standard file descriptors.
	si = file(stdin, 'r')
	so = file(stdout, 'a+')
	se = file(stderr, 'a+', 0)
	os.dup2(si.fileno(), sys.stdin.fileno())
	os.dup2(so.fileno(), sys.stdout.fileno())
	os.dup2(se.fileno(), sys.stderr.fileno())

	# Try write pid
	try:
		pid_fd=open(pidfile,"w")
		pid_fd.write("%d"%os.getpid())
		pid_fd.close()
	except IOError:
		pass

	# TODO: handle setuid


if __name__ == "__main__":
	 '''This is an example main function run by the daemon.
	 This prints a count and timestamp once per second.
	 '''

	 daemonize('/dev/null','/tmp/daemon.log','/tmp/daemon.log')
	 import time
	 sys.stdout.write ('Daemon started with pid %d\n' % os.getpid() )
	 sys.stdout.write ('Daemon stdout output\n')
	 sys.stderr.write ('Daemon stderr output\n')
	 c = 0
	 while 1:
		 sys.stdout.write ('%d: %s\n' % (c, time.ctime(time.time())) )
		 sys.stdout.flush()
		 c = c + 1
		 time.sleep(1)
