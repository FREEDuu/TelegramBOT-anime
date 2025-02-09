import os
import json
from pathlib import Path

def list_extensions(browser_type='chrome'):
    # Set path based on browser type
    base_path = Path.home() / '.config'
    if browser_type == 'chrome':
        extensions_path = base_path / 'google-chrome' / 'Default' / 'Extensions'
    else:
        extensions_path = base_path / 'chromium' / 'Default' / 'Extensions'
    
    if not extensions_path.exists():
        return f"No extensions found: {extensions_path} does not exist"
    
    extensions = []
    for ext_id in extensions_path.iterdir():
        for version in ext_id.iterdir():
            manifest_path = version / 'manifest.json'
            if manifest_path.exists():
                with open(manifest_path) as f:
                    manifest = json.load(f)
                    extensions.append({
                        'name': manifest.get('name', 'Unknown'),
                        'id': ext_id.name,
                        'version': version.name
                    })
                break  # Only read the first version found
                
    return extensions

# Usage
extensions = list_extensions('chromium')  # or 'chrome'
for ext in extensions:
    print(ext)