from mcp.server.fastmcp import FastMCP
import ezdxf
import os

mcp = FastMCP("DXF Server")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@mcp.tool()
def server_directory():
    """
    Return the directory containing server.py.
    """
    return BASE_DIR

@mcp.tool()
def list_dxf_files():
    """
    List all DXF files located beside server.py.
    """
    return [f for f in os.listdir(BASE_DIR) if f.lower().endswith(".dxf")]

@mcp.tool()
def create_dxf(filename: str):
    """
    Create a new DXF drawing.
    """
    doc = ezdxf.new()
    path = os.path.join(BASE_DIR, filename)
    doc.saveas(path)
    return f"Created {filename}"

@mcp.tool()
def add_line(filename: str, x1: float, y1: float, x2: float, y2: float):
    """
    Add a line entity.
    """
    path = os.path.join(BASE_DIR, filename)
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    msp.add_line((x1, y1), (x2, y2))
    doc.save()
    return "Line added"

@mcp.tool()
def add_circle(filename: str, center_x: float, center_y: float, radius: float):
    """
    Add a circle entity.
    """
    path = os.path.join(BASE_DIR, filename)
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    msp.add_circle((center_x, center_y), radius)
    doc.save()
    return "Circle added"

@mcp.tool()
def add_arc(filename: str, center_x: float, center_y: float, radius: float, start_angle: float, end_angle: float):
    """
    Add an arc entity.
    """
    path = os.path.join(BASE_DIR, filename)
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    msp.add_arc((center_x, center_y), radius, start_angle, end_angle)
    doc.save()
    return "Arc added"

def _get_entities(filename: str):
    """Internal helper to read and return all modelspace entities."""
    path = os.path.join(BASE_DIR, filename)
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    return doc, msp, list(msp)

@mcp.tool()
def list_entities(filename: str):
    """
    List all entities and their geometry.
    """
    _, _, entities = _get_entities(filename)
    results = []
    for idx, entity in enumerate(entities):
        if entity.dxftype() == "LINE":
            results.append(f"{idx}: LINE start={entity.dxf.start} end={entity.dxf.end}")
            
        elif entity.dxftype() == "CIRCLE":
            results.append(f"{idx}: CIRCLE center={entity.dxf.center} radius={entity.dxf.radius}")
            
        elif entity.dxftype() == "ARC":
            results.append(
                f"{idx}: ARC center={entity.dxf.center} "
                f"radius={entity.dxf.radius} "
                f"start={entity.dxf.start_angle} "
                f"end={entity.dxf.end_angle}"
            )
            
        else:
            results.append(f"{idx}: {entity.dxftype()}")
    return "\n".join(results)

@mcp.tool()
def delete_entity(filename: str, entity_index: int):
    """
    Delete an entity by index. Automatically reads entities first to resolve the correct index.
    """
    doc, msp, entities = _get_entities(filename)

    if entity_index < 0 or entity_index >= len(entities):
        return f"Error: index {entity_index} out of range (file has {len(entities)} entities)"

    entity_type = entities[entity_index].dxftype()
    entities[entity_index].destroy()
    doc.save()
    return f"Deleted entity {entity_index}: {entity_type}"

@mcp.tool()
def update_line(
    filename: str,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    new_x1: float,
    new_y1: float,
    new_x2: float,
    new_y2: float
):
    """
    Update a line by matching its coordinates and replacing them.
    """
    path = os.path.join(BASE_DIR, filename)
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    for entity in msp:
        if entity.dxftype() != "LINE":
            continue
        start = entity.dxf.start
        end = entity.dxf.end
        if (round(start.x, 3) == round(x1, 3)
            and round(start.y, 3) == round(y1, 3)
            and round(end.x, 3) == round(x2, 3)
            and round(end.y, 3) == round(y2, 3)
        ):
            entity.dxf.start = (new_x1, new_y1)
            entity.dxf.end = (new_x2, new_y2)
            doc.save()
            return "Line updated"
    return "Line not found"

@mcp.tool()
def update_circle(
    filename: str,
    center_x: float,
    center_y: float,
    old_radius: float,
    new_center_x: float,
    new_center_y: float,
    new_radius: float
):
    """
    Update a circle's center and radius.
    """
    path = os.path.join(BASE_DIR, filename)
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    for entity in msp:
        if entity.dxftype() != "CIRCLE":
            continue
        center = entity.dxf.center
        radius = entity.dxf.radius
        if (
            round(center.x, 3) == round(center_x, 3)
            and round(center.y, 3) == round(center_y, 3)
            and round(radius, 3) == round(old_radius, 3)
        ):
            entity.dxf.center = (new_center_x, new_center_y)
            entity.dxf.radius = new_radius
            doc.save()
            return "Circle updated"
    return "Circle not found"

@mcp.tool()
def update_arc(
    filename: str,
    center_x: float,
    center_y: float,
    old_radius: float,
    old_start_angle: float,
    old_end_angle: float,
    new_center_x: float,
    new_center_y: float,
    new_radius: float,
    new_start_angle: float,
    new_end_angle: float
):
    """
    Update an arc's center, radius and angles.
    """
    path = os.path.join(BASE_DIR, filename)

    doc = ezdxf.readfile(path)
    msp = doc.modelspace()

    for entity in msp:

        if entity.dxftype() != "ARC":
            continue

        center = entity.dxf.center
        radius = entity.dxf.radius
        start_angle = entity.dxf.start_angle
        end_angle = entity.dxf.end_angle

        if (
            round(center.x, 3) == round(center_x, 3)
            and round(center.y, 3) == round(center_y, 3)
            and round(radius, 3) == round(old_radius, 3)
            and round(start_angle, 3) == round(old_start_angle, 3)
            and round(end_angle, 3) == round(old_end_angle, 3)
        ):
            entity.dxf.center = (new_center_x, new_center_y)
            entity.dxf.radius = new_radius
            entity.dxf.start_angle = new_start_angle
            entity.dxf.end_angle = new_end_angle
            doc.save()
            return "Arc updated"
    return "Arc not found"

if __name__ == "__main__":
    mcp.run(transport="stdio")