# DocMemory Web Interface

A user-friendly web interface for the DocMemory document memory system.

## Features

- **Easy Activation**: One-click activation/deactivation of DocMemory system
- **Document Search**: Advanced search with semantic, keyword, and hybrid options
- **File Upload**: Upload documents in multiple formats (PDF, DOCX, TXT, HTML, CSV)
- **Document Management**: View, organize, and manage stored documents
- **System Monitoring**: Real-time system status and statistics
- **Settings Panel**: Configure system preferences

## Requirements

- Python 3.8+
- DocMemory package
- Flask

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure DocMemory is installed:
```bash
pip install docmemory
```

## Usage

1. Start the server:
```bash
python server.py
```

2. Open your browser and go to: `http://localhost:8000`

## API Endpoints

- `GET /` - Main UI
- `GET /api/status` - Get system status
- `POST /api/toggle` - Activate/deactivate system
- `POST /api/search` - Search documents
- `POST /api/upload` - Upload documents
- `GET /api/documents` - Get document list

## Interface Guide

### Main Dashboard
- System status indicator (active/inactive)
- Document count and search statistics
- Quick access to all features

### Search Tab
- Enter queries to search in document memory
- Choose between hybrid, semantic, or keyword search
- View search results with relevance scores

### Upload Tab
- Drag and drop or browse files to upload
- Supports multiple formats: PDF, DOCX, TXT, HTML, CSV
- Track upload progress

### Memory Tab
- View all stored documents
- Filter and organize by tags
- Access individual documents

### Settings Tab
- Configure auto-backup settings
- Adjust memory thresholds
- Manage system preferences

## Troubleshooting

If you encounter issues:
1. Make sure DocMemory is properly installed
2. Check that all dependencies are installed
3. Verify that the Flask server is running on port 8000
4. Check browser console for any JavaScript errors

## License

MIT License