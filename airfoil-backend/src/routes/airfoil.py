from flask import Blueprint, request, jsonify
import tempfile
import os
from src.naca_generator import generate_naca_4digit, format_airfoil_txt
from src.csv_processor import parse_airfoil_csv, process_coordinates_for_output

airfoil_bp = Blueprint('airfoil', __name__)

@airfoil_bp.route('/generate-naca', methods=['POST'])
def generate_naca():
    """Generate NACA airfoil coordinates"""
    try:
        data = request.get_json()
        naca_code = data.get('naca_code', '2412')
        solidworks_format = data.get('solidworks_format', False)
        
        # Validate NACA code
        if not naca_code or len(naca_code) != 4 or not naca_code.isdigit():
            return jsonify({'error': 'Invalid NACA code. Must be 4 digits.'}), 400
        
        # Generate coordinates
        x_coords, y_coords, header_info = generate_naca_4digit(naca_code)
        
        # Format coordinates
        coordinates_text = format_airfoil_txt(x_coords, y_coords, header_info, solidworks_format)
        
        return jsonify({
            'coordinates': coordinates_text,
            'name': f'NACA {naca_code}',
            'format': 'solidworks' if solidworks_format else 'standard',
            'point_count': len(x_coords)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@airfoil_bp.route('/process-csv', methods=['POST'])
def process_csv():
    """Process uploaded CSV file and convert to coordinates"""
    try:
        if 'csv_file' not in request.files:
            return jsonify({'error': 'No CSV file uploaded'}), 400
        
        file = request.files['csv_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        solidworks_format = request.form.get('solidworks_format', 'false').lower() == 'true'
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.csv', delete=False) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Parse CSV data
            x_coords, y_coords, airfoil_name, metadata = parse_airfoil_csv(temp_path)
            
            # Process coordinates for output
            x_processed, y_processed = process_coordinates_for_output(x_coords, y_coords)
            
            # Format coordinates
            if solidworks_format:
                lines = []
                for x, y in zip(x_processed, y_processed):
                    lines.append(f"{x:.6f} {y:.6f} 0.000000")
                coordinates_text = "\n".join(lines)
            else:
                lines = [airfoil_name]
                for x, y in zip(x_processed, y_processed):
                    lines.append(f"  {x:.6f}  {y:.6f}")
                coordinates_text = "\n".join(lines)
            
            return jsonify({
                'coordinates': coordinates_text,
                'name': airfoil_name,
                'format': 'solidworks' if solidworks_format else 'standard',
                'point_count': len(x_processed),
                'metadata': metadata
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@airfoil_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'airfoil-generator'})

