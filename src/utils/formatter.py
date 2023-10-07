def format_user_name(user_model):
    formatted_name = f"{user_model.last_name} {user_model.name[0]}."
    if user_model.patronymic:
        formatted_name += f" {user_model.patronymic[0]}."
    return formatted_name


def get_fullname(user_model):
    formatted_name = f"{user_model.last_name} {user_model.name} {user_model.patronymic}"
    return formatted_name
