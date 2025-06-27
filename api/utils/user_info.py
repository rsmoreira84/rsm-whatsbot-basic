def build_user_info_message(user):
    message = "*User Info*\n" \
              "Name: "

    if "name" in user:
        message += user["name"]
    else:
        message += "Not set"

    message += "\nPhone: "
    if "number" in user:
        message += user["number"]
    else:
        message += "Not set"

    message += "\nEmail: "
    if "email" in user:
        message += user["email"]
    else:
        message += "Not set"

    return message
