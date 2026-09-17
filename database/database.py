import os
import sqlite3
from datetime import datetime, timedelta

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home_theater.db")

def get_db_connection():
    """Establishes and returns a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes database tables for products, registered clients, and installation logs."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Products Catalog Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        image TEXT DEFAULT 'default_theater.jpg',
        specifications TEXT,
        status TEXT DEFAULT 'available', -- 'available' or 'sold'
        sold_at TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Registered Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        email TEXT,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Installation Requests Management Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS installations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        setup_type TEXT NOT NULL,
        room_size TEXT,
        address TEXT NOT NULL,
        status TEXT DEFAULT 'pending', -- 'pending' or 'completed'
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# =============================================================================
# PRODUCTS CATALOG METHODS
# =============================================================================

def get_available_products(search_query: str = None):
    """Retrieves all active systems currently available for demonstration and public sale."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if search_query and search_query.strip():
        q = f"%{search_query.strip()}%"
        cursor.execute("""
            SELECT * FROM products 
            WHERE status = 'available' 
            AND (product_name LIKE ? OR description LIKE ? OR specifications LIKE ?)
            ORDER BY id DESC
        """, (q, q, q))
    else:
        cursor.execute("SELECT * FROM products WHERE status = 'available' ORDER BY id DESC")
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_products(status_filter: str = None):
    """Administrative method to track entire store stock by status layer."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if status_filter:
        cursor.execute("SELECT * FROM products WHERE status = ? ORDER BY id DESC", (status_filter,))
    else:
        cursor.execute("SELECT * FROM products ORDER BY id DESC")
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_product_by_id(product_id: int):
    """Fetches full database metadata details for a specific equipment system ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_product(product_name: str, description: str, price: float, image: str, specifications: str):
    """Inserts a freshly refurbished audio component or theater package into the database catalog."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (product_name, description, price, image, specifications, status)
        VALUES (?, ?, ?, ?, ?, 'available')
    """, (product_name, description, price, image, specifications))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def update_product(product_id: int, product_name: str, description: str, price: float, specifications: str, image: str = None):
    """Saves updated administrative pricing or specification adjustments back to a component card."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if image:
        cursor.execute("""
            UPDATE products 
            SET product_name = ?, description = ?, price = ?, specifications = ?, image = ?
            WHERE id = ?
        """, (product_name, description, price, specifications, image, product_id))
    else:
        cursor.execute("""
            UPDATE products 
            SET product_name = ?, description = ?, price = ?, specifications = ?
            WHERE id = ?
        """, (product_name, description, price, specifications, product_id))
    conn.commit()
    conn.close()

def mark_product_as_sold(product_id: int):
    """Toggles item out of client store view and flags the precise baseline timestamp for retention sweeps."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    cursor.execute("UPDATE products SET status = 'sold', sold_at = ? WHERE id = ?", (now_str, product_id))
    conn.commit()
    conn.close()

def mark_product_as_available(product_id: int):
    """Reverts a product back into live storefront inventory and clears out historical sold metrics."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET status = 'available', sold_at = NULL WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def delete_product(product_id: int):
    """Permanently purges a system record configuration directly out of the database data layer."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# =============================================================================
# ADMIN METRICS & MAINTENANCE LIFECYCLE
# =============================================================================

def get_dashboard_stats():
    """Computes layout count aggregates for live administrative analytics cards."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    stats = {}
    cursor.execute("SELECT COUNT(*) FROM products WHERE status = 'available'")
    stats["available_count"] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products WHERE status = 'sold'")
    stats["sold_count"] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    stats["customer_count"] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM installations WHERE status = 'pending'")
    stats["pending_installations"] = cursor.fetchone()[0]
    
    conn.close()
    return stats

def cleanup_expired_sold_products():
    """Automated background optimization to sweep and clean sold products older than 48 hours (2 days)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, sold_at FROM products WHERE status = 'sold'")
    sold_items = cursor.fetchall()
    
    deleted_count = 0
    now = datetime.now()
    
    for item in sold_items:
        if item["sold_at"]:
            try:
                sold_dt = datetime.fromisoformat(item["sold_at"])
                if now - sold_dt > timedelta(days=2):
                    cursor.execute("DELETE FROM products WHERE id = ?", (item["id"],))
                    deleted_count += 1
            except ValueError:
                pass
                
    if deleted_count > 0:
        conn.commit()
    conn.close()
    return deleted_count

# =============================================================================
# REVENUE & REGISTRATION CUSTOMER PORTALS
# =============================================================================

def register_customer(name: str, phone: str, email: str, password_plain: str):
    """Inserts cryptographic records for customer registration profiles if requested."""
    from utils.helpers import hash_password
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        h = hash_password(password_plain)
        cursor.execute("""
            INSERT INTO customers (name, phone, email, password_hash)
            VALUES (?, ?, ?, ?)
        """, (name.strip(), phone.strip(), email.strip() if email else None, h))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def authenticate_customer(phone: str, password_plain: str):
    """Verifies standard customer password match queries."""
    from utils.helpers import hash_password
    conn = get_db_connection()
    cursor = conn.cursor()
    h = hash_password(password_plain)
    cursor.execute("SELECT * FROM customers WHERE phone = ? AND password_hash = ?", (phone.strip(), h))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# =============================================================================
# TECHNICAL SERVICE INSTALLATION BOOKING METHODS
# =============================================================================

def add_installation_request(customer_name: str, phone: str, setup_type: str, room_size: str, address: str):
    """Appends structural site inspection metadata parameters directly into technician assignment grids."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO installations (customer_name, phone, setup_type, room_size, address, status)
        VALUES (?, ?, ?, ?, ?, 'pending')
    """, (customer_name.strip(), phone.strip(), setup_type, room_size.strip() if room_size else None, address.strip()))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_installation_requests():
    """Retrieves all technician schedules ordered from newest entry logs down."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM installations ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_installation_status(request_id: int, new_status: str):
    """Flags active room setups as completed when sound calibrations are complete."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE installations SET status = ? WHERE id = ?", (new_status, request_id))
    conn.commit()
    conn.close()