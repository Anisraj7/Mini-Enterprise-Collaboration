"""
Script to delete all SLA rule and SLA tracking data from the database
"""
from sqlalchemy import text
from app.db.database import engine


def delete_all_sla_data():
    """Delete all SLA rules and tracking data"""
    
    try:
        with engine.connect() as conn:
            # Get tracking count before delete
            tracking_result = conn.execute(
                text("SELECT COUNT(*) FROM sla_tracking")
            )
            tracking_count = tracking_result.scalar()
            print(f"Deleting {tracking_count} SLA tracking records...")
            
            # Delete all SLA tracking records first (due to foreign key constraint)
            conn.execute(text("DELETE FROM sla_tracking"))
            print(f"✓ Deleted {tracking_count} SLA tracking records")
            
            # Get rule count before delete
            rule_result = conn.execute(
                text("SELECT COUNT(*) FROM sla_rules")
            )
            rule_count = rule_result.scalar()
            print(f"Deleting {rule_count} SLA rules...")
            
            # Delete all SLA rules
            conn.execute(text("DELETE FROM sla_rules"))
            print(f"✓ Deleted {rule_count} SLA rules")
            
            # Commit all changes
            conn.commit()
            print("\n✓ All SLA data deleted successfully!")
        
    except Exception as e:
        print(f"✗ Error deleting SLA data: {e}")
        raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    delete_all_sla_data()
