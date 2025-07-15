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
from os import getenv, getuid
from pwd import getpwuid
from sys import path as paths
from typing import MutableSequence


__all__ = (
	"BasePath",
	"BaseVenv",
	"HomePath",
	"Username"
)


BaseParts:MutableSequence[Str] = paths[0].split( "\x2f" )
BasePath:Str = "\x2f".join( BaseParts[:BaseParts.index( "src" )] ) if "src" in BaseParts else BaseParts
""" The Base Path of Application """

BaseParts:MutableSequence[Str] = paths[4].split( "\x2f" )
BaseVenv:Str = "\x2f".join( BaseParts[:BaseParts.index( "lib" )] )
""" The Base Path of Virtual Environment """

HomePath:Str = getenv( "HOME" )
""" The Home Path of User Previlege """

Username:Str = "root"
""" Current Username User Previlege """

try:
	Username = getpwuid( getuid() )[0]
except KeyError:
	Username = "root"

del BaseParts
