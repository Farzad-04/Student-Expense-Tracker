import json
import re

# Read the Figma data
with open('figma-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract colors, fonts, and layout information
design_tokens = {
    'colors': [],
    'fonts': [],
    'spacing': [],
    'components': []
}

def extract_colors(node, path=""):
    """Extract color information from nodes"""
    if 'fills' in node:
        for fill in node['fills']:
            if fill.get('type') == 'SOLID' and 'color' in fill:
                color = fill['color']
                r = int(color['r'] * 255)
                g = int(color['g'] * 255)
                b = int(color['b'] * 255)
                a = color.get('a', 1.0)
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                design_tokens['colors'].append({
                    'name': node.get('name', 'Unknown'),
                    'path': path,
                    'hex': hex_color,
                    'rgba': f"rgba({r}, {g}, {b}, {a})",
                    'rgb': f"rgb({r}, {g}, {b})"
                })
    
    if 'children' in node:
        for child in node['children']:
            child_path = f"{path}/{node.get('name', '')}" if path else node.get('name', '')
            extract_colors(child, child_path)

def extract_fonts(node):
    """Extract font information"""
    if 'style' in node:
        style = node['style']
        if 'fontFamily' in style or 'fontSize' in style:
            design_tokens['fonts'].append({
                'name': node.get('name', 'Unknown'),
                'fontFamily': style.get('fontFamily', ''),
                'fontSize': style.get('fontSize', ''),
                'fontWeight': style.get('fontWeight', ''),
                'letterSpacing': style.get('letterSpacing', ''),
                'lineHeight': style.get('lineHeightPx', '')
            })
    
    if 'children' in node:
        for child in node['children']:
            extract_fonts(child)

def extract_layout(node, path=""):
    """Extract layout and component information"""
    if node.get('type') in ['FRAME', 'COMPONENT', 'INSTANCE', 'GROUP']:
        layout_info = {
            'name': node.get('name', 'Unknown'),
            'type': node.get('type', ''),
            'path': path,
            'width': node.get('absoluteBoundingBox', {}).get('width', 0),
            'height': node.get('absoluteBoundingBox', {}).get('height', 0),
            'x': node.get('absoluteBoundingBox', {}).get('x', 0),
            'y': node.get('absoluteBoundingBox', {}).get('y', 0),
            'padding': node.get('paddingLeft', 0),
            'cornerRadius': node.get('cornerRadius', 0),
            'layoutMode': node.get('layoutMode', ''),
            'layoutGrow': node.get('layoutGrow', 0),
            'layoutAlign': node.get('layoutAlign', '')
        }
        design_tokens['components'].append(layout_info)
    
    if 'children' in node:
        for child in node['children']:
            child_path = f"{path}/{node.get('name', '')}" if path else node.get('name', '')
            extract_layout(child, child_path)

# Extract information from the document
document = data.get('document', {})
if 'children' in document:
    for page in document['children']:
        if 'children' in page:
            for frame in page['children']:
                extract_colors(frame)
                extract_fonts(frame)
                extract_layout(frame)

# Save extracted tokens
with open('design-tokens.json', 'w', encoding='utf-8') as f:
    json.dump(design_tokens, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(design_tokens['colors'])} colors")
print(f"Extracted {len(design_tokens['fonts'])} font styles")
print(f"Extracted {len(design_tokens['components'])} components")
print("\nDesign tokens saved to design-tokens.json")

# Print some key colors
print("\n=== Key Colors ===")
unique_colors = {}
for color in design_tokens['colors']:
    if color['hex'] not in unique_colors:
        unique_colors[color['hex']] = color
        print(f"{color['name']}: {color['hex']} ({color['rgb']})")

