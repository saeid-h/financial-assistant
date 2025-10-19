"""
Category Model for database operations.
"""

import sqlite3
from typing import List, Dict, Optional


class Category:
    """Model for managing categories and category hierarchy."""
    
    def __init__(self, db_path: str):
        """
        Initialize Category model.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
    
    def get_all(self) -> List[Dict]:
        """
        Get all categories.
        
        Returns:
            List of category dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*,
                   p.name as parent_name
            FROM categories c
            LEFT JOIN categories p ON c.parent_id = p.id
            ORDER BY c.type, c.level, c.name
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_by_id(self, category_id: int) -> Optional[Dict]:
        """
        Get category by ID.
        
        Args:
            category_id: Category ID
        
        Returns:
            Category dictionary or None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*,
                   p.name as parent_name
            FROM categories c
            LEFT JOIN categories p ON c.parent_id = p.id
            WHERE c.id = ?
        """, (category_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_by_type(self, category_type: str) -> List[Dict]:
        """
        Get categories by type (income or expense).
        
        Args:
            category_type: 'income' or 'expense'
        
        Returns:
            List of category dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*,
                   p.name as parent_name
            FROM categories c
            LEFT JOIN categories p ON c.parent_id = p.id
            WHERE c.type = ?
            ORDER BY c.level, c.name
        """, (category_type,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_hierarchy(self) -> Dict:
        """
        Get categories organized as a hierarchy.
        
        Returns:
            Dictionary with 'income' and 'expense' trees
        """
        all_categories = self.get_all()
        
        # Build hierarchy
        hierarchy = {
            'income': [],
            'expense': []
        }
        
        # Create lookup dict
        cat_by_id = {cat['id']: cat for cat in all_categories}
        
        # Add children array to each category
        for cat in cat_by_id.values():
            cat['children'] = []
        
        # Build tree
        for cat in all_categories:
            if cat['parent_id'] is None:
                # Root level
                hierarchy[cat['type']].append(cat)
            else:
                # Child level
                parent = cat_by_id.get(cat['parent_id'])
                if parent:
                    parent['children'].append(cat)
        
        return hierarchy
    
    def create(self, name: str, level: int, category_type: str, 
               parent_id: Optional[int] = None) -> int:
        """
        Create a new category.
        
        Args:
            name: Category name
            level: Category level (1-3)
            category_type: 'income' or 'expense'
            parent_id: Optional parent category ID
        
        Returns:
            Category ID
        """
        # Validate
        if not name or not name.strip():
            raise ValueError("Category name is required")
        
        if category_type not in ['income', 'expense']:
            raise ValueError("Category type must be 'income' or 'expense'")
        
        if level not in [1, 2, 3]:
            raise ValueError("Category level must be 1, 2, or 3")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO categories (name, parent_id, level, type)
                VALUES (?, ?, ?, ?)
            """, (name.strip(), parent_id, level, category_type))
            
            category_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return category_id
        
        except sqlite3.IntegrityError as e:
            conn.close()
            raise ValueError(f"Category already exists: {name}")
    
    def update(self, category_id: int, name: Optional[str] = None,
               parent_id: Optional[int] = None) -> bool:
        """
        Update a category.
        
        Args:
            category_id: Category ID
            name: Optional new name
            parent_id: Optional new parent ID
        
        Returns:
            True if updated, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build update query
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name.strip())
        
        if parent_id is not None:
            updates.append("parent_id = ?")
            params.append(parent_id)
        
        if not updates:
            conn.close()
            return True
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(category_id)
        
        query = f"UPDATE categories SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated
    
    def delete(self, category_id: int) -> bool:
        """
        Delete a category.
        
        Args:
            category_id: Category ID
        
        Returns:
            True if deleted, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_full_path(self, category_id: int) -> str:
        """
        Get full category path (e.g., "Expenses → Food → Groceries").
        
        Args:
            category_id: Category ID
        
        Returns:
            Full path string
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        path = []
        current_id = category_id
        
        while current_id:
            cursor.execute("SELECT id, name, parent_id FROM categories WHERE id = ?", (current_id,))
            row = cursor.fetchone()
            
            if not row:
                break
            
            path.insert(0, row['name'])
            current_id = row['parent_id']
        
        conn.close()
        
        return ' → '.join(path) if path else 'Uncategorized'

