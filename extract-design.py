import json
import re
from collections import defaultdict

# Read the full Figma file data
with open('figma-data.json', 'r', encoding='utf-8-sig') as f:
    full_data = json.load(f)

# Read nodes if available
try:
    with open('figma-nodes.json', 'r', encoding='utf-8') as f:
        nodes_data = json.load(f)
except:
    nodes_data = None

def rgb_to_hex(r, g, b):
    """Convert RGB (0-1) to hex"""
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def extract_design_system(node, path="", depth=0):
    """Recursively extract design system information"""
    info = {
        'name': node.get('name', ''),
        'type': node.get('type', ''),
        'path': path,
        'colors': [],
        'fonts': {},
        'layout': {},
        'children': []
    }
    
    # Extract colors from fills
    if 'fills' in node and node['fills']:
        for fill in node['fills']:
            if fill.get('type') == 'SOLID' and 'color' in fill:
                c = fill['color']
                hex_color = rgb_to_hex(c['r'], c['g'], c['b'])
                info['colors'].append({
                    'hex': hex_color,
                    'rgba': f"rgba({int(c['r']*255)}, {int(c['g']*255)}, {int(c['b']*255)}, {c.get('a', 1.0)})",
                    'opacity': c.get('a', 1.0)
                })
    
    # Extract text styles
    if 'style' in node:
        style = node['style']
        if 'fontFamily' in style:
            info['fonts'] = {
                'fontFamily': style.get('fontFamily', ''),
                'fontSize': style.get('fontSize', ''),
                'fontWeight': style.get('fontWeight', ''),
                'letterSpacing': style.get('letterSpacing', {}),
                'lineHeight': style.get('lineHeightPx', ''),
                'textAlign': style.get('textAlign', '')
            }
    
    # Extract layout properties
    if 'absoluteBoundingBox' in node:
        bbox = node['absoluteBoundingBox']
        info['layout'] = {
            'x': bbox.get('x', 0),
            'y': bbox.get('y', 0),
            'width': bbox.get('width', 0),
            'height': bbox.get('height', 0)
        }
    
    info['layout'].update({
        'cornerRadius': node.get('cornerRadius', 0),
        'paddingLeft': node.get('paddingLeft', 0),
        'paddingRight': node.get('paddingRight', 0),
        'paddingTop': node.get('paddingTop', 0),
        'paddingBottom': node.get('paddingBottom', 0),
        'layoutMode': node.get('layoutMode', ''),
        'layoutGrow': node.get('layoutGrow', 0),
        'layoutAlign': node.get('layoutAlign', ''),
        'gap': node.get('itemSpacing', 0)
    })
    
    # Recursively process children
    if 'children' in node and depth < 10:  # Limit depth to avoid too much recursion
        for child in node['children']:
            child_path = f"{path}/{node.get('name', '')}" if path else node.get('name', '')
            child_info = extract_design_system(child, child_path, depth + 1)
            info['children'].append(child_info)
    
    return info

# Extract design from main frame (node 1-2)
design_system = {}
document = full_data.get('document', {})

if 'children' in document:
    for page in document['children']:
        if 'children' in page:
            for frame in page['children']:
                frame_id = frame.get('id', '')
                if frame_id in ['1:2', '1-2'] or 'Frame' in frame.get('name', ''):
                    design_system = extract_design_system(frame)
                    break

# Save extracted design system
with open('design-system.json', 'w', encoding='utf-8') as f:
    json.dump(design_system, f, indent=2, ensure_ascii=False)

# Extract unique colors
all_colors = set()
def collect_colors(node):
    for color in node.get('colors', []):
        all_colors.add(color['hex'])
    for child in node.get('children', []):
        collect_colors(child)

collect_colors(design_system)

# Print summary
print("=== Design System Summary ===")
print(f"\nComponent: {design_system.get('name', 'Unknown')}")
print(f"Type: {design_system.get('type', 'Unknown')}")
print(f"\nUnique Colors Found: {len(all_colors)}")
for color in sorted(all_colors):
    print(f"  {color}")

print(f"\nDesign system saved to design-system.json")

