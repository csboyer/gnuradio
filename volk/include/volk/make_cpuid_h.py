#!/usr/bin/env python
#
# Copyright 2011 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from xml.dom import minidom
from emit_omnilog import *

def make_cpuid_h(dom) :
    tempstring = "";
    tempstring = tempstring +'/*this file is auto generated by volk_register.py*/';
    tempstring = tempstring +'\n#ifndef INCLUDED_VOLK_CPU_H';
    tempstring = tempstring +'\n#define INCLUDED_VOLK_CPU_H\n\n';
    tempstring = tempstring + emit_prolog();
    tempstring = tempstring + '\n'

    tempstring = tempstring + "struct VOLK_CPU {\n"
    for domarch in dom:
        arch = str(domarch.attributes["name"].value);
        tempstring = tempstring + "    int (*has_" + arch + ") ();\n";
    tempstring = tempstring + "};\n\n";
    tempstring = tempstring + "extern struct VOLK_CPU volk_cpu;\n\n";

    tempstring = tempstring + "void volk_cpu_init ();\n"
    tempstring = tempstring + "unsigned int volk_get_lvarch ();\n"

    tempstring = tempstring + "\n";
    tempstring = tempstring + emit_epilog();
    tempstring = tempstring + "#endif /*INCLUDED_VOLK_CPU_H*/\n"
    
    return tempstring;
