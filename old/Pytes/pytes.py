#  pytes.py
#  
#  Copyright 2016 Juan Martínez <mratmartinez@anche.no>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import struct, os.path

class Pyte(object):
    def __init__(self, filename):
        self.filename = filename
        if os.path.isfile(filename) == False:
            self.op = open(filename, "wb")
            self.op.close()
        self.op = open(filename, "r+b")
    
    def write(self, bytel):
        if bytel > 255:
            print("That's more than a byte!")
        elif bytel < 0:
            print("Please, unsigned byte!")
        else:
            packedbyte = struct.pack("B", bytel)
            self.op.write(packedbyte)
    
    def read(self):
        self.op.seek(0)
        return(self.op.read())

    def generator(self):
        self.count = 0
        while self.count <= 255:
            yield self.count
            self.count += 2

    def stapit(self):
        self.op.close()
