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

from builtins import str as Str
from os import getenv
from sys import path as paths
from typing import MutableSequence


__all__ = (
	"BasePath",
	"BaseVenv",
	"HomePath"
)


BaseParts:MutableSequence[Str] = paths[0].split( "\x2f" )
BasePath:Str = "\x2f".join( BaseParts[:BaseParts.index( "src" )] )
""" The Base Path of Application """

BaseParts:MutableSequence[Str] = paths[4].split( "\x2f" )
BaseVenv:Str = "\x2f".join( BaseParts[:BaseParts.index( "lib" )] )
""" The Base Path of Virtual Environment """

HomePath:Str = getenv( "HOME" )
""" The Home Path of User Previlege """

del BaseParts
