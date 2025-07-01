from datetime import datetime, timezone
import uuid

def create_echo_breadcrumb(token):
    """Create a breadcrumb dictionary from HTTP headers."""
    return {
        "at_time": datetime.now(timezone.utc),
        "by_user": token["user_id"],
        "from_ip": "discord",  
        "correlation_id": str(uuid.uuid4())
    }
