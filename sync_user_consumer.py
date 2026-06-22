#!/usr/bin/env python3
import psycopg2

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'erp.smartlifefoundation.org',
    'user': 'postgres',
    'password': 'postgres'
}

try:
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    print("Connected to database successfully")

    # Check if there are any users with consumer access in the user management
    # This would be indicated by group membership
    cur.execute("""
        SELECT DISTINCT ru.id, ru.login, rp.name, rp.id as partner_id
        FROM res_users ru
        JOIN res_partner rp ON ru.partner_id = rp.id
        JOIN res_groups_users_rel rgur ON ru.id = rgur.uid
        JOIN res_groups rg ON rgur.gid = rg.id
        WHERE rg.name::text ILIKE '%consumer%'
        AND ru.active = true;
    """)
    users = cur.fetchall()

    if users:
        print(f"\nFound {len(users)} users with consumer group access:")
        for user in users:
            print(f"  User: {user[1]} ({user[2]}) - Partner ID: {user[3]}")

            # Update their partner record to be a consumer
            cur.execute("""
                UPDATE res_partner
                SET is_consumer = true, is_volunteer = false, is_vendor = false,
                    is_corporate = false, is_company = false
                WHERE id = %s;
            """, (user[3],))

        conn.commit()
        print("Updated partner records for users with consumer access")
    else:
        print("No users found with consumer group access")

    # Also check for any partners where we know they should be consumers
    # (for example, if there are any with specific patterns in their data)

    # For now, let's just make sure our test consumer is properly set
    cur.execute("""
        SELECT id, name, is_consumer
        FROM res_partner
        WHERE is_consumer = true AND active = true;
    """)
    consumers = cur.fetchall()

    print(f"\nCurrent consumers in the system:")
    for consumer in consumers:
        print(f"  ID: {consumer[0]} | Name: {consumer[1]} | Consumer: {consumer[2]}")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
    print("Database connection closed")