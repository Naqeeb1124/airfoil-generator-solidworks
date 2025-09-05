---
layout: default
categories: [Web Development, Aerospace, CAD, Python]
title: "Web-Based Airfoil Coordinate Generator"
description: "A web application that generates and converts NACA airfoil coordinates for CAD applications. Users can generate coordinates for any 4-digit NACA airfoil or convert existing coordinate files into a SolidWorks-compatible format."
files:
  - name: "Run Application"
    path: "run_application.py"
  - name: "Quick Start Guide"
    path: "QUICK_START.md"
  - name: "Backend Source"
    path: "airfoil-backend/"
  - name: "Frontend Source"
    path: "airfoil-generator/"
---

<a href="YOUR_DEPLOYED_APP_URL_HERE" class="btn btn-primary" target="_blank">Live Demo</a>

## Project Overview

This project is a web-based tool for generating and processing airfoil coordinate files. It provides a simple interface for aerospace engineers and students to create NACA airfoil geometries for use in CAD software like SolidWorks.

The application has two main features:
*   **NACA Airfoil Generation:** Users can input any 4-digit NACA series code (e.g., 2412) and the application will generate the corresponding x, y coordinates.
*   **Coordinate File Conversion:** Users can upload a CSV file with airfoil coordinates and the application will convert it to a format suitable for import into SolidWorks (a 3-column XYZ format).

The backend is built with Python and Flask, and the frontend is a modern web interface.

## Running the Application

To run the airfoil coordinate generator locally:

1.  **Navigate to the project directory:**
    ```bash
    cd _projects/16-airfoil-coord-generator-xyz
    ```
2.  **Run the application script:**
    ```bash
    python run_application.py
    ```
    The script will guide you through installing any necessary dependencies.

3.  **Open your web browser** to [http://localhost:5000](http://localhost:5000) to use the application.

For more detailed instructions, please see the `QUICK_START.md` file.
