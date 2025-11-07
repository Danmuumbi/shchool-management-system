# backend/check_teachers_tables.py
from utils import get_tenant_engine
from sqlalchemy import inspect

def check_tables_for_tenant(subdomain):
    """Check if teachers tables exist in tenant database"""
    try:
        engine = get_tenant_engine(subdomain)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"🔍 Checking tables for subdomain: {subdomain}")
        print(f"📊 All tables: {tables}")
        print(f"✅ Teachers table exists: {'teachers' in tables}")
        
        if 'teachers' in tables:
            # Check table structure
            columns = inspector.get_columns('teachers')
            print(f"📋 Teachers table columns:")
            for col in columns:
                print(f"   - {col['name']} ({col['type']})")
        
        return 'teachers' in tables
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

if __name__ == "__main__":
    check_tables_for_tenant("evol")