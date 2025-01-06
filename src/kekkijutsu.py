#!/usr/bin/env python3

#
# @author hxAri (hxari)
# @create 07-01-2025 03:00
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

from base64 import b64decode
from builtins import str as Str
from datetime import datetime
from os import chmod, makedirs as mkdir, remove
from os.path import isdir, isfile
from shutil import rmtree
from traceback import format_exception
from typing import Any, final, MutableMapping, Optional

from kekkijutsu.common import puts, typeof
from kekkijutsu.completer import autocomplete
from kekkijutsu.constant import BasePath
from kekkijutsu.logger import Logger


__all__ = [
]



@final
class Kekkijutsu:
	
	comment:Str
	""" Comment Template filename """
	
	encoding:Str
	""" Character Encoding """
	
	kwargs:MutableMapping[Str,Any]
	""" Default Key Arguments """
	
	logger:Logger
	""" Logger Instance """
	
	prompt:Str
	""" Prompt Formatter """
	
	shellexec:Str
	""" Shell Executable filename """
	
	def __init__( self ) -> None:
		
		""" Construct method of class Kekkijutsu """
		
		self.comment = f"{BasePath}/resources/templates/comments.template"
		self.encoding = "UTF-8"
		self.kwargs = {
			"author": "hxari",
			"project": "?",
			"pathname": "."
		}
		self.logger = Logger( self )
		self.prompt:Str = "├╼ [{author}@{project}]─[{pathname}]\n├╼  <<-{label}>"
		self.shellexec = f"{BasePath}/resources/templates/shellexec.template"
	
	def main( self ) -> None:
		
		""" Main program execution """
		
		prefix = "\x20" * 4
		puts( "", start=prefix )
		puts( "· Welcome To Generator", start=prefix )
		puts( "│", start=prefix )
		puts( "├╼ Generator is a powerful Python Project builder.", start=prefix )
		puts( "├╼ Plase input your project name e.g Steganography", start=prefix )
		puts( "│", start=prefix )
		try:
			project = autocomplete( self.prompt.format( **{ **self.kwargs, "label": "project" }), prefix=prefix, values=None )
			# project = autocomplete( self.prompt.format( **{ **self.kwargs, "label": "project" }), prefix=prefix, values=[ "Sample" ] )
			pathname = "/?"
			while not isdir( pathname ):
				pathname = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "label": "pathname" }), prefix=prefix, values=None )
				# pathname = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "label": "pathname" }), prefix=prefix, values=[ "/self/personal/coding/Python/Generator" ] )
				if isdir( f"{pathname}/{project}" ):
					puts( "├╼ Project exists", start=prefix )
					overwrite = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "label": "remove<Y,n>" }), prefix=prefix, values=[ "Y", "y", "N", "n" ] )
					if overwrite in [ "Y", "y" ]:
						rmtree( f"{pathname}/{project}" )
						break
					pathname = "/?"
				elif isfile( f"{pathname}/{project}" ):
					puts( "├╼ Project exists as file", start=prefix )
					overwrite = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "label": "overwrite<Y,n>" }), prefix=prefix, values=[ "Y", "y", "N", "n" ] )
					if overwrite in [ "Y", "y" ]:
						remove( f"{pathname}/{project}" )
						break
					pathname = "/?"
			author = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "pathname": pathname, "label": "author" }), prefix=prefix, values=None )
			github = ""
			puts( "├╼ Have remote repositoy?", start=prefix )
			confirm = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "pathname": pathname, "label": "github<Y,n>" }), prefix=prefix, values=[ "Y", "y", "N", "n" ] )
			if confirm in [ "Y", "y" ]:
				github = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "pathname": pathname, "label": "github" }), prefix=prefix, values=None )
			nickname = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "pathname": pathname, "label": "nickname" }), prefix=prefix, values=None )
			usermail = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "pathname": pathname, "author": nickname, "label": "usermail" }), prefix=prefix, values=None )
			biograph = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "pathname": pathname, "author": nickname, "label": "description" }), prefix=prefix, values=None )
			confirm = autocomplete( self.prompt.format( **{ **self.kwargs, "project": project, "pathname": pathname, "author": nickname, "label": "generate<Y,n>" }), prefix=prefix, values=[ "Y", "y", "N", "n" ] )
			if confirm in [ "Y", "y" ]:
				currtime = datetime.now()
				created = currtime.strftime( "%d-%m-%Y %H:%M" )
				puts( f"├╼ Mkdir {pathname}/{project}", start=prefix )
				mkdir( f"{pathname}/{project}" )
				puts( f"├╼ Mkdir {pathname}/{project}/src", start=prefix )
				mkdir( f"{pathname}/{project}/src" )
				puts( f"├╼ Mkdir {pathname}/{project}/src/{project.lower()}", start=prefix )
				mkdir( f"{pathname}/{project}/src/{project.lower()}" )
				puts( "├╼ Reading template program-comment", start=prefix )
				comments = self.template( "program-comment", formats={
					"year": currtime.year,
					"author": author,
					"github": github,
					"create": created,
					"project": project,
					"nickname": nickname,
					"usermail": usermail,
					"biograph": biograph,
				})
				
				puts( "├╼ Reading template program-configs", start=prefix )
				template = self.template( "program-configs", formats={
					"comment": comments,
					"project": project.lower(),
					"github": github
				})
				filename = f"{pathname}/{project}/.config"
				puts( f"├╼ Writing {filename}", start=prefix )
				self.write( filename, template )
				
				puts( "├╼ Reading template program-main", start=prefix )
				template = self.template( "program-main", formats={ "comment": comments, "project": project.lower() } )
				filename = f"{pathname}/{project}/src/{project.lower()}.py"
				puts( f"├╼ Writing {filename}", start=prefix )
				self.write( filename, template )
				
				puts( "├╼ Reading template program-init", start=prefix )
				template = self.template( "program-init", formats={ "comment": comments, "project": project } )
				filename = f"{pathname}/{project}/src/{project.lower()}/__init__.py"
				puts( f"├╼ Writing {filename}", start=prefix )
				self.write( filename, template )
				
				puts( "├╼ Reading template program-constant", start=prefix )
				template = self.template( "program-constant", formats={ "comment": comments } )
				filename = f"{pathname}/{project}/src/{project.lower()}/constant.py"
				puts( f"├╼ Writing {filename}", start=prefix )
				self.write( filename, template )
				
				puts( "├╼ Reading template program-common", start=prefix )
				template = self.template( "program-common", formats={ "comment": comments, "project": project.lower() } )
				filename = f"{pathname}/{project}/src/{project.lower()}/common.py"
				puts( f"├╼ Writing {filename}", start=prefix )
				self.write( filename, template )
				
				puts( "├╼ Reading template program-logger", start=prefix )
				template = self.template( "program-logger", formats={ "comment": comments, "project": project.lower() } )
				filename = f"{pathname}/{project}/src/{project.lower()}/logger.py"
				puts( f"├╼ Writing {filename}", start=prefix )
				self.write( filename, template )
				
				puts( "├╼ Reading template program-executable", start=prefix )
				template = self.template( "program-executable", formats={ "comment": comments } )
				filename = f"{pathname}/{project}/{project.lower()}"
				puts( f"├╼ Writing {filename}", start=prefix )
				self.write( filename, template )
				puts( f"├╼ Chmod {filename}", start=prefix )
				chmod( filename, 509 )
				
				puts( "├╼ Reading template program-license", start=prefix )
				template = self.template( "program-license", formats={} )
				filename = f"{pathname}/{project}/LICENSE"
				puts( f"├╼ Writing {filename}", start=prefix )
				self.write( filename, template )
				
				puts( "├╼ Reading template program-readme", start=prefix )
				template = self.template( "program-readme", formats={
					"project": project,
					"biograph": biograph
				})
				filename = f"{pathname}/{project}/README.md"
				puts( f"├╼ Writing {filename}", start=prefix )
				self.write( filename, template )
				
				puts( "├╼ Success", start=prefix )
		except Exception as e:
			typing = typeof( e )
			puts( f"├╼ {typing}:", start=prefix )
			traceback = "\x0a".join( format_exception( e ) )
			puts( f"├╼ {traceback}", start=prefix, close=1 )
		puts( "└╴ Program terminated", start=prefix, close=0 )
	
	def template( self, name:Str, formats:Optional[MutableMapping[Str,Any]]=None ) -> Str:
		filename = f"{BasePath}/resources/templates/{name}.template"
		if not isfile( filename ):
			raise FileNotFoundError( f"No such template or file {filename}" )
		template = ""
		with open( filename, "r", encoding=self.encoding ) as fopen:
			template = b64decode( fopen.read() ).decode( self.encoding )
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


if __name__ == "__main__":
	kekkijutsu = Kekkijutsu()
	kekkijutsu.main()
