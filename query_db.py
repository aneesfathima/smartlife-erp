import psycopg2
import json

def main():
    try:
        conn = psycopg2.connect(
            host='postgres-db',
            database='erp.smartlifefoundation.org',
            user='odoo',
            password='odoo'
        )
        cur = conn.cursor()
        
        # 1. Query volunteer partners and users
        print("=== PARTNERS AND USERS ===")
        cur.execute("""
            SELECT p.id, p.name, p.is_volunteer, p.is_consumer, u.id, u.login 
            FROM res_partner p 
            LEFT JOIN res_users u ON u.partner_id = p.id
            WHERE p.name ILIKE '%yasira%' OR p.name ILIKE '%priya%' OR p.name ILIKE '%admin%'
        """)
        for row in cur.fetchall():
            print(f"Partner ID: {row[0]}, Name: {row[1]}, IsVol: {row[2]}, IsStudent: {row[3]}, UserID: {row[4]}, Login: {row[5]}")
            
        # 2. Query location information
        print("\n=== CAMPS / LOCATIONS ===")
        cur.execute("""
            SELECT id, name, is_camp, address 
            FROM asset_location 
            LIMIT 10
        """)
        for row in cur.fetchall():
            print(f"Location ID: {row[0]}, Name: {row[1]}, IsCamp: {row[2]}, Address: {row[3]}")
            
        # 3. Query all projects
        print("\n=== PROJECTS ===")
        cur.execute("""
            SELECT id, name, is_public, active 
            FROM project_project
        """)
        for row in cur.fetchall():
            print(f"Project ID: {row[0]}, Name: {row[1]}, IsPublic: {row[2]}, Active: {row[3]}")

        # 4. Check relation tables for volunteers
        print("\n=== VOLUNTEERS CONFIRMED RELATION TABLES ===")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name LIKE '%project_task%res_users%' OR table_name LIKE '%project_task%volunteer%'
        """)
        tables = [r[0] for r in cur.fetchall()]
        print("Found relation tables:", tables)
        
        for table in tables:
            cur.execute(f"SELECT * FROM {table} LIMIT 10")
            print(f"Table {table} rows:", cur.fetchall())

        # 5. Query tasks
        print("\n=== TASKS ===")
        cur.execute("""
            SELECT id, name, project_id, location_id, camp_name_id, start_datetime, end_datetime, active, admin_status
            FROM project_task
            LIMIT 10
        """)
        for row in cur.fetchall():
            print(f"Task ID: {row[0]}, Name: {row[1]}, ProjectID: {row[2]}, LocID: {row[3]}, CampNameID: {row[4]}, Start: {row[5]}, End: {row[6]}, Active: {row[7]}, Status: {row[8]}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    main()
