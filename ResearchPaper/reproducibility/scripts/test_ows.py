import io
from orangecanvas.scheme.readwrite import parse_ows_stream

xml_content = """<?xml version="1.0" encoding="utf-8"?>
<scheme version="2.0" title="Marine Project">
  <nodes/>
  <links/>
</scheme>"""

try:
    stream = io.BytesIO(xml_content.encode("utf-8"))
    res = parse_ows_stream(stream)
    print("Successfully parsed scheme XML:", res.title)
except Exception as e:
    print("Parsing error:", e)
