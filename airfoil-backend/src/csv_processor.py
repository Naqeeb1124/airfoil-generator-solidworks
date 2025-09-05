"""
CSV airfoil data processor
Handles various CSV formats and converts them to standard TXT format
"""

import numpy as np
import re

def parse_airfoil_csv(csv_file_path):
    """
    Parse airfoil data from CSV file
    
    Args:
        csv_file_path (str): Path to the CSV file
    
    Returns:
        tuple: (x_coords, y_coords, airfoil_name, metadata)
    """
    try:
        # Read the entire CSV file
        with open(csv_file_path, 'r') as f:
            content = f.read()
        
        # Split content into lines
        lines = content.strip().split('\n')
        
        # Initialize variables
        airfoil_name = "Unknown Airfoil"
        metadata = {}
        coordinate_data = []
        
        # Parse header information
        in_coordinates = False
        coordinate_section = None
        found_header = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines
            if not line or line == ',':
                continue
            
            # Look for airfoil name
            if line.startswith('Name,'):
                airfoil_name = line.split(',', 1)[1].strip()
                continue
            
            # Check for coordinate section headers FIRST
            if 'airfoil surface' in line.lower() or line.lower().startswith('airfoil surface'):
                coordinate_section = 'surface'
                in_coordinates = False
                found_header = True
                continue
            elif 'camber line' in line.lower():
                coordinate_section = 'camber'
                in_coordinates = False
                continue
            elif 'chord line' in line.lower():
                coordinate_section = 'chord'
                in_coordinates = False
                continue
            
            # Look for metadata (lines with key,value format before coordinates)
            if ',' in line and not in_coordinates and not found_header:
                parts = line.split(',', 1)
                if len(parts) == 2 and parts[0] and parts[1]:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key not in ['X(mm)', 'Y(mm)', 'X', 'Y'] and 'surface' not in key.lower():
                        metadata[key] = value
                continue
            
            # Check for coordinate column headers
            if ('X(' in line and 'Y(' in line) or ('x' in line.lower() and 'y' in line.lower()):
                if coordinate_section == 'surface':
                    in_coordinates = True
                continue
            
            # Parse coordinate data for airfoil surface
            if coordinate_section == 'surface' and ',' in line:
                parts = line.split(',')
                if len(parts) >= 2:
                    try:
                        x_str = parts[0].strip()
                        y_str = parts[1].strip()
                        # Skip header lines and empty values
                        if x_str and y_str and not ('X(' in x_str or 'Y(' in x_str):
                            x = float(x_str)
                            y = float(y_str)
                            coordinate_data.append((x, y))
                    except ValueError:
                        continue
        
        if not coordinate_data:
            raise ValueError("No valid coordinate data found in CSV file")
        
        # Convert to numpy arrays
        coordinates = np.array(coordinate_data)
        x_coords = coordinates[:, 0]
        y_coords = coordinates[:, 1]
        
        # Normalize coordinates if they appear to be in mm or other units
        max_x = np.max(x_coords)
        if max_x > 10:  # Likely in mm or other units, normalize to chord length
            x_coords = x_coords / max_x
            y_coords = y_coords / max_x
        
        return x_coords, y_coords, airfoil_name, metadata
        
    except Exception as e:
        raise ValueError(f"Error parsing CSV file: {str(e)}")

def process_coordinates_for_output(x_coords, y_coords):
    """
    Process coordinates to match airfoiltools.com format
    - Ensure proper ordering (upper surface then lower surface)
    - Remove duplicates at leading/trailing edges
    
    Args:
        x_coords (array): X coordinates
        y_coords (array): Y coordinates
    
    Returns:
        tuple: (processed_x, processed_y)
    """
    # Create coordinate pairs
    coords = list(zip(x_coords, y_coords))
    
    # Find leading edge (minimum x) and trailing edge (maximum x)
    min_x_idx = np.argmin(x_coords)
    max_x_idx = np.argmax(x_coords)
    
    # Separate upper and lower surfaces
    # This is a simplified approach - in practice, you might need more sophisticated logic
    upper_surface = []
    lower_surface = []
    
    for i, (x, y) in enumerate(coords):
        if i <= len(coords) // 2:
            upper_surface.append((x, y))
        else:
            lower_surface.append((x, y))
    
    # Sort upper surface from trailing edge to leading edge (decreasing x)
    upper_surface.sort(key=lambda coord: coord[0], reverse=True)
    
    # Sort lower surface from leading edge to trailing edge (increasing x)
    lower_surface.sort(key=lambda coord: coord[0])
    
    # Remove duplicate leading edge point
    if lower_surface and upper_surface:
        if abs(lower_surface[0][0] - upper_surface[-1][0]) < 1e-6:
            lower_surface = lower_surface[1:]
    
    # Combine surfaces
    all_coords = upper_surface + lower_surface
    
    if all_coords:
        processed_x, processed_y = zip(*all_coords)
        return np.array(processed_x), np.array(processed_y)
    else:
        return x_coords, y_coords

def csv_to_txt_format(csv_file_path, output_file_path=None, solidworks_format=False):
    """
    Convert CSV airfoil data to TXT format
    
    Args:
        csv_file_path (str): Path to input CSV file
        output_file_path (str): Path to output TXT file (optional)
        solidworks_format (bool): If True, format for SolidWorks compatibility
    
    Returns:
        str: Formatted TXT content
    """
    # Parse CSV data
    x_coords, y_coords, airfoil_name, metadata = parse_airfoil_csv(csv_file_path)
    
    # Process coordinates for output
    x_processed, y_processed = process_coordinates_for_output(x_coords, y_coords)
    
    # Format as TXT
    lines = []
    
    if not solidworks_format:
        # Standard format with header
        lines.append(airfoil_name)
        for x, y in zip(x_processed, y_processed):
            lines.append(f"  {x:.6f}  {y:.6f}")
    else:
        # SolidWorks format: three-column, space-delimited, no header, Z=0 for 2D airfoils
        for x, y in zip(x_processed, y_processed):
            lines.append(f"{x:.6f} {y:.6f} 0.000000")
    
    content = "\n".join(lines)
    
    # Save to file if output path provided
    if output_file_path:
        with open(output_file_path, 'w') as f:
            f.write(content)
    
    return content

# Test the processor
if __name__ == "__main__":
    # Test with the sample CSV file
    try:
        csv_path = "/home/ubuntu/upload/b737d-il.csv"
        x, y, name, meta = parse_airfoil_csv(csv_path)
        print(f"Parsed airfoil: {name}")
        print(f"Number of points: {len(x)}")
        print(f"Metadata: {meta}")
        print(f"X range: {np.min(x):.6f} to {np.max(x):.6f}")
        print(f"Y range: {np.min(y):.6f} to {np.max(y):.6f}")
        
        # Test conversion to standard TXT format
        txt_content = csv_to_txt_format(csv_path, solidworks_format=False)
        print(f"\nFirst few lines of standard TXT output:")
        print("\n".join(txt_content.split("\n")[:6]))
        
        # Test conversion to SolidWorks TXT format
        solidworks_content = csv_to_txt_format(csv_path, solidworks_format=True)
        print(f"\nFirst few lines of SolidWorks TXT output:")
        print("\n".join(solidworks_content.split("\n")[:5]))
        
    except Exception as e:
        print(f"Error: {e}")

