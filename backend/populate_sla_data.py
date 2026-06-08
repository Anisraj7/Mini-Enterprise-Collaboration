"""
Script to populate sample SLA rule and tracking data for the dashboard
"""
from datetime import datetime, timedelta
from sqlalchemy import text
from app.db.database import engine


def populate_sample_sla_data():
    """Populate sample SLA rules and tracking records"""
    
    try:
        with engine.connect() as conn:
            # Check if users exist
            user_result = conn.execute(
                text("SELECT id FROM users LIMIT 1")
            )
            user_id = user_result.scalar()
            
            if not user_id:
                print("✗ No users found in database. Please create a user first.")
                return
            
            print(f"Using user_id: {user_id}")
            
            # Insert sample SLA rules
            print("\nInserting SLA rules...")
            sla_rules_data = [
                ("Task", "High", 8),
                ("Task", "Medium", 24),
                ("Task", "Low", 72),
                ("Approval", "High", 4),
                ("Approval", "Medium", 12),
                ("Approval", "Low", 48),
            ]
            
            for module_name, priority, hours in sla_rules_data:
                conn.execute(
                    text(f"""
                    INSERT INTO sla_rules 
                    (module_name, priority, allowed_hours, escalation_enabled, is_active, created_by, created_at)
                    VALUES (:module, :priority, :hours, false, true, :user_id, NOW())
                    """),
                    {"module": module_name, "priority": priority, "hours": hours, "user_id": user_id}
                )
            
            print(f"✓ Inserted {len(sla_rules_data)} SLA rules")
            
            # Get the SLA rules we just created
            rules_result = conn.execute(
                text("SELECT id, module_name, priority, allowed_hours FROM sla_rules ORDER BY id DESC LIMIT 6")
            )
            rules = rules_result.fetchall()
            
            # Insert sample SLA tracking records
            print("\nInserting SLA tracking records...")
            now = datetime.utcnow()
            
            tracking_records = [
                # Active records
                {
                    "module_name": "Task",
                    "record_id": 1,
                    "sla_rule_id": next(r[0] for r in rules if r[1] == "Task" and r[2] == "High"),
                    "start_time": now - timedelta(hours=2),
                    "due_time": now + timedelta(hours=6),
                    "completed_time": None,
                    "status": "ACTIVE",
                    "breach_reason": None,
                },
                {
                    "module_name": "Task",
                    "record_id": 2,
                    "sla_rule_id": next(r[0] for r in rules if r[1] == "Task" and r[2] == "Medium"),
                    "start_time": now - timedelta(hours=12),
                    "due_time": now + timedelta(hours=12),
                    "completed_time": None,
                    "status": "ACTIVE",
                    "breach_reason": None,
                },
                # Breached records
                {
                    "module_name": "Task",
                    "record_id": 3,
                    "sla_rule_id": next(r[0] for r in rules if r[1] == "Task" and r[2] == "Low"),
                    "start_time": now - timedelta(hours=80),
                    "due_time": now - timedelta(hours=8),
                    "completed_time": None,
                    "status": "BREACHED",
                    "breach_reason": "Exceeded allowed time",
                },
                {
                    "module_name": "Approval",
                    "record_id": 1,
                    "sla_rule_id": next(r[0] for r in rules if r[1] == "Approval" and r[2] == "High"),
                    "start_time": now - timedelta(hours=5),
                    "due_time": now - timedelta(hours=1),
                    "completed_time": None,
                    "status": "BREACHED",
                    "breach_reason": "Pending approval too long",
                },
                # Completed within SLA
                {
                    "module_name": "Task",
                    "record_id": 4,
                    "sla_rule_id": next(r[0] for r in rules if r[1] == "Task" and r[2] == "Medium"),
                    "start_time": now - timedelta(hours=18),
                    "due_time": now + timedelta(hours=6),
                    "completed_time": now - timedelta(hours=2),
                    "status": "COMPLETED_WITHIN_SLA",
                    "breach_reason": None,
                },
                {
                    "module_name": "Approval",
                    "record_id": 2,
                    "sla_rule_id": next(r[0] for r in rules if r[1] == "Approval" and r[2] == "Medium"),
                    "start_time": now - timedelta(hours=8),
                    "due_time": now + timedelta(hours=4),
                    "completed_time": now - timedelta(hours=1),
                    "status": "COMPLETED_WITHIN_SLA",
                    "breach_reason": None,
                },
            ]
            
            for record in tracking_records:
                conn.execute(
                    text("""
                    INSERT INTO sla_tracking
                    (module_name, record_id, sla_rule_id, start_time, due_time, completed_time, status, breach_reason, created_at)
                    VALUES (:module_name, :record_id, :sla_rule_id, :start_time, :due_time, :completed_time, :status, :breach_reason, NOW())
                    """),
                    record
                )
            
            print(f"✓ Inserted {len(tracking_records)} SLA tracking records")
            
            # Commit all changes
            conn.commit()
            print("\n✓ Sample SLA data populated successfully!")
            print("\nSummary:")
            print(f"  - SLA Rules: {len(sla_rules_data)}")
            print(f"  - SLA Tracking Records: {len(tracking_records)}")
            print(f"    • Active: 2")
            print(f"    • Breached: 2")
            print(f"    • Completed within SLA: 2")
        
    except Exception as e:
        print(f"✗ Error populating SLA data: {e}")
        raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    populate_sample_sla_data()
