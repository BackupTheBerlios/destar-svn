#!/usr/bin/env python

"""quixote.server.medusa_http

An HTTP handler for Medusa that publishes a Quixote application.
"""

# A simple HTTP server, using Medusa, that publishes a Quixote application.

import sys
import asyncore, rfc822, socket, urllib
from cStringIO import StringIO
try:
	from quixote.http_response import Stream
except:
	print "You need Quixote 2.x or greater"
	sys.exit(1)
from quixote.publish import Publisher
from medusa import http_server, xmlrpc_handler
from quixote.http_request import HTTPRequest
from quixote.errors import PublishError


class StreamProducer:
    def __init__(self, stream):
	self.iterator = iter(stream)

    def more(self):
	try:
	    return self.iterator.next()
	except StopIteration:
	    return ''


class QuixoteHandler:
    def __init__(self, publisher, server_name, server, https=False):
	"""QuixoteHandler(publisher:Publisher, server_name:string,
			server:medusa.http_server.http_server)

	Publish the specified Quixote publisher.  'server_name' will
	be passed as the SERVER_NAME environment variable.
	"""
	self.publisher = publisher
	self.server_name = server_name
	self.server = server
	self.https = https

    def match(self, request):
	# Always match, since this is the only handler there is.
	return 1

    def handle_request(self, request):
	msg = rfc822.Message(StringIO('\n'.join(request.header)))
	length = int(msg.get('Content-Length', '0'))
	if length:
	    request.collector = xmlrpc_handler.collector(self, request)
	else:
	    self.continue_request('', request)

    def continue_request(self, data, request):
	msg = rfc822.Message(StringIO('\n'.join(request.header)))
	remote_addr, remote_port = request.channel.addr
	if '#' in request.uri:
	    # MSIE is buggy and sometimes includes fragments in URLs
	    [request.uri, fragment] = request.uri.split('#', 1)
	if '?' in request.uri:
	    [path, query_string] = request.uri.split('?', 1)
	else:
	    path = request.uri
	    query_string = ''

	path = urllib.unquote(path)
	server_port = str(self.server.port),
	http_host = msg.get("Host")
	if http_host:
		if ":" in http_host:
			server_name, server_port = http_host.split(":", 1)
		else:
			server_name = http_host
	else:
		server_name = (self.server.ip or
					socket.gethostbyaddr(socket.gethostname())[0])

	environ = {'REQUEST_METHOD': request.command,
		   'ACCEPT_ENCODING': msg.get('Accept-encoding'),
		   'CONTENT_TYPE': msg.get('Content-type'),
		   'CONTENT_LENGTH': len(data),
		   "GATEWAY_INTERFACE": "CGI/1.1",
		   'HTTP_COOKIE': msg.get('Cookie'),
		   'HTTP_REFERER': msg.get('Referer'),
		   'HTTP_USER_AGENT': msg.get('User-agent'),
		   'PATH_INFO': path,
		   'QUERY_STRING': query_string,
		   'REMOTE_ADDR': remote_addr,
		   'REMOTE_PORT': str(remote_port),
		   'REQUEST_URI': request.uri,
		   'SCRIPT_NAME': '',
		   "SCRIPT_FILENAME": '',
		   'SERVER_NAME': server_name,
		   'SERVER_PORT': server_port,
		   'SERVER_PROTOCOL': 'HTTP/1.1',
		   'SERVER_SOFTWARE': self.server_name,
		   }

	if self.https:
		   environ['HTTPS'] = 'on'

	# Propagate HTTP headers
	for title, header in msg.items():
	    envname = title.replace('-', '_').upper()
	    if title not in ('content-type', 'content-length'):
		envname = "HTTP_" + envname
	    environ[envname] = header
	for k,v in environ.items():
	    if v == None:
		environ[k] = ''

	stdin = StringIO(data)
	#qreq = self.publisher.create_request(stdin, environ)
	qresponse = self.publisher.process(stdin, environ)
#	try:
#	    self.publisher.parse_request(qreq)
#	    output = self.publisher.process_request(qreq, environ)
#	except PublishError, err:
#	    output = self.publisher.finish_interrupted_request(qreq, err)
#	except:
#	    output = self.publisher.finish_failed_request(qreq)
#
#	qresponse = qreq.response
#	if output:
#	    qresponse.set_body(output)

	# Copy headers from Quixote's HTTP response
	for name, value in qresponse.generate_headers():
	    # XXX Medusa's HTTP request is buggy, and only allows unique
	    # headers.
	    request[name] = value

	request.response(qresponse.status_code)
	request.push(StreamProducer(qresponse.generate_body_chunks()))

#	# XXX should we set a default Last-Modified time?
#	if qresponse.body is not None:
#	    if isinstance(qresponse.body, Stream):
#		request.push(StreamProducer(qresponse.body))
#	    else:
#		request.push(qresponse.body)

	request.done()

class Server:
    """
    Convenience class for starting a Quixote app with Medusa.

    approot: the module which is the root of your Quixote app
    config_file: an (optional) Quixote config file path
    port: the HTTP port at which to run the server
    enable_ptl: ensure that PTL mechanism is started (default: true)
    """

    def __init__(self, approot, create_publisher, config_file=None, port=80,
	       enable_ptl=True, https=False):
	self.approot = approot
	self.config_file = config_file
	self.port = port
	#self.publishclass = publisher
	self.publisher = create_publisher()
	self.https = https
	if enable_ptl:
	    from quixote import enable_ptl
	    enable_ptl()

    def run(self):
	print 'Serving application %r on port %d' % (self.approot, self.port)
	server = http_server.http_server('', self.port)
#	publisher = self.publishclass(self.approot)
#	if self.config_file:
#	    publisher.read_config(self.config_file)
#	publisher.setup_logs()
	dh = QuixoteHandler(self.publisher, self.approot, server, self.https)
	server.install_handler(dh)
	asyncore.loop()

if __name__ == '__main__':
    s = Server('quixote.demo', port=8080)
    s.run()


