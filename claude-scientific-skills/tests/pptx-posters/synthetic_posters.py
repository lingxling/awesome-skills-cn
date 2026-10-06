"""Synthetic manifest builders for local, claim-free tests."""

from __future__ import annotations

from typing import Any


def build_manifest(
    manifest_content_hash: Any,
    *,
    include_image: bool = False,
    image_sha256: str = "0" * 64,
    image_path: str = "synthetic.png",
    printer_color_mode: str = "RGB",
) -> dict[str, Any]:
    """Return a complete synthetic manifest and bind its approval hash."""
    sources: list[dict[str, Any]] = [
        {
            "id": "SRC-CONFERENCE",
            "kind": "conference_rule",
            "citation": "Synthetic test conference rule; no external claim.",
            "locator": "local-test-conference-record",
            "author_verified": True,
        },
        {
            "id": "SRC-PRINTER",
            "kind": "printer_rule",
            "citation": "Synthetic test printer rule; no external claim.",
            "locator": "local-test-printer-record",
            "author_verified": True,
        },
        {
            "id": "SRC-CONTENT",
            "kind": "author_content",
            "citation": "Synthetic test content; no scientific claim.",
            "locator": "local-test-content-record",
            "author_verified": True,
        },
    ]
    assets: list[dict[str, Any]] = []
    elements: list[dict[str, Any]] = [
        {
            "id": "title",
            "type": "text",
            "reading_order": 1,
            "x_in": 0.5,
            "y_in": 0.5,
            "width_in": 9.0,
            "height_in": 1.0,
            "source_ids": ["SRC-CONTENT"],
            "author_approved": True,
            "allow_in_bleed": False,
            "role": "title",
            "text": "Synthetic layout test",
            "font_size_pt_design": 28.0,
            "font_face": "Arial",
            "bold": True,
            "align": "left",
            "vertical_align": "middle",
            "contrast_pair_id": "black_on_white",
            "line_color_id": None,
            "line_width_pt": 0,
            "margin_in": 0.1,
        },
        {
            "id": "body",
            "type": "text",
            "reading_order": 2,
            "x_in": 0.5,
            "y_in": 1.5,
            "width_in": 9.0 if not include_image else 4.0,
            "height_in": 6.0,
            "source_ids": ["SRC-CONTENT"],
            "author_approved": True,
            "allow_in_bleed": False,
            "role": "body",
            "text": "Synthetic text used only to test deterministic local generation.",
            "font_size_pt_design": 18.0,
            "font_face": "Arial",
            "bold": False,
            "align": "left",
            "vertical_align": "top",
            "contrast_pair_id": "black_on_white",
            "line_color_id": None,
            "line_width_pt": 0,
            "margin_in": 0.1,
        },
    ]
    if include_image:
        sources.append(
            {
                "id": "SRC-ASSET",
                "kind": "asset_license",
                "citation": "Synthetic test image generated locally by the test.",
                "locator": "local-test-image",
                "author_verified": True,
            }
        )
        assets.append(
            {
                "id": "ASSET-IMAGE",
                "path": image_path,
                "role": "figure",
                "sha256": image_sha256,
                "source_id": "SRC-ASSET",
                "license": "Synthetic test fixture only.",
                "provenance": (
                    "Created locally by the synthetic test from fixed drawing commands."
                ),
                "alt_text": (
                    "Blue rectangle on white used only to verify local image placement."
                ),
                "author_approved": True,
                "qr_target": None,
            }
        )
        elements.append(
            {
                "id": "image",
                "type": "image",
                "reading_order": 3,
                "x_in": 4.5,
                "y_in": 1.5,
                "width_in": 5.0,
                "height_in": 6.0,
                "source_ids": ["SRC-ASSET"],
                "author_approved": True,
                "allow_in_bleed": False,
                "asset_id": "ASSET-IMAGE",
                "fit": "contain",
                "fallback_text_element_id": None,
                "long_description_element_id": None,
            }
        )

    manifest: dict[str, Any] = {
        "schema_version": "2.0",
        "document": {
            "id": "synthetic-test",
            "title": "Synthetic layout test",
            "subject": "Synthetic test input with no scientific claim.",
            "language": "en-US",
            "authors": ["Test Author"],
            "source_ids": ["SRC-CONTENT"],
        },
        "canvas": {
            "width_in": 10.0,
            "height_in": 8.0,
            "background_color": "#FFFFFF",
        },
        "physical_output": {
            "trim_width_in": 10.0,
            "trim_height_in": 8.0,
            "bleed_in": 0.0,
            "safe_margin_in": 0.5,
            "orientation": "landscape",
        },
        "requirements": {
            "conference": {
                "confirmed": True,
                "source_id": "SRC-CONFERENCE",
                "max_width_in": 10.0,
                "max_height_in": 8.0,
                "orientation": "landscape",
                "required_delivery_format": "PPTX",
                "notes": "Synthetic local requirement used only by tests.",
            },
            "printer": {
                "confirmed": True,
                "source_id": "SRC-PRINTER",
                "trim_width_in": 10.0,
                "trim_height_in": 8.0,
                "bleed_in": 0.0,
                "safe_margin_in": 0.5,
                "accepted_color_mode": printer_color_mode,
                "scaling_allowed": False,
                "notes": "Synthetic local printer record used only by tests.",
            },
        },
        "quality": {
            "minimum_font_pt_final": 18.0,
            "font_guidance_basis": "heuristic",
            "font_guidance_source_id": None,
            "minimum_raster_dpi_final": 100.0,
            "raster_dpi_basis": "heuristic",
            "raster_dpi_source_id": None,
        },
        "palette": {
            "colors": {"black": "#000000", "white": "#FFFFFF"},
            "contrast_pairs": [
                {
                    "id": "black_on_white",
                    "foreground_color_id": "black",
                    "background_color_id": "white",
                    "usage": "normal_text",
                }
            ],
            "data_series_redundant_encoding": True,
        },
        "sources": sources,
        "assets": assets,
        "elements": elements,
        "approval": {
            "status": "approved",
            "approved_by": "Test Author",
            "approved_at": "2026-07-23T12:00:00+00:00",
            "content_sha256": "",
        },
    }
    manifest["approval"]["content_sha256"] = manifest_content_hash(manifest)
    return manifest
