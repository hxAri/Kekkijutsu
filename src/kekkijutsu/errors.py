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

from builtins import int as Int, str as Str
from typing import Iterable, Optional

from kekkijutsu.common import typeof, traceback


__all__ = [
	"KekkijutsuError",
	"KekkijutsuWarning",
	"Throwable"
]


class Throwable( Exception ):
	
	""" Base Kekkijutsu Throwable """
	
	code:Int
	""" Error Code """
	
	message:Str
	""" Error Message """
	
	previous:Iterable[Exception]
	""" Error Previous Exception or Error """
	
	def __init__( self, message:Str, code:Int=0, previous:Optional[Iterable[Exception]]=None ) -> None:
		
		"""
		Construct method of class Throwable
		
		Parameters:
			message (Str):
				Error message
			code (Int):
				Error code
			previous (Optional[Iterable[Exception]]):
				Previous error
		"""
		
		if not hasattr( previous, "__iter__" ):
			previous = []
		self.previous = previous
		self.message = message
		self.code = code
		
		Exception.__init__( self, message, code, previous )
	
	def __repr__( self ) -> Str:
		return traceback( self, "\x0a" )
	
	def __str__( self ) -> Str:
		return f"{typeof( self )}: {self.code}: {self.message}"
	
	...
	
class KekkijutsuError( Throwable ): """ Base Kekkijutsu Error Class """
class KekkijutsuWarning( Throwable ): """ Base Kekkijutsu Warning Class """
