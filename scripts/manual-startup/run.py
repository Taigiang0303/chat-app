#!/usr/bin/env python
"""
Entry point script for the Notification Service.
This script properly sets up the Python path to ensure imports work correctly.
"""
import os
import sys
import uvicorn

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    # Run the application with the correct import path
    uvicorn.run("app.main:app", host="0.0.0.0", port=8003, reload=True) 