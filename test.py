from db_connector import AsyncDataBaseConnector

import asyncio


connector = AsyncDataBaseConnector(path_to_db="./test.db")


async def main():
    if await connector.add_user("test_id"):
        print("ой, с базой данных что-то пошло не так")
    # await connector.add_subject_to_user(user_id="test_id", subject="матеша")
    # await connector.add_scores_to_subject(user_id="test_id", subject="матеша", scores="345545454")

asyncio.run(main())
