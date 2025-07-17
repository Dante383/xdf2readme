from dataclasses import dataclass
from enum import Enum
import xml.etree.ElementTree as ET

class XdfElementType(Enum):
	CONSTANT = 0
	TABLE = 1
	AXIS = 2
	PATCH = 3

@dataclass
class XdfElement:
	title: str
	description: str
	category_indexes: list[int]
	type: XdfElementType

@dataclass
class XdfAxis(XdfElement):
	# axes don't actually have anything besides title (unit), its all inherited from parent
	pass 

@dataclass
class XdfCategory:
	index: int
	name: str
	elements: list[XdfElement]

@dataclass
class XdfHeader:
	title: str
	author: str
	description: str
	categories: dict[int, XdfCategory]

@dataclass
class Xdf:
	header: XdfHeader
	elements: dict[XdfElementType, XdfElement]

class XdfParser:
	ELEMENT_TAGS: dict[XdfElementType, str] = {
		XdfElementType.CONSTANT: 'XDFCONSTANT',
		XdfElementType.TABLE: 'XDFTABLE',
		XdfElementType.AXIS: 'XDFAXIS',
		XdfElementType.PATCH: 'XDFPATCH'
	}

	def __init__ (self, filename: str) -> None:
		self.filename = filename

	def parse_header (self) -> XdfHeader:
		header = self.root.find('XDFHEADER')
		xdf_header = XdfHeader(
			title=header.find('deftitle').text,
			author=header.find('author').text,
			description=header.find('description').text,
			categories={
				int(category.get('index'), 16): 
				XdfCategory(
					index=int(category.get('index'), 16),
					name=category.get('name'),
					elements=[]
				) for category in header.findall('CATEGORY')
			}
		)
		return xdf_header

	def parse_elements (self, element_type: XdfElementType) -> list[XdfElement]:
		elements = []
		for node in self.root.findall(self.ELEMENT_TAGS[element_type]):
			element = XdfElement(
					title=node.find('title').text,
					description=getattr(node.find('description'), 'text', None),
					category_indexes=[
						int(category.get('category'))-1 # 1-indexed here, but 0-indexed in category defs 
						for category in node.findall('CATEGORYMEM')
					],
					type=element_type
			)

			self.parse_axes(node, element)

			elements.append(element)
			for category_index in element.category_indexes:
				self.xdf_header.categories[category_index].elements.append(element)

		return elements

	def parse_axes (self, table_node, table: XdfElement) -> list[XdfAxis]:
		axes = []
		for node in table_node.findall(self.ELEMENT_TAGS[XdfElementType.AXIS]):
			axis = XdfAxis(
				title=getattr(node.get('units'), 'text', None),
				description=None,
				category_indexes=table.category_indexes,
				type=XdfElementType.AXIS
			)
			self.elements[XdfElementType.AXIS].append(axis) # @TODO: inconsistent, very dirty
		return axes
			

	def parse (self) -> Xdf:
		self.tree = ET.parse(self.filename)
		self.root = self.tree.getroot()

		self.xdf_header = self.parse_header()
		self.elements = {k: [] for k in XdfElementType}

		for element_type in [XdfElementType.CONSTANT, XdfElementType.TABLE, XdfElementType.PATCH]:
			self.elements[element_type] += self.parse_elements(element_type)


		return Xdf(self.xdf_header, self.elements)