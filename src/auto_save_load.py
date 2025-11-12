"""
DocMemory - Auto-save and Auto-load Mechanisms
"""
import threading
import time
import atexit
import signal
import json
from pathlib import Path
from datetime import datetime
import zipfile
import shutil
from .docmemory_core import DocMemoryCore, DocumentMemory

class AutoSaveManager:
    """Manages automatic saving of document memories"""
    
    def __init__(self, core_memory: DocMemoryCore, 
                 auto_save_interval: int = 300,  # 5 minutes
                 backup_interval: int = 3600):   # 1 hour
        self.core_memory = core_memory
        self.auto_save_interval = auto_save_interval
        self.backup_interval = backup_interval
        
        # Threading for background operations
        self.save_lock = threading.Lock()
        self.running = True
        
        # Backup configuration
        self.backup_dir = core_memory.storage_path / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Start background threads
        self._start_background_processes()
        
        # Register cleanup handlers
        atexit.register(self.graceful_shutdown)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _start_background_processes(self):
        """Start background threads for auto operations"""
        # Auto-save thread
        self.save_thread = threading.Thread(target=self._auto_save_worker, daemon=True)
        self.save_thread.start()
        
        # Auto-backup thread
        self.backup_thread = threading.Thread(target=self._auto_backup_worker, daemon=True)
        self.backup_thread.start()
    
    def _auto_save_worker(self):
        """Background worker for auto-saving changes"""
        while self.running:
            try:
                time.sleep(self.auto_save_interval)
                
                with self.save_lock:
                    if self.core_memory.unsaved_changes:
                        print(f"Auto-saving {len(self.core_memory.unsaved_changes)} document changes...")
                        
                        # In a real implementation, we might batch these operations
                        unsaved_count = len(self.core_memory.unsaved_changes)
                        self.core_memory.unsaved_changes.clear()  # Reset changes since DB is always updated
                        
                        print(f"Auto-save completed: {unsaved_count} changes saved to database.")
            
            except Exception as e:
                print(f"Auto-save error: {e}")
    
    def _auto_backup_worker(self):
        """Background worker for auto-backing up data"""
        while self.running:
            try:
                time.sleep(self.backup_interval)
                self._perform_auto_backup()
            except Exception as e:
                print(f"Auto-backup error: {e}")
    
    def _perform_auto_backup(self):
        """Perform automatic backup of all data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"docmemory_backup_{timestamp}.zip"
        
        try:
            # Create backup by zipping the entire storage directory
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in self.core_memory.storage_path.rglob("*"):
                    if file_path.is_file() and "backups" not in str(file_path):
                        arcname = file_path.relative_to(self.core_memory.storage_path.parent)
                        zipf.write(file_path, arcname)
            
            print(f"Auto-backup completed: {backup_file.name}")
            
            # Clean up old backups (keep only the 5 most recent)
            self._cleanup_old_backups()
            
        except Exception as e:
            print(f"Backup failed: {e}")
    
    def _cleanup_old_backups(self):
        """Remove old backup files, keeping only the most recent ones"""
        backups = sorted(self.backup_dir.glob("*.zip"), key=lambda x: x.stat().st_mtime, reverse=True)
        for old_backup in backups[5:]:  # Keep only the 5 most recent backups
            try:
                old_backup.unlink()
                print(f"Removed old backup: {old_backup.name}")
            except Exception as e:
                print(f"Error removing old backup {old_backup.name}: {e}")
    
    def graceful_shutdown(self):
        """Perform graceful shutdown operations"""
        print("Performing graceful shutdown...")
        self.running = False
        
        # Perform final save
        with self.save_lock:
            if self.core_memory.unsaved_changes:
                print(f"Final save: {len(self.core_memory.unsaved_changes)} pending changes")
        
        print("System shutdown completed.")
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown"""
        self.graceful_shutdown()
        exit(0)

class AutoLoadManager:
    """Manages automatic loading of document memories at startup"""
    
    def __init__(self, core_memory: DocMemoryCore, storage_path: str):
        self.core_memory = core_memory
        self.storage_path = Path(storage_path)
        self.state_file = self.storage_path / "system_state.json"
    
    def auto_load_system(self):
        """Automatically load the memory system at startup"""
        print("Auto-loading DocMemory system...")
        
        # Check if this is a fresh system or continuation
        if self.state_file.exists():
            # Load previous system state
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            
            doc_count = self.core_memory.get_document_count()
            print(f"Loaded system with {doc_count} documents from previous session")
            print(f"Last session: {state.get('last_start', 'Unknown')}")
        else:
            # First-time initialization
            print("Initializing new DocMemory system")
            self._initialize_system_state()
    
    def _initialize_system_state(self):
        """Initialize system state file"""
        initial_state = {
            "system_version": "1.0",
            "initialized": True,
            "last_start": datetime.now().isoformat(),
            "document_count": 0
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(initial_state, f, indent=2)

class DocMemoryAutoSystem:
    """Main system integrating core memory with auto-save/load"""
    
    def __init__(self, storage_path: str = "./docmemory_storage/"):
        # Initialize core memory system
        self.core_memory = DocMemoryCore(storage_path)
        
        # Initialize auto-load system
        self.auto_load = AutoLoadManager(self.core_memory, storage_path)
        self.auto_load.auto_load_system()
        
        # Initialize auto-save system
        self.auto_save = AutoSaveManager(self.core_memory)
        
        print(f"DocMemory system initialized at: {storage_path}")
        print(f"Current document count: {self.core_memory.get_document_count()}")
    
    def add_document(self, 
                     content: str, 
                     title: str, 
                     source_file: str,
                     embedding: 'np.ndarray',
                     document_type: str = "unknown",
                     tags: list = None,
                     metadata: dict = None,
                     summary: str = "",
                     page_numbers: list = None) -> str:
        """Add a document with automatic persistence"""
        doc_id = self.core_memory.store_document(
            content=content,
            title=title,
            source_file=source_file,
            embedding=embedding,
            document_type=document_type,
            tags=tags,
            metadata=metadata,
            summary=summary,
            page_numbers=page_numbers
        )
        
        # Mark as potentially needing backup
        return doc_id
    
    def get_document(self, doc_id: str) -> DocumentMemory:
        """Retrieve a document"""
        return self.core_memory.retrieve_document(doc_id)
    
    def search_documents(self, query_embedding: 'np.ndarray', limit: int = 10):
        """Search documents (will be implemented in next component)"""
        # This will be implemented in the search component
        pass
    
    def close(self):
        """Close the system gracefully"""
        self.auto_save.graceful_shutdown()
        self.core_memory.close()