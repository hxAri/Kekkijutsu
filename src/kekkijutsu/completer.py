#!/usr/bin/env bash

#
# @author Ari Setiawan
# @create 29.08-2024 00:00
# @github https://github.com/hxAri/Generator
#
# Generator Copyright (c) 2024 - Ari Setiawan <hxari@proton.me>
# Generator Licence under GNU General Public Licence v3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

from builtins import int as Int, str as Str
from prompt_toolkit import ANSI as Ansi, PromptSession
from prompt_toolkit.completion import WordCompleter
from typing import (
	Callable, 
	MutableSequence, 
	Optional, 
	TypeVar as Var, 
	Union
)

from kekkijutsu.common import colorize, puts


__all__ = [
	"autocomplete"
]


_T = Var( "_T" )
""" Return Type """


def autocomplete( prompt:Union[Ansi,Callable[[],Str],Str], values:MutableSequence[Str], prefix:Str="\x20" * 4, typing:_T=Str ) -> Optional[_T]:
	try:
		session = PromptSession( 
			completer=WordCompleter( values \
				if values is not None and values \
				else [] 
			) 
		)
		while True:
			try:
				message = colorize( prompt() if callable( prompt ) is True else prompt )
				message = "".join([ prefix, message.replace( "\x0a", f"\x0a{prefix}" ) ])
				value = session.prompt( Ansi( f"{message} " ) )
				if not value:
					continue
				if values is not None and values:
					if value in values:
						return typing( value )
					continue
				return typing( value )
			except IndexError: ...
			except ValueError: ...
			finally:
				...
	except( EOFError, KeyboardInterrupt ):
		puts( "Aborted", start="\x20" * 4, end="\x0a" * 2, close=1, logging=False )
	return None


if __name__ == "__main__":
	...
