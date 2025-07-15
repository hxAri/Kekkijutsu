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

from base64 import b64decode
from builtins import int as Int, str as Str
from os.path import isfile
from re import split
from typing import Any, final, MutableMapping, Optional

from kekkijutsu.constant import BasePath
from kekkijutsu.logger import Logger


__all__ = [
	"Builder"
]


@final
class Builder:
	
	""" Kekkijutsu Builder Implementation """
	
	basepath:Str
	""" Application Base pathname """
	
	comment:Str
	""" Comment Template filename """
	
	encoding:Str
	""" Character Encoding """
	
	kwargs:MutableMapping[Str,Any]
	""" Default Key Arguments """
	
	logger:Logger
	""" Logger Instance """
	
	prefix:Str
	""" Prefix Indentation """
	
	prompt:Str
	""" Prompt Formatter """
	
	shellexec:Str
	""" Shell Executable filename """
	
	def __init__( self, basepath:Optional[Str]=None, prefix:Int=4 ) -> None:
		
		""" Construct method of class Builder """
		
		if basepath is None or not basepath:
			basepath = BasePath
		self.basepath = basepath
		self.comment = f"{basepath}/resources/templates/comments.template"
		self.encoding = "UTF-8"
		self.kwargs = dict(
			author="hxari",
			project="?",
			pathname="."
		)
		self.logger = Logger( self )
		self.prefix = "\x20" * prefix
		self.prompt:Str = "├╼ [{author}@{project}]─[{pathname}]\n├╼  <<-{label}>"
		self.shellexec = f"{basepath}/resources/templates/shellexec.template"
	
	def classname( self, project:Str ) -> Str:
		return "".join( part.capitalize() for part in split( r"(?:-|_|\.)", project ) )
	
	def template( self, name:Str, formats:Optional[MutableMapping[Str,Any]]=None ) -> Str:
		filename = f"{self.basepath}/resources/templates/{name}.template"
		if not isfile( filename ):
			raise FileNotFoundError( f"No such template or file {filename}" )
		template = ""
		with open( filename, "r", encoding=self.encoding ) as fopen:
			flines = list( line for line in fopen.readlines() if line and not line.startswith( "----- BEGIN" ) and not line.startswith( "----- END" ) )
			template = b64decode( "\x0a".join( flines ) ).decode( self.encoding )
			fopen.close()
		if formats is not None and formats:
			for keyset, value in formats.items():
				syntax = "{?={key}}".replace( "{key}", keyset )
				template = template.replace( syntax, Str( value ) )
			...
		return template
	
	def write( self, filename:Str, contents:Str ) -> None:
		with open( filename, "w", encoding=self.encoding ) as fopen:
			fopen.write( contents )
			fopen.close()
		...
	
	...
