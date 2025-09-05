# Quick Start Guide

## Fastest Way to Run the Application

1. **Run the application**:
   ```bash
   python3 run_application.py
   ```

3. **Open your browser** to `http://localhost:5000`

That's it! The script will automatically install dependencies and start the application.

## What You Can Do

### Generate NACA Airfoils
- Enter any 4-digit NACA code (e.g., 2412, 0012, 4415)
- Choose between Standard or SolidWorks format
- Download the coordinate file

### Process CSV Files
- Upload CSV files with airfoil coordinates
- Convert to SolidWorks-compatible format
- Download the converted file

### SolidWorks Import
1. Open SolidWorks
2. Create a new part
3. Go to Insert > Curve > Curve Through XYZ Points
4. Browse and select your downloaded .txt file
5. The airfoil curve will be created automatically

## File Formats

**Standard Format** (with header):
```
NACA 2412 Airfoil M=2.0% P=40.0% T=12.0%
  1.000084  0.001257
  0.998557  0.001575
  ...
```

**SolidWorks Format** (no header, 3 columns):
```
1.000084 0.001257 0.000000
0.998557 0.001575 0.000000
...
```

## Troubleshooting

- **Port 5000 in use**: Edit `airfoil-backend/src/main.py` and change the port number
- **Dependencies error**: Run `pip install flask flask-cors numpy` manually
- **Browser doesn't open**: Manually go to `http://localhost:5000`

