# Mock database with a very insecure "secret" key for the Security Auditor to find
DATABASE = {
    "users": [
        {"id": 1, "username": "admin", "role": "superuser"},
        {"id": 2, "username": "guest", "role": "viewer"}
    ],
    "config": {
        "DB_ADMIN_PASS": "P@ssw0rd123!!", # HARDCODED SECRET
        "AWS_KEY": "AKIAEXAMPLE123456789" # ANOTHER SECRET
    }
}

def get_user_by_id(user_id: int):
    for user in DATABASE["users"]:
        if user["id"] == user_id:
            return user
    return None
