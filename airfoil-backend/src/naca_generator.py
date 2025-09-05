"""
NACA 4-digit airfoil coordinate generator
Based on the standard NACA equations for camber line and thickness distribution
"""

import numpy as np
import math

def generate_naca_4digit(naca_code, num_points=81):
    """
    Generate coordinates for a NACA 4-digit airfoil
    
    Args:
        naca_code (str): 4-digit NACA designation (e.g., "2412")
        num_points (int): Number of points to generate (default: 81)
    
    Returns:
        tuple: (x_coords, y_upper, y_lower, header_info)
    """
    if len(naca_code) != 4 or not naca_code.isdigit():
        raise ValueError("NACA code must be a 4-digit string")
    
    # Parse NACA parameters
    m = int(naca_code[0]) / 100.0  # Maximum camber as fraction of chord
    p = int(naca_code[1]) / 10.0   # Position of maximum camber as fraction of chord
    t = int(naca_code[2:4]) / 100.0  # Maximum thickness as fraction of chord
    
    # Generate x coordinates using cosine spacing for better leading edge resolution
    beta = np.linspace(0, np.pi, num_points)
    x = 0.5 * (1 - np.cos(beta))
    
    # Calculate thickness distribution (symmetric airfoil)
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    
    # Calculate camber line
    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)
    
    if m > 0 and p > 0:  # Cambered airfoil
        # Forward of maximum camber
        mask1 = x <= p
        yc[mask1] = (m / p**2) * (2 * p * x[mask1] - x[mask1]**2)
        dyc_dx[mask1] = (2 * m / p**2) * (p - x[mask1])
        
        # Aft of maximum camber
        mask2 = x > p
        yc[mask2] = (m / (1 - p)**2) * ((1 - 2*p) + 2*p*x[mask2] - x[mask2]**2)
        dyc_dx[mask2] = (2 * m / (1 - p)**2) * (p - x[mask2])
    
    # Calculate surface coordinates
    theta = np.arctan(dyc_dx)
    
    # Upper surface
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    
    # Lower surface
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)
    
    # Combine upper and lower surfaces
    # Upper surface from trailing edge to leading edge
    x_upper = xu[::-1]
    y_upper = yu[::-1]
    
    # Lower surface from leading edge to trailing edge (skip leading edge point to avoid duplication)
    x_lower = xl[1:]
    y_lower = yl[1:]
    
    # Combine coordinates
    x_coords = np.concatenate([x_upper, x_lower])
    y_coords = np.concatenate([y_upper, y_lower])
    
    # Create header information
    header_info = f"NACA {naca_code} Airfoil M={m*100:.1f}% P={p*100:.1f}% T={t*100:.1f}%"
    
    return x_coords, y_coords, header_info

def format_airfoil_txt(x_coords, y_coords, header_info, solidworks_format=False):
    """
    Format airfoil coordinates as a text string
    
    Args:
        x_coords (array): X coordinates
        y_coords (array): Y coordinates
        header_info (str): Header information
        solidworks_format (bool): If True, format for SolidWorks compatibility (no header, include Z=0)
    
    Returns:
        str: Formatted text content
    """
    lines = []
    
    if not solidworks_format:
        # Standard airfoiltools.com format with header
        lines.append(header_info)
        for x, y in zip(x_coords, y_coords):
            lines.append(f"  {x:.6f}  {y:.6f}")
    else:
        # SolidWorks format: three-column, space-delimited, no header, Z=0 for 2D airfoils
        for x, y in zip(x_coords, y_coords):
            lines.append(f"{x:.6f} {y:.6f} 0.000000")
    
    return "\n".join(lines)

def save_airfoil_txt(x_coords, y_coords, header_info, filename, solidworks_format=False):
    """
    Save airfoil coordinates to a text file
    
    Args:
        x_coords (array): X coordinates
        y_coords (array): Y coordinates
        header_info (str): Header information
        filename (str): Output filename
        solidworks_format (bool): If True, format for SolidWorks compatibility
    """
    content = format_airfoil_txt(x_coords, y_coords, header_info, solidworks_format)
    
    with open(filename, 'w') as f:
        f.write(content)

# Test the generator
if __name__ == "__main__":
    # Test with NACA 2412
    x, y, header = generate_naca_4digit("2412")
    print(f"Generated {len(x)} points for NACA 2412")
    print(f"Header: {header}")
    print(f"First few points (standard format):")
    standard_content = format_airfoil_txt(x[:5], y[:5], header, solidworks_format=False)
    print(standard_content)
    
    print(f"\nFirst few points (SolidWorks format):")
    solidworks_content = format_airfoil_txt(x[:5], y[:5], header, solidworks_format=True)
    print(solidworks_content)

