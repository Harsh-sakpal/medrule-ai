"""
Vercel Serverless Function Adapter for MedRule AI
Exposes the Flask WSGI instance to Vercel's Python runtime.
"""

import sys
import os

# Append the project root directory so that app, knowledge_base, and inference_engine can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Vercel looks for the WSGI application callable named `app`
if __name__ == "__main__":
    app.run()
