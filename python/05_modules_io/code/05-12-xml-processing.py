"""XML processing with xml.etree.ElementTree"""
import xml.etree.ElementTree as ET
from pathlib import Path

print("=== Parsing XML ===")
xml_data = """<?xml version="1.0"?>
<library>
    <book id="1" lang="en">
        <title>Learning Python</title>
        <author>Mark Lutz</author>
        <price currency="USD">39.99</price>
    </book>
    <book id="2" lang="en">
        <title>Fluent Python</title>
        <author>Luciano Ramalho</author>
        <price currency="USD">49.99</price>
    </book>
</library>"""

root = ET.fromstring(xml_data)
print(f"Root: {root.tag} ({len(root)} books)")

print("\n=== find() / findall() ===")
for book in root.findall("book"):
    title = book.find("title").text
    author = book.find("author").text
    price = book.find("price").text
    print(f"  {title} by {author} — ${price}")

print("\n=== Attributes with .get() ===")
for book in root.findall("book"):
    book_id = book.get("id")
    lang = book.get("lang")
    print(f"  Book #{book_id} ({lang})")

print("\n=== XPath — with predicate ===")
expensive = root.findall("book[@id='2']")
if expensive:
    print(f"  Expensive book: {expensive[0].find('title').text}")

print("\n=== Creating XML ===")
catalog = ET.Element("catalog")
item = ET.SubElement(catalog, "item", {"sku": "PY101"})
ET.SubElement(item, "name").text = "Python 101"
ET.SubElement(item, "price", {"currency": "USD"}).text = "29.99"

tree = ET.ElementTree(catalog)
tmp = Path("/tmp/catalog.xml")
tree.write(tmp, encoding="utf-8", xml_declaration=True)
print(f"Wrote: {tmp}")
print(tmp.read_text(encoding="utf-8"))
tmp.unlink(missing_ok=True)

print("\n=== Safe parsing (prevent XML bomb) ===")
try:
    ET.fromstring("<!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]><foo>&xxe;</foo>")
    print("  Unsafe parse succeeded (BAD!)")
except ET.ParseError as e:
    print(f"  Safe parse blocked: {e}")

print("\n=== iter() — recursive search ===")
prices = [el.text for el in root.iter("price")]
print(f"  All prices: {prices}")
