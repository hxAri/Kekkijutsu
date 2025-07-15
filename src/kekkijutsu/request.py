#!/usr/bin/env python3

#
# @author hxAri (hxari)
# @create 15-07-2025 12:39
# @github https://github.com/hxAri/Kekkijutsu
#
# Kekkijutsu is a powerful Python Project builder.
#
# Kekkijutsu Copyright (c) 2025 - hxAri <hxari@proton.me>
# Kekkijutsu Licence under GNU General Public Licence v3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# This program was built and created under Kekkijutsu.
# Visit the github page <https://github.com/hxAri/Kekkijutsu>.
#

from builtins import bool as Bool, int as Int, str as Str
from requests import Response, Session
from requests.exceptions import (
	ConnectionError as RequestConnectionError, 
	ConnectTimeout as RequestConnectionTimeout, 
	RequestException as RequestError
)
from typing import ( 
	Any, 
	MutableMapping, 
	Optional, 
	Tuple, 
	Union
)
from urllib3.exceptions import (
	ConnectionError as UrllibConnectionError,
	ConnectTimeoutError as UrllibConnectTimeoutError,
	RequestError as UrllibRequestError,
	NewConnectionError as UrllibNewConnectionError
)
from urllib.parse import urlparse as urlparser

from kekkijutsu.common import traceback, typeof
from kekkijutsu.logger import Logger


__all__ = [
	"request"
]


_logger:Logger = Logger( __name__ )
""" Logger Instance """


def request( method:Str, url:Str, auth:Tuple[Str,Str]=None, data:MutableMapping[Str,Any]=None, files:MutableMapping[Str,Bytes]=None, cookies:MutableMapping[Str,Str]=None, headers:MutableMapping[Str,Str]=None, params:MutableMapping[Str,Str]=None, payload:MutableMapping[Str,Any]=None, proxies:MutableMapping[Str,Str]=None, session:Optional[Session]=None, stream:Bool=False, verify:Bool=None, timeout:Int=None, tries:Int=10, thread:Union[Int,Str]=0 ) -> Response:
	
	"""
	Send HTTP Request
	
	Parameters:
		method (Str):
			Http request method
		url (Str):
			Http request url target
		auth (Tuple[Str,Str]):
			Http request authentication
		data (MutableMapping[Str,Any]):
			Http request multipart form data
		files (MutableMapping[Str,Bytes]):
			Http request files
		cookies (MutableMapping[Str,Str]):
			Http request cookies
		headers (MutableMapping[Str,Str]):
			Http request headers
		params (MutableMapping[Str,Str]):
			Http request parameters
		payload (MutableMapping[Str,Any]):
			Http request json payload data
		proxies (MutableMapping[Str,Any]):
			Http request proxies
		stream (Bool):
			Allow request stream
		verify (Bool):
			Verify http request
		timeout (Int):
			Http request timeout
		tries (Int):
			Http request timeout tries
		thread (Int|Str):
			Current thread position number
	
	Returns:
		response (Response):
			Request response
	"""
	
	counter = 0
	if session is None or not session:
		session = Session()
	throwned = []
	throwable = [
		RequestConnectionError, 
		RequestConnectionTimeout, 
		RequestError,
		UrllibConnectionError,
		UrllibConnectTimeoutError,
		UrllibRequestError,
		UrllibNewConnectionError
	]
	continueable = ( 
		RequestConnectionError, 
		RequestConnectionTimeout, 
		UrllibConnectionError,
		UrllibConnectTimeoutError,
		UrllibNewConnectionError
	)
	if tries <= 0:
		tries = 10
	urlparsed = urlparser( url )
	source = f"{urlparsed.scheme}://{urlparsed.netloc}{urlparsed.path}"
	while counter <= tries:
		_logger.info( "Request {} url=\"{}\"", method, source, thread=thread )
		try:
			response = session.request( 
				url=url, 
				auth=auth,
				data=data, 
				files=files, 
				json=payload, 
				stream=stream,
				verify=verify,
				method=method, 
				cookies=cookies, 
				headers=headers, 
				timeout=timeout,
				proxies=proxies,
				params=params 
			)
			_logger.info( "Response {} url=\"{}\" code={}", method, source, response.status_code, thread=thread )
			return response
		except BaseException as e:
			instance = type( e )
			throwable.append( e )
			_logger.error( "Uncaught {}: {}", typeof( e ), traceback( e, "\x0a" ), thread=thread )
			if instance in throwable:
				if isinstance( e, continueable ):
					counter += 1
					continue
			if throwned:
				raise ExceptionGroup( f"An error occurred while sending a {method} request to url=\"{url}\"", throwned )
			raise e
	...
