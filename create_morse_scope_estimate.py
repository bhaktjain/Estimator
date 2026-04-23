"""
Build a detailed estimate from a provided scope workbook.
"""
import argparse
import os
import re
import csv
import pandas as pd

EXTENSION_AREA = 600  # SF per floor
NEW_BATHROOM_AREA = 60  # SF

category_map = {
    "Demolition": "Demolition",
    "Electrical": "Electrical",
    "Walls & Ceiling": "Drywall & Insulation",
    "Doors": "Doors",
    "Trims": "Trims",
    "Flooring": "Flooring",
    "Painting & Wall Coverings": "Painting & Wall Coverings",
    "Plumbing": "Plumbing",
    "Waterproofing": "Waterproofing",
    "Tile": "Tile",
    "Wall Tiling ": "Tile - Walls",
    "Accessories": "Accessories",
    "Extensions/Additions": "Structural & Framing",
    "Concrete ": "Concrete",
    "Siding ": "Siding & Exterior",
    "Windows": "Windows",
    "Gutters ": "Roofing / Gutters",
}

def qty_value_from_string(qty_str: str) -> float:
    matches = re.findall(r"([\d.]+)", qty_str)
    return float(matches[0]) if matches else 1.0


def format_unit_cost(cost: float, qty_label: str) -> str:
    unit = "UNIT"
    if " " in qty_label:
        unit = qty_label.split()[1]
    return f"${cost:,.2f} per {unit}"

def aggregate_duplicates(rows):
    aggregated = {}
    for row in rows:
        key = (row['Category'], row['Room'], row['ItemName'])
        if key in aggregated:
            existing = aggregated[key]
            existing_total = float(existing['Total'])
            existing['Total'] = f"{existing_total + float(row['Total']):.2f}"
            existing['Description'] = f"{existing['Description']}\n\n---\n{row['Description']}"
            existing['Quantity'] = f"{existing['Quantity']} + {row['Quantity']}"
        else:
            aggregated[key] = row.copy()
    return list(aggregated.values())

def get_pricing(category: str, item_name: str, description: str):
    item = (item_name or "").lower()
    desc = (description or "").lower()

    if category == "Demolition":
        if "pre-construction" in item or "site preparation" in item:
            return {"qty": "1 UNIT", "unit_cost": 2500, "markup": 0.75}
        if "excavation" in item or "grading" in item:
            return {"qty": f"{EXTENSION_AREA} SF", "unit_cost": 15, "markup": 0.75}
        if "bathroom" in desc:
            return {"qty": "1 UNIT", "unit_cost": 3300, "markup": 0.75}
        return {"qty": f"{EXTENSION_AREA} SF", "unit_cost": 7, "markup": 0.75}

    if category == "Electrical":
        if "bathroom" in desc:
            return {"qty": "1 UNIT", "unit_cost": 3500, "markup": 0.75}
        return {"qty": "4 UNIT", "unit_cost": 3500, "markup": 0.75}

    if category == "Drywall & Insulation":
        if "mold" in desc or "moisture" in desc:
            return {"qty": "1 UNIT", "unit_cost": 2200, "markup": 0.75}
        return {"qty": f"{EXTENSION_AREA * 2} SF", "unit_cost": 8, "markup": 0.75}

    if category == "Doors":
        return {"qty": "8 UNIT", "unit_cost": 550, "markup": 0.75}

    if category == "Trims":
        if "base" in desc or "baseboard" in item:
            return {"qty": "350 LF", "unit_cost": 11, "markup": 0.75}
        return {"qty": "200 LF", "unit_cost": 17, "markup": 0.75}

    if category == "Flooring":
        if "2nd" in desc:
            return {"qty": f"{EXTENSION_AREA} SF", "unit_cost": 7, "markup": 0.75}
        if "1st" in desc:
            return {"qty": f"{EXTENSION_AREA} SF", "unit_cost": 8, "markup": 0.75}
        return {"qty": f"{EXTENSION_AREA} SF", "unit_cost": 6, "markup": 0.75}

    if category == "Painting & Wall Coverings":
        return {"qty": f"{EXTENSION_AREA * 2} SF", "unit_cost": 4.5, "markup": 0.75}

    if category == "Plumbing":
        if "bathroom" in desc:
            if "new location" in desc or "extension" in desc:
                return {"qty": "1 UNIT", "unit_cost": 9900, "markup": 0.75}
            return {"qty": "1 UNIT", "unit_cost": 8800, "markup": 0.75}
        return {"qty": "1 UNIT", "unit_cost": 3850, "markup": 0.75}

    if category == "Waterproofing":
        return {"qty": "1 UNIT", "unit_cost": 2100, "markup": 0.75}

    if category == "Tile":
        if "floor" in desc:
            return {"qty": "1 UNIT", "unit_cost": 2000, "markup": 0.80}
        return {"qty": "1 UNIT", "unit_cost": 2600, "markup": 0.80}

    if category == "Tile - Walls":
        return {"qty": "1 UNIT", "unit_cost": 3400, "markup": 0.80}

    if category == "Accessories":
        return {"qty": "1 UNIT", "unit_cost": 2000, "markup": 0.75}

    if category == "Structural & Framing":
        if "exterior wall" in desc:
            return {"qty": f"{EXTENSION_AREA * 2} SF", "unit_cost": 45, "markup": 0.75}
        return {"qty": "1 UNIT", "unit_cost": 25000, "markup": 0.75}

    if category == "Concrete":
        if "footing" in item:
            return {"qty": f"{EXTENSION_AREA} SF", "unit_cost": 18, "markup": 0.75}
        if "slab" in item:
            return {"qty": f"{EXTENSION_AREA} SF", "unit_cost": 20, "markup": 0.75}
        return {"qty": f"{EXTENSION_AREA} SF", "unit_cost": 15, "markup": 0.75}

    if category == "Siding & Exterior":
        return {"qty": f"{EXTENSION_AREA * 2} SF", "unit_cost": 9, "markup": 0.75}

    if category == "Windows":
        return {"qty": "6 UNIT", "unit_cost": 1200, "markup": 0.75}

    if category == "Roofing / Gutters":
        return {"qty": f"{EXTENSION_AREA} LF", "unit_cost": 18, "markup": 0.75}

    # fallback
    return {"qty": "1 UNIT", "unit_cost": 2000, "markup": 0.75}


def write_csv(path, rows):
    fieldnames = [
        "Category",
        "Room",
        "ItemName",
        "Description",
        "Quantity",
        "UnitCost",
        "Markup",
        "MarkupType",
        "Total",
        "Confidence",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_estimate(scope_path, output_dir):
    df = pd.read_excel(scope_path)
    estimate_rows = []
    for _, row in df.iterrows():
        item_name = row.get("ItemName")
        if pd.isna(item_name):
            continue
        category_raw = row.get("Category", "General")
        mapped_category = category_map.get(category_raw, category_raw.strip())
        room = row.get("Room", "General")
        description = row.get("Description", "")
        pricing = get_pricing(mapped_category, str(item_name), str(description))
        qty_label = pricing["qty"]
        base_qty = qty_value_from_string(qty_label)
        base_cost = pricing["unit_cost"] * base_qty
        total = base_cost * (1 + pricing["markup"])

        estimate_rows.append(
            {
                "Category": mapped_category,
                "Room": room,
                "ItemName": item_name,
                "Description": description or item_name,
                "Quantity": qty_label,
                "UnitCost": format_unit_cost(pricing["unit_cost"], qty_label),
                "Markup": str(pricing["markup"]),
                "MarkupType": "",
                "Total": f"{total:.2f}",
                "Confidence": "90",
            }
        )

    estimate_rows = aggregate_duplicates(estimate_rows)

    os.makedirs(output_dir, exist_ok=True)
    full_csv = os.path.join(output_dir, "scope_estimate_full.csv")
    write_csv(full_csv, estimate_rows)
    pd.DataFrame(estimate_rows).to_excel(
        os.path.join(output_dir, "scope_estimate_full.xlsx"), index=False
    )

    # Chapter cost (no markup)
    chapter_rows = []
    total_base = 0.0
    for row in estimate_rows:
        new_row = row.copy()
        markup = float(row.get("Markup", 0) or 0)
        total = float(row["Total"])
        base = total / (1 + markup) if markup else total
        new_row["Total"] = f"{base:.2f}"
        new_row["Markup"] = "0.00"
        total_base += base
        chapter_rows.append(new_row)

    chapter_csv = os.path.join(output_dir, "scope_estimate_chapter_cost_only.csv")
    write_csv(chapter_csv, chapter_rows)
    pd.DataFrame(chapter_rows).to_excel(
        os.path.join(output_dir, "scope_estimate_chapter_cost_only.xlsx"), index=False
    )

    print(f"[SCOPE] Created {len(estimate_rows)} items from {scope_path}")
    print(f"[SCOPE] Total with markups: ${sum(float(r['Total']) for r in estimate_rows):,.2f}")
    print(f"[SCOPE] Chapter cost total: ${total_base:,.2f}")
    print(f"[SCOPE] Outputs in {output_dir}")
    return full_csv, chapter_csv


def main():
    parser = argparse.ArgumentParser(description="Build estimate from scope workbook.")
    parser.add_argument("--scope_excel", required=True, help="Path to scope workbook (xlsx)")
    parser.add_argument(
        "--output_dir",
        required=True,
        help="Directory to write scope-based estimate outputs",
    )
    args = parser.parse_args()
    build_estimate(args.scope_excel, args.output_dir)


if __name__ == "__main__":
    main()

