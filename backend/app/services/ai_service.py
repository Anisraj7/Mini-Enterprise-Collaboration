def generate_ai_summary(tasks):
    pending = [t for t in tasks if t.status == "PENDING"]
    high_priority = [t for t in tasks if t.priority == "HIGH"]
    delayed = [t for t in tasks if t.status == "DELAYED"]

    return {
        "pending_tasks": len(pending),
        "high_priority_tasks": len(high_priority),
        "delayed_tasks": len(delayed),
        "summary": f"{len(high_priority)} high priority tasks pending"
    }