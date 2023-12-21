from uuid import UUID


def generate_guid(number: int):
    return UUID(f"00000000-0000-0000-0000-00000000000{number}")
