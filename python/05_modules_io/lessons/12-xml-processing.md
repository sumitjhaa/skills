# 📄 XML Processing
<!-- ⏱️ 12 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Parse, create, and query XML data using Python's `xml.etree.ElementTree` — still widely used in APIs, configs, and legacy systems.

> 💡 **TL;DR — The whole point:** XML is verbose but powerful. Use `xml.etree.ElementTree` for parsing, `lxml` for advanced XPath, and always parse safely to avoid XML bombs.

## 🔗 Why This Matters
JSON has largely replaced XML for web APIs, but XML is still everywhere: SOAP APIs, RSS/Atom feeds, SVG graphics, Android manifests, Maven POM files, Excel `.xlsx` (it's ZIP + XML), and configuration files. You need to read it, query it, and sometimes write it.

## The Concept

| Task | Function/Method |
|------|----------------|
| Parse XML string | `ET.fromstring(xml_string)` |
| Parse XML file | `ET.parse(file_path)` |
| Get root element | `tree.getroot()` |
| Find first match | `root.find("tag")` |
| Find all matches | `root.findall("tag")` |
| Iterate recursively | `root.iter("tag")` |
| Read attribute | `elem.get("attr")` |
| Read text content | `elem.text` |
| Create new element | `ET.SubElement(parent, "tag")` |
| Write to file | `tree.write(path)` |

### XPath Quick Reference
- `tag` — direct child elements named `tag`
- `.//tag` — descendants named `tag` (any depth)
- `[@attr]` — elements with `attr` attribute
- `[@attr="val"]` — elements where `attr` equals `val`
- `tag[@attr="val"]/child` — chained path

## Code Example

```python
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
ns = {"": "http://example.com/catalog"}
catalog = ET.Element("catalog")
item = ET.SubElement(catalog, "item", {"sku": "PY101"})
ET.SubElement(item, "name").text = "Python 101"
ET.SubElement(item, "price", {"currency": "USD"}).text = "29.99"

tree = ET.ElementTree(catalog)
tmp = Path("/tmp/catalog.xml")
tree.write(tmp, encoding="utf-8", xml_declaration=True)
print(f"Wrote: {tmp}")
print(tmp.read_text(encoding="utf-8"))

print("\n=== Safe parsing (prevent XML bomb) ===")
try:
    ET.fromstring("<!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]><foo>&xxe;</foo>")
    print("  Unsafe parse succeeded (BAD!)")
except ET.ParseError as e:
    print(f"  Safe parse blocked: {e}")

print("\n=== iter() — recursive search ===")
prices = [el.text for el in root.iter("price")]
print(f"  All prices: {prices}")
```

## 🔍 How It Works
- `ET.fromstring()` parses XML text into an element tree; `ET.parse()` reads from a file
- `find()` and `findall()` accept limited XPath (no `//` at start, no `..`, no `|`)
- For full XPath (full `//`, `..`, `|`, functions), use `lxml` (`pip install lxml`)
- `ET.SubElement(parent, tag, attrib)` appends a child and returns it
- `tree.write(path, encoding, xml_declaration)` writes with `<?xml version="1.0"?>`
- Python's `xml.etree` is **not secure** by default against XML External Entity (XXE) attacks — use `defusedxml` for untrusted input

## ⚠️ Common Pitfall
- `root.find("author")` only finds **direct children**. For nested elements, use `.//author` or `root.iter("author")`
- XML is case-sensitive — `root.find("Book")` won't match `<book>`
- Attributes with namespaces need `{uri}attr` syntax or `lxml`'s `xpath()` with namespace maps

## 🧠 Memory Aid
"Find for first, Findall for list, Iter for recursive, Get for attributes."

## 🏃 Try It
Parse an RSS feed XML (fetch one with `httpx`), extract the latest 5 article titles and links using `.//item`, `.//title`, and `.//link`.

## 🔗 Related
- [JSON & CSV](06-json-csv.md) — the other two big data formats
- [Regex](07-regex.md) — text pattern matching (alternative to XML parsing)
- [Web Scraping](../10_ecosystem/lessons/15-web-scraping.md) — extracting data from web pages

## ➡️ Next
Phase 06 — Error Handling
