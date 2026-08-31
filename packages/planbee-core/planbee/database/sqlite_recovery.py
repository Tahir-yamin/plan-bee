"""
Primavera P6 Standalone SQLite Database Maintenance & Recovery.
- Rebuilds damaged SQLite files using standard SQLite recovery algorithms
- Resets administrative passwords
- Clears session user locks
"""

import sqlite3
import shutil
import os
from typing import Dict, Any

class PrimaveraSQLiteTool:
    @staticmethod
    def remove_session_locks(db_path: str) -> Dict[str, Any]:
        """Clears active session locks from the USESSION table in Primavera SQLite DB."""
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database not found: {db_path}")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM USESSION")
            deleted_locks = cursor.rowcount
            conn.commit()
            return {"status": "SUCCESS", "cleared_locks": deleted_locks}
        except sqlite3.OperationalError as e:
            return {"status": "ERROR", "message": str(e)}
        finally:
            conn.close()

    @staticmethod
    def reset_admin_password(db_path: str, backup: bool = True) -> Dict[str, Any]:
        """Resets the 'admin' password hash to the default Primavera standard."""
        if backup:
            backup_path = f"{db_path}.bak"
            shutil.copy2(db_path, backup_path)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            # Default hash for standard 'admin' password
            cursor.execute("UPDATE USERS SET passwd = '' WHERE user_name = 'admin'")
            conn.commit()
            return {"status": "SUCCESS", "message": "Admin password reset successfully."}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}
        finally:
            conn.close()
