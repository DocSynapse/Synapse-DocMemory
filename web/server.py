"""
DocMemory Web Interface
Simple Flask server to serve the DocMemory UI
"""
import os
import sys
# Add the parent directory to the path to import docmemory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

# Import DocMemory system
try:
    from docmemory import create_system
except ImportError:
    print("Warning: Could not import docmemory. Make sure you're running from the DocMemory directory.")
    # Provide a mock implementation for testing
    def create_system():
        class MockSystem:
            def get_document_count(self):
                return 0
            def search(self, query, search_type="hybrid", limit=10):
                return []
            def add_document_from_file(self, file_path, title=None, tags=None, custom_metadata=None):
                return ["mock_id"]
            def get_document(self, doc_id):
                return None
            def get_related_documents(self, doc_id, limit=5):
                return []
        return MockSystem()

app = Flask(__name__, static_folder='web', template_folder='web')

# Initialize DocMemory system
docmemory_system = create_system()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/status')
def get_status():
    """Get current system status"""
    return jsonify({
        'active': True,
        'document_count': docmemory_system.get_document_count(),
        'search_count': 0,  # This would be tracked in a real implementation
        'system_health': 'good'
    })

@app.route('/api/toggle', methods=['POST'])
def toggle_system():
    """Toggle system activation state"""
    data = request.get_json()
    active = data.get('active', True)
    
    # In a real implementation, you would control the system state
    return jsonify({'success': True, 'active': active})

@app.route('/api/search', methods=['POST'])
def search_documents():
    """Search documents in memory"""
    data = request.get_json()
    query = data.get('query', '')
    search_type = data.get('type', 'hybrid')
    
    # Perform search using DocMemory system
    results = docmemory_system.search(query, search_type=search_type, limit=10)
    
    # Format results
    formatted_results = []
    for result in results:
        formatted_results.append({
            'id': result['id'],
            'title': result['title'],
            'content': result['content'][:300] + '...' if len(result['content']) > 300 else result['content'],
            'score': result['score'],
            'source': result['source_file'],
            'tags': result.get('tags', []),
            'timestamp': result.get('timestamp', '')
        })
    
    return jsonify({'results': formatted_results})

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Upload a document to memory"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save file temporarily
    temp_path = f"temp_{file.filename}"
    file.save(temp_path)
    
    try:
        # Add document to DocMemory system
        doc_ids = docmemory_system.add_document_from_file(
            temp_path,
            title=file.filename,
            tags=['uploaded']
        )
        
        # Clean up temp file
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'document_ids': doc_ids,
            'count': len(doc_ids)
        })
    except Exception as e:
        # Clean up temp file even if there's an error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Get list of documents in memory"""
    # In a real implementation, this would return actual documents
    # For now, return mock data
    return jsonify({
        'documents': [
            {'id': 1, 'title': 'Research Paper', 'type': 'PDF', 'size': '2.4 MB', 'date': '2024-01-15', 'tags': ['research', 'ai']},
            {'id': 2, 'title': 'Technical Docs', 'type': 'DOCX', 'size': '1.1 MB', 'date': '2024-01-14', 'tags': ['technical', 'documentation']},
            {'id': 3, 'title': 'Project Report', 'type': 'PDF', 'size': '3.7 MB', 'date': '2024-01-13', 'tags': ['project', 'report']}
        ]
    })

if __name__ == '__main__':
    print("Starting DocMemory Web Interface...")
    print("Visit http://localhost:8000 to access the UI")
    app.run(host='0.0.0.0', port=8000, debug=True)