#!/usr/bin/env python3
"""Validate generated editorial .drawio XML."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SELF_TEST_XML = """<mxGraphModel background="#F2EFE8" grid="0" tooltips="0" connect="0" arrows="0" fold="0" page="0" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="border" value="" style="rounded=1;arcSize=3;fillColor=none;strokeColor=#B9B3AB;strokeWidth=1.5;pointerEvents=0;" vertex="1" parent="1">
      <mxGeometry x="20" y="20" width="1614" height="600" as="geometry"/>
    </mxCell>
    <mxCell id="title" value="Sample Diagram" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;fontStyle=1;fontSize=32;fontColor=#1F1F1C;" vertex="1" parent="1">
      <mxGeometry x="80" y="40" width="1200" height="50" as="geometry"/>
    </mxCell>
    <mxCell id="n1" value="Start" style="rounded=1;whiteSpace=wrap;arcSize=50;fillColor=#F8E9E1;strokeColor=#D88966;strokeWidth=1.8;fontColor=#D88966;fontSize=20;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="140" y="180" width="160" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="n2" value="Done" style="rounded=1;whiteSpace=wrap;arcSize=10;fillColor=#CFE8D7;strokeColor=#71AE88;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;" vertex="1" parent="1">
      <mxGeometry x="380" y="180" width="160" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="e1" edge="1" source="n1" target="n2" style="endArrow=open;endSize=14;edgeStyle=orthogonalEdgeStyle;strokeColor=#7A756E;strokeWidth=1.8;rounded=1;" parent="1">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>"""


def parse_xml(text: str) -> ET.Element:
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise ValueError(f"XML parse failed: {exc}") from exc

    if root.tag == "mxGraphModel":
        return root

    if root.tag == "mxfile":
        diagram = root.find("diagram")
        if diagram is None or not diagram.text:
            raise ValueError("mxfile wrapper does not contain a readable diagram payload")
        payload = diagram.text.strip()
        if not payload.startswith("<mxGraphModel"):
            raise ValueError("compressed mxfile payload is not supported by this validator")
        try:
            return ET.fromstring(payload)
        except ET.ParseError as exc:
            raise ValueError(f"uncompressed mxfile diagram XML parse failed: {exc}") from exc

    raise ValueError(f"expected mxGraphModel or mxfile root, got {root.tag!r}")


def style_value(style: str, key: str) -> str | None:
    match = re.search(rf"(?:^|;){re.escape(key)}=([^;]+)", style)
    return match.group(1) if match else None


def is_grid_aligned(value: str) -> bool:
    try:
        number = float(value)
    except ValueError:
        return False
    return number.is_integer() and int(number) % 10 == 0


def collect_cells(model: ET.Element) -> list[ET.Element]:
    graph_root = model.find("root")
    if graph_root is None:
        raise ValueError("mxGraphModel is missing root element")
    return list(graph_root.findall("mxCell"))


def validate_model(model: ET.Element) -> list[str]:
    errors: list[str] = []
    cells = collect_cells(model)
    by_id = {cell.get("id"): cell for cell in cells if cell.get("id")}

    background = model.get("background")
    if background not in {"#F2EFE8", "#FFFFFF"}:
        errors.append("mxGraphModel background must be #F2EFE8 or #FFFFFF")

    border = by_id.get("border")
    if border is None:
        errors.append('missing mxCell id="border"')
    else:
        graph_cells = [cell for cell in cells if cell.get("id") not in {"0", "1"}]
        if not graph_cells or graph_cells[0].get("id") != "border":
            errors.append('border must be the first graph cell after id="0" and id="1"')
        style = border.get("style", "")
        if style_value(style, "rounded") != "1":
            errors.append("border must use rounded=1")
        if style_value(style, "pointerEvents") != "0":
            errors.append("border must use pointerEvents=0")
        geometry = border.find("mxGeometry")
        if geometry is None:
            errors.append("border is missing mxGeometry")
        else:
            expected = {"x": "20", "y": "20", "width": "1614"}
            for key, expected_value in expected.items():
                if geometry.get(key) != expected_value:
                    errors.append(f"border geometry {key} must be {expected_value}")

    title = by_id.get("title")
    if title is None:
        errors.append('missing mxCell id="title"')
    else:
        style = title.get("style", "")
        font_size = style_value(style, "fontSize")
        try:
            parsed_font_size = int(float(font_size or "0"))
        except ValueError:
            parsed_font_size = 0
        if parsed_font_size < 28:
            errors.append("title fontSize must be at least 28")
        if style_value(style, "fontColor") != "#1F1F1C":
            errors.append("title fontColor must be #1F1F1C")

    for cell in cells:
        cell_id = cell.get("id", "<missing-id>")
        geometry = cell.find("mxGeometry")
        if cell.get("edge") == "1":
            style = cell.get("style", "")
            if "endArrow=open" not in style or "endSize=14" not in style:
                errors.append(f"edge {cell_id} must use endArrow=open and endSize=14")
            if "edgeStyle=orthogonalEdgeStyle" not in style:
                errors.append(f"edge {cell_id} must use edgeStyle=orthogonalEdgeStyle")
            if "endArrow=block" in style or "endFill=1" in style:
                errors.append(f"edge {cell_id} must not use filled/block arrowheads")
            if geometry is None:
                errors.append(f"edge {cell_id} is missing mxGeometry")
            elif geometry.get("relative") != "1" or geometry.get("as") != "geometry":
                errors.append(f"edge {cell_id} geometry must be relative=1 as=geometry")

        if geometry is not None:
            for key in ("x", "y"):
                value = geometry.get(key)
                if value is not None and not is_grid_aligned(value):
                    errors.append(f"cell {cell_id} geometry {key}={value} is not on a 10px grid")

    return errors


def validate_text(text: str) -> list[str]:
    model = parse_xml(text)
    return validate_model(model)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated editorial .drawio XML.")
    parser.add_argument("path", nargs="?", type=Path, help="Path to a .drawio file")
    parser.add_argument("--self-test", action="store_true", help="Validate the built-in sample XML")
    args = parser.parse_args()

    if args.self_test:
        errors = validate_text(SELF_TEST_XML)
        if errors:
            print("Self-test failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Self-test passed")
        return 0

    if args.path is None:
        parser.error("path is required unless --self-test is used")

    try:
        text = args.path.read_text(encoding="utf-8")
        errors = validate_text(text)
    except OSError as exc:
        print(f"Failed to read {args.path}: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if errors:
        print(f"{args.path}: validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"{args.path}: validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
