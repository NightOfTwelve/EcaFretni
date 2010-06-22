#	
#	symbol.py ... Symbols
#	Copyright (C) 2010  KennyTM~ <kennytm@gmail.com>
#	
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#	
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#	
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#	

from data_table import DataTable
from .macho import MachO
from monkey_patching import patch


class Symbol(object):
	"""A symbol in Mach-O file.
	
	.. attribute:: name
	
		The name of the symbol.
	
	.. attribute:: addr
	
		The address of the symbol
	
	.. attribute:: ordinal
	
		Index of this symbol in the local symbol table.
	
	.. attribute:: library
	
		The :class:`~macho.loadcommands.dylib.DylibCommand` object associated
		with this symbol.
	
	.. attribute:: extern
	
		A boolean indicating whether this is an external symbol.
	
	
	"""
	
	def __init__(self, name, addr, ordinal=-1, library=None, extern=False):
		self.name = name
		self.addr = addr
		self.ordinal = ordinal
		self.library = library
		self.extern = extern
	
	def copy(self):
		'''Create a copy of this symbol.'''
		return type(self)(self.name, self.addr, self.ordinal, self.library, self.extern)
	
	def _toTuple(self):
		return (self.name, self.addr, self.ordinal, self.library.offset if self.library else 0, self.extern)

	def __eq__(self, other):
		return self._toTuple() == other._toTuple()
	
	def __hash__(self):
		return hash(self._toTuple())
		
	
	def __str__(self):
		return "<Symbol {!r}:0x{:x}>".format(self.name, self.addr)
		
	def __repr__(self):
		args = [repr(self.name), '0x{:x}'.format(self.addr)]
		if self.ordinal >= 0:
			args.append('ordinal={!r}'.format(self.ordinal))
		if self.library is not None:
			args.append('library={!r}'.format(self.library))
		if self.extern:
			args.append('extern=True')
		return 'Symbol({})'.format(', '.join(args))


@patch
class MachO_SymbolPatches(MachO):
	'''
	This patch adds method to the :class:`~macho.macho.MachO` class for symbol
	processing.
	
	.. attribute:: symbols
	
		Returns a :class:`~data_table.DataTable` of :class:`Symbol`\\s ordered
		by insertion order, with the following column names: ``'name'``,
		``'addr'`` and ``'ordinal'``.
		
	'''

	def addSymbols(self, symbols):
		'''Add an iterable of :class:`Symbol`\\s to this Mach-O object.'''
	
		if not hasattr(self, 'symbols'):
			self.symbols = DataTable('name', 'addr', 'ordinal')
		
		self_symbols_append = self.symbols.append
		for sym in symbols:
			self_symbols_append(sym, name=sym.name, addr=sym.addr, ordinal=sym.ordinal)
		
