# Installation Guide

Complete installation instructions for Aethersite on different platforms.

---

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Detailed Installation Steps](#detailed-installation-steps)
- [Platform-Specific Notes](#platform-specific-notes)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)
- [Optional Dependencies](#optional-dependencies)

---

## System Requirements

### Minimum Requirements

- **OS:** Linux, macOS, or Windows 10+
- **Python:** 3.8 or higher
- **RAM:** 4 GB
- **Disk Space:** 10 GB available
- **Internet:** For downloading dependencies

### Recommended Specifications

- **Python:** 3.9 or 3.10
- **RAM:** 8 GB or more
- **Disk:** SSD for better performance
- **CPU:** Multi-core processor for faster embedding generation

---

## Quick Installation

```bash
# 1. Clone the repository
git clone https://github.com/DocSynapse/Aethersite.git
cd Aethersite

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
python -c "from docsynapse import create_system; print('Installation successful!')"
```

**That's it!** You're ready to use Aethersite.

---

## Detailed Installation Steps

### 1. Install Python

**Check if Python is installed:**
```bash
python --version
# or
python3 --version
```

**If Python is not installed:**

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-venv
```

**macOS:**
```bash
brew install python@3.9
```

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Run installer
- ✅ Check "Add Python to PATH"

### 2. Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/DocSynapse/Aethersite.git

# Or using SSH
git clone git@github.com:DocSynapse/Aethersite.git

cd Aethersite
```

### 3. Create Virtual Environment (Recommended)

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system packages
- Easy to reset if something goes wrong

**Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You'll see (venv) in your prompt
(venv) user@machine:~/docmemory$
```

**Windows (Command Prompt):**
```cmd
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies (optional, for contributors)
pip install -r requirements-dev.txt
```

**What gets installed:**
- `numpy` — numerical computations
- `faiss-cpu` — vector similarity search
- `sentence-transformers` — text embeddings
- `PyPDF2` — PDF processing
- `python-docx` — DOCX processing
- `pandas` — CSV/data processing
- `beautifulsoup4` — HTML parsing
- `Pillow` — image processing
- `pytesseract` — OCR (optional)

### 5. Download Embedding Model

**First run will download the model automatically:**

```python
from sentence_transformers import SentenceTransformer

# This downloads ~80 MB model on first run
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully!")
```

**Or download manually:**
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Platform-Specific Notes

### Linux

**Install system dependencies for PDF/image processing:**
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev
sudo apt install tesseract-ocr  # For OCR support

# Fedora/RHEL
sudo dnf install gcc python3-devel
sudo dnf install tesseract
```

### macOS

**Install via Homebrew:**
```bash
brew install tesseract  # For OCR support
```

**If you encounter SSL certificate errors:**
```bash
# Install certificates
/Applications/Python\ 3.9/Install\ Certificates.command
```

### Windows

**FAISS Installation:**

If `faiss-cpu` fails to install:
```bash
# Try conda installation
conda install -c pytorch faiss-cpu

# Or use pre-built wheel
pip install faiss-cpu --no-cache-dir
```

**Tesseract for OCR (optional):**
1. Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install
3. Add to PATH

**Long path support:**
```powershell
# Enable long path support (as Administrator)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

---

## Verifying Installation

### Basic Verification

```python
# test_installation.py
from docsynapse import create_system
import tempfile

# Create test system
test_dir = tempfile.mkdtemp()
system = create_system(storage_path=test_dir)

print("✓ System initialized")

# Create test document
with open("test.txt", "w") as f:
    f.write("This is a test document about artificial intelligence.")

# Add document
doc_ids = system.add_document_from_file(
    "test.txt",
    title="Test Document",
    tags=["test"]
)

print(f"✓ Document added: {len(doc_ids)} chunks")

# Search
results = system.search("artificial intelligence", search_type="hybrid")
print(f"✓ Search working: {len(results)} results")

# Cleanup
system.close()
print("\n✅ Installation verified successfully!")
```

Run it:
```bash
python test_installation.py
```

### Check Component Versions

```python
# check_versions.py
import sys
import numpy as np
import faiss
import sentence_transformers

print(f"Python: {sys.version}")
print(f"NumPy: {np.__version__}")
print(f"FAISS: {faiss.__version__}")
print(f"Sentence Transformers: {sentence_transformers.__version__}")
```

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'faiss'"

**Solution:**
```bash
# Try different installation method
pip install faiss-cpu --no-cache-dir

# Or use conda
conda install -c pytorch faiss-cpu
```

#### 2. "SSL: CERTIFICATE_VERIFY_FAILED"

**macOS:**
```bash
/Applications/Python\ 3.9/Install\ Certificates.command
```

**Linux/Windows:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### 3. "Failed building wheel for X"

**Linux:**
```bash
sudo apt install build-essential python3-dev
```

**macOS:**
```bash
xcode-select --install
```

**Windows:**
- Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)

#### 4. "Out of Memory" during embedding

**Reduce batch size:**
```python
# In document_processor.py, reduce chunk size
self.max_chunk_size = 500  # Instead of 1000
```

#### 5. "Permission denied" when writing files

**Linux/macOS:**
```bash
# Check permissions
ls -la docsynapse_storage/

# Fix if needed
chmod -R 755 docsynapse_storage/
```

**Windows:**
- Run terminal as Administrator
- Or choose different storage path

#### 6. Slow embedding generation

**Use GPU (if available):**
```bash
# Install CUDA-enabled PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install GPU FAISS
pip uninstall faiss-cpu
conda install -c pytorch faiss-gpu
```

### Getting Help

If you encounter issues not listed here:

1. **Check existing issues:** [GitHub Issues](https://github.com/yourusername/docmemory/issues)
2. **Search discussions:** [GitHub Discussions](https://github.com/yourusername/docmemory/discussions)
3. **Create new issue** with:
   - Full error message
   - Python version
   - OS and version
   - Steps to reproduce

---

## Optional Dependencies

### Tesseract OCR

For extracting text from images in PDFs:

**Installation:**
```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**Verify:**
```bash
tesseract --version
```

### Additional Document Formats

**For Markdown support:**
```bash
pip install markdown beautifulsoup4
```

**For LaTeX support:**
```bash
pip install pylatexenc
```

**For EPUB support:**
```bash
pip install ebooklib
```

---

## Docker Installation (Alternative)

**Coming soon!**

```bash
# Pull image
docker pull docmemory/docmemory:latest

# Run container
docker run -v $(pwd)/data:/data docmemory/docmemory
```

---

## Development Installation

For contributors who want to modify the code:

```bash
# Clone repository
git clone https://github.com/DocSynapse/Aethersite.git
cd Aethersite

# Install in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install
```

This allows you to modify code and see changes immediately without reinstalling.

---

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove directory
cd ..
rm -rf docmemory/

# Or keep code but remove dependencies
pip uninstall -r requirements.txt -y
```

---

## Next Steps

After installation:

1. **Read the Quick Start** in [README.md](./README.md)
2. **Explore examples** in `examples/` directory
3. **Check architecture** in [ARCHITECTURE.md](./ARCHITECTURE.md)
4. **Join community** in [Discussions](https://github.com/yourusername/docmemory/discussions)

---

## System-Specific Optimization

### For Large Document Collections (>10K docs)

```bash
# Install with performance optimizations
pip install faiss-cpu --no-cache-dir
pip install orjson  # Faster JSON parsing

# Consider using PostgreSQL instead of SQLite
pip install psycopg2-binary
```

### For Low-Memory Systems (<4 GB RAM)

```python
# Use smaller embedding model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L12-v2')  # Smaller variant
```

### For Offline Installation

```bash
# On online machine
pip download -r requirements.txt -d ./packages/

# Transfer to offline machine, then:
pip install --no-index --find-links=./packages/ -r requirements.txt
```

---

**Installation complete! Happy document searching! 🚀**

For questions or issues, open a [GitHub Issue](https://github.com/yourusername/docmemory/issues).
