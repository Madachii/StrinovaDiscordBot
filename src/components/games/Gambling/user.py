from dataclasses import dataclass

@dataclass
class User:
    userID: int
    bablo: int
    basestring: int
    active_banner: str
    legendary_pulls: int
    epic_pulls: int
    rare_pulls: int
    weight_legendary: int
    weight_epic: int
    weight_rare: int
    weight_refined: int

    @staticmethod
    async def get_user_data(id, db):
        data = await db.get_user_data(id)
        data = data[0]
        if not data:
            return None

        return User(*data)