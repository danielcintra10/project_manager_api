
user_roles = [("P", "Project Manager"), ("D", "Developer")]


def get_role_db_value(role_display):
    match role_display:
        case "Developer":
            return "D"
        case "Project Manager":
            return "P"
