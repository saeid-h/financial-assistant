"""
File Archiving Service for Financial Assistant

Archives uploaded CSV files in YYYY/MM directory structure for future reference.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


class FileArchiver:
    """
    Service to archive CSV files in organized directory structure.
    """
    
    def __init__(self, base_archive_path: str):
        """
        Initialize the file archiver.
        
        Args:
            base_archive_path: Base directory for archives (e.g., 'data/archives')
        """
        self.base_archive_path = Path(base_archive_path)
    
    def archive_file(self, file_path: str, account_id: int, original_filename: str) -> dict:
        """
        Archive a CSV file.
        
        Args:
            file_path: Path to the file to archive
            account_id: Account ID the file belongs to
            original_filename: Original name of the uploaded file
            
        Returns:
            Dictionary with keys:
                - success: Boolean indicating success
                - archive_path: Path where file was archived
                - error: Error message if failed
        """
        try:
            # Get current date for directory structure
            now = datetime.now()
            year = now.strftime('%Y')
            month = now.strftime('%m')
            timestamp = now.strftime('%Y%m%d_%H%M%S')
            
            # Create archive directory structure: base/YYYY/MM/
            archive_dir = self.base_archive_path / year / month
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename: accountID_originalname_timestamp.csv
            name, ext = os.path.splitext(original_filename)
            archive_filename = f"{account_id}_{name}_{timestamp}{ext}"
            archive_path = archive_dir / archive_filename
            
            # Copy file to archive
            shutil.copy2(file_path, archive_path)
            
            return {
                'success': True,
                'archive_path': str(archive_path),
                'archived_at': now.isoformat()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_archives(self, year: int = None, month: int = None, account_id: int = None):
        """
        List archived files with optional filtering.
        
        Args:
            year: Filter by year
            month: Filter by month (1-12)
            account_id: Filter by account ID
            
        Returns:
            List of archived file information
        """
        archives = []
        
        try:
            # Determine search path
            if year and month:
                search_path = self.base_archive_path / str(year) / f"{month:02d}"
            elif year:
                search_path = self.base_archive_path / str(year)
            else:
                search_path = self.base_archive_path
            
            if not search_path.exists():
                return archives
            
            # Find all CSV files
            for csv_file in search_path.rglob('*.csv'):
                # Parse filename to extract account_id
                filename = csv_file.name
                try:
                    file_account_id = int(filename.split('_')[0])
                except (ValueError, IndexError):
                    file_account_id = None
                
                # Filter by account_id if specified
                if account_id and file_account_id != account_id:
                    continue
                
                archives.append({
                    'filename': filename,
                    'path': str(csv_file),
                    'account_id': file_account_id,
                    'size': csv_file.stat().st_size,
                    'modified': datetime.fromtimestamp(csv_file.stat().st_mtime).isoformat()
                })
            
            # Sort by modified date (newest first)
            archives.sort(key=lambda x: x['modified'], reverse=True)
        
        except Exception as e:
            print(f"Error listing archives: {e}")
        
        return archives
    
    def get_archive(self, archive_path: str) -> str:
        """
        Get the full path to an archived file.
        
        Args:
            archive_path: Path to the archive
            
        Returns:
            Full path to the archived file, or None if not found
        """
        path = Path(archive_path)
        if path.exists() and path.is_file():
            return str(path)
        return None
    
    def delete_archive(self, archive_path: str) -> bool:
        """
        Delete an archived file.
        
        Args:
            archive_path: Path to the archive to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            path = Path(archive_path)
            if path.exists() and path.is_file():
                path.unlink()
                
                # Clean up empty directories
                try:
                    path.parent.rmdir()  # Remove month dir if empty
                    path.parent.parent.rmdir()  # Remove year dir if empty
                except OSError:
                    pass  # Directory not empty, that's fine
                
                return True
        except Exception as e:
            print(f"Error deleting archive: {e}")
        
        return False

