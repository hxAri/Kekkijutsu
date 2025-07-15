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

from builtins import str as Str
from click.core import Context, Group
from click.decorators import (
	argument as Argument, 
	group, 
	option as Option, 
	pass_context as Instance
)
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from os import chmod, makedirs as mkdir, remove
from os.path import isdir, isfile
from shutil import rmtree
from subprocess import PIPE, Popen
from sys import argv
from typing import final, IO as Io, MutableSequence, Optional, TypeVar as Var
try:
	from typing import Self
except ImportError:
	Self = Var( "Self" )

from kekkijutsu.builder import Builder
from kekkijutsu.commands import *
from kekkijutsu.common import puts, traceback, typeof
from kekkijutsu.completer import autocomplete
from kekkijutsu.constant import BasePath, BaseVenv
from kekkijutsu.helper import Helper
from kekkijutsu.logger import *


__all__ = [
]


@final
@group( cls=Helper )
class Cli: """ Kekkijutsu Command Line Interface """

@final
class Command:
	
	""" Kekkijutsu Command Containers """
	
	logger = Logger( __name__ )
	""" Logger Instance """
	
	@Cli.command( help="Building the program" )
	@Instance
	def builder( context:Context ) -> None:
		builder = Builder( prefix=4 )
		puts( "" )
		puts( "· Welcome To Generator", start=builder.prefix )
		puts( "│", start=builder.prefix )
		puts( "├╼ Generator is a powerful Python Project builder.", start=builder.prefix )
		puts( "├╼ Please input your project name e.g Steganography", start=builder.prefix )
		puts( "│", start=builder.prefix )
		try:
			project = autocomplete( builder.prompt.format( **{ **builder.kwargs, "label": "project" }), prefix=builder.prefix, values=None )
			classname = builder.classname( project )
			module = autocomplete( builder.prompt.format( **{ **builder.kwargs, "label": "module" }), prefix=builder.prefix, values=None )
			module = module.lower()
			pathname = "/?"
			while not isdir( pathname ):
				pathname = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "label": "pathname" }), prefix=builder.prefix, values=None )
				if isdir( f"{pathname}/{project}" ):
					puts( "├╼ Project exists", start=builder.prefix )
					overwrite = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "label": "remove<Y,n>" }), prefix=builder.prefix, values=[ "Y", "y", "N", "n" ] )
					if overwrite in [ "Y", "y" ]:
						rmtree( f"{pathname}/{project}" )
						break
					pathname = "/?"
				elif isfile( f"{pathname}/{project}" ):
					puts( "├╼ Project exists as file", start=builder.prefix )
					overwrite = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "label": "overwrite<Y,n>" }), prefix=builder.prefix, values=[ "Y", "y", "N", "n" ] )
					if overwrite in [ "Y", "y" ]:
						remove( f"{pathname}/{project}" )
						break
					pathname = "/?"
			author = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "pathname": pathname, "label": "author" }), prefix=builder.prefix, values=None )
			github = ""
			puts( "├╼ Have remote repositoy?", start=builder.prefix )
			confirm = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "pathname": pathname, "label": "github<Y,n>" }), prefix=builder.prefix, values=[ "Y", "y", "N", "n" ] )
			if confirm in [ "Y", "y" ]:
				github = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "pathname": pathname, "label": "github" }), prefix=builder.prefix, values=None )
			nickname = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "pathname": pathname, "label": "nickname" }), prefix=builder.prefix, values=None )
			usermail = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "pathname": pathname, "author": nickname, "label": "usermail" }), prefix=builder.prefix, values=None )
			biograph = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "pathname": pathname, "author": nickname, "label": "description" }), prefix=builder.prefix, values=None )
			confirm = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "pathname": pathname, "author": nickname, "label": "generate<Y,n>" }), prefix=builder.prefix, values=[ "Y", "y", "N", "n" ] )
			if confirm in [ "Y", "y" ]:
				currtime = datetime.now()
				created = currtime.strftime( "%d-%m-%Y %H:%M" )
				puts( f"├╼ Mkdir {pathname}/{project}", start=builder.prefix )
				mkdir( f"{pathname}/{project}" )
				puts( f"├╼ Mkdir {pathname}/{project}/src", start=builder.prefix )
				mkdir( f"{pathname}/{project}/src" )
				puts( f"├╼ Mkdir {pathname}/{project}/src/{module}", start=builder.prefix )
				mkdir( f"{pathname}/{project}/src/{module}" )
				puts( "├╼ Reading template program-comment", start=builder.prefix )
				comments = builder.template( "program-comment", formats={
					"year": currtime.year,
					"author": author,
					"github": github,
					"create": created,
					"project": project,
					"nickname": nickname,
					"usermail": usermail,
					"biograph": biograph,
				})
				
				formats = {
					"comment": comments,
					"github": github,
					"module": module,
					"project": project,
					"project.class": classname,
					"project.lower": project.lower(),
					"project.upper": project.upper()
				}
				
				puts( "├╼ Reading template program-configs", start=builder.prefix )
				template = builder.template( "program-configs", formats=formats )
				filename = f"{pathname}/{project}/.config"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Reading template program-main", start=builder.prefix )
				template = builder.template( "program-main", formats=formats )
				filename = f"{pathname}/{project}/src/{project.lower()}.py"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Reading template program-init", start=builder.prefix )
				template = builder.template( "program-init", formats=formats )
				filename = f"{pathname}/{project}/src/{module}/__init__.py"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Reading template program-constant", start=builder.prefix )
				template = builder.template( "program-constant", formats=formats )
				filename = f"{pathname}/{project}/src/{module}/constant.py"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Reading template program-common", start=builder.prefix )
				template = builder.template( "program-common", formats=formats )
				filename = f"{pathname}/{project}/src/{module}/common.py"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Reading template program-errors", start=builder.prefix )
				template = builder.template( "program-errors", formats=formats )
				filename = f"{pathname}/{project}/src/{module}/errors.py"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				support = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "pathname": pathname, "author": nickname, "label": "suport multithreading and multiprocessing<Y,n>" }), prefix=builder.prefix, values=[ "Y", "y", "N", "n" ] )
				if support in [ "Y", "y" ]:
					puts( "├╼ Reading template program-main-multithreading", start=builder.prefix )
					template = builder.template( "program-main-multithreading", formats=formats )
					filename = f"{pathname}/{project}/src/{project.lower()}.py"
					puts( f"├╼ Writing {filename}", start=builder.prefix )
					builder.write( filename, template )
					puts( "├╼ Reading template program-futures", start=builder.prefix )
					template = builder.template( "program-futures", formats=formats )
					filename = f"{pathname}/{project}/src/{module}/futures.py"
					puts( f"├╼ Writing {filename}", start=builder.prefix )
					builder.write( filename, template )
				
				support = autocomplete( builder.prompt.format( **{ **builder.kwargs, "project": project, "pathname": pathname, "author": nickname, "label": "suport kafka<Y,n>" }), prefix=builder.prefix, values=[ "Y", "y", "N", "n" ] )
				if support in [ "Y", "y" ]:
					puts( "├╼ Reading template program-kafka", start=builder.prefix )
					template = builder.template( "program-kafka", formats=formats )
					filename = f"{pathname}/{project}/src/{module}/kafka.py"
					puts( f"├╼ Writing {filename}", start=builder.prefix )
					builder.write( filename, template )
				
				puts( "├╼ Reading template program-gitignore", start=builder.prefix )
				template = builder.template( "program-gitignore", formats=formats )
				filename = f"{pathname}/{project}/.gitignore"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Reading template program-logger", start=builder.prefix )
				template = builder.template( "program-logger", formats=formats )
				filename = f"{pathname}/{project}/src/{module}/logger.py"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Reading template program-request", start=builder.prefix )
				template = builder.template( "program-request", formats=formats )
				filename = f"{pathname}/{project}/src/{module}/request.py"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Reading template program-executable", start=builder.prefix )
				template = builder.template( "program-executable", formats=formats )
				filename = f"{pathname}/{project}/{project.lower()}"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				puts( f"├╼ Chmod {filename}", start=builder.prefix )
				chmod( filename, 509 )
				
				puts( "├╼ Reading template program-license", start=builder.prefix )
				template = builder.template( "program-license", formats=formats )
				filename = f"{pathname}/{project}/LICENSE"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Reading template program-readme", start=builder.prefix )
				template = builder.template( "program-readme", formats={
					"project": project,
					"biograph": biograph
				})
				filename = f"{pathname}/{project}/README.md"
				puts( f"├╼ Writing {filename}", start=builder.prefix )
				builder.write( filename, template )
				
				puts( "├╼ Success", start=builder.prefix )
		except Exception as e:
			puts( "├╼ {}:".format( typeof( e ) ), start=builder.prefix )
			puts( "├╼ {}".format( traceback( e, "\x0a" ) ), start=builder.prefix, close=1 )
		puts( "└╴ Program terminated", start=builder.prefix, close=0 )
	
	@Cli.command( help="Testing the program" )
	@Argument( "testing", required=False, type=Str )
	@Option( "--params", help="Testing parameters", required=False, type=Str )
	@Instance
	def testing( context:Context, testing:Str, params:Optional[Str]=None ) -> None:
		
		def callback( label:Str, logger:Logger[Command], stream:Io[Str] ) -> None:
			
			"""
			Thread callback handler for print output from stream
			
			Parameters:
				label (Str):
					Label os stream
				logger (Logger):
					Logger instance
				stream (Io[Str]):
					Stream process
			"""
			
			for line in iter( stream.readline, "" ):
				logger.debug( "{}: {}", label, line.replace( "\x0a", "" ), end="\x0a" )
			...
		
		logger = Command.logger
		if testing is not None:
			puts( f"Executing program src/tests/{testing}.py {params}" )
			process = Popen( 
				args=[
					f"{BaseVenv}/bin/python",
					f"-u",
					f"{BasePath}/src/tests/{testing}.py",
					f"" if params is None else params
				],
				bufsize=1,
				stderr=PIPE,
				stdout=PIPE,
				stdin=PIPE,
				text=True
			)
			with ThreadPoolExecutor( 2 ) as pool:
				futures = []
				futures:MutableSequence[Future]
				futures.append( pool.submit( callback, "Stdout", logger, process.stdout ) )
				futures.append( pool.submit( callback, "Stderr", logger, process.stderr ) )
				while process.poll() is None:
					...
			process.stdout.close()
			process.stderr.close()
			code = process.returncode
			if code == 0:
				logger.debug( "Execution program is success", close=0 )
			else:
				logger.debug( "Execution program is failed" )
				logger.debug( f"Execution program has return code {code}", close=code )
		try:
			...
		except BaseException as e:
			logger.error( "\x3a\x20".join([ typeof( e ), traceback( e, "\x0a" ) ]) )
		...
	
	...

@final
class Kekkijutsu:
	
	""" Kekkijutsu Main Program """
	
	commands:MutableSequence[Group]
	""" Registered commands """
	
	logger:Logger[Self]
	""" Logger Instance """
	
	def __init__( self ) -> None:
		
		""" Construct method of class Kekkijutsu """
		
		disabled = "--logging-store-disabled"
		enabled = "--logging-store-enabled"
		verbose = "--verbose"
		if verbose in argv:
			del argv[argv.index( verbose )]
			threshold( Level.VERBOSE )
		else:
			threshold( Level.DISABLE )
		if disabled in argv:
			del argv[argv.index( disabled )]
			disableStoreLog()
		elif enabled in argv:
			del argv[argv.index( enabled )]
			enableStoreLog()
		
		self.commands = [
		]
		self.logger = Logger( self )
	
	def main( self ) -> None:
		
		""" Main Program execution """
		
		self.logger.info( "Starting application with argv: {}", argv[1:] )
		for command in self.commands:
			self.logger.info( "Registering command: {}[{}]", typeof( command ), command.name )
			Cli.add_command( command )
		self.logger.info( "Instantiate command line interface: {}", typeof( Cli ) )
		status = 0
		try:
			Cli( obj={})
		except Exception as e:
			status = e.code if hasattr( e, "code" ) and e.code != 0 else 1
			puts( "\x3a\x20".join([ typeof( e ), traceback( e, "\x0a" ) ]) )
		except SystemExit as e:
			status = e.code
		finally:
			self.logger.info( "Program terminated with status: {}", status )
			puts( close=status )
		...
	
	...


if __name__ == "__main__":
	main = Kekkijutsu()
	main.main()
