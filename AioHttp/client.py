import asyncio
from aiohttp import ClientSession


async def main():
    async with ClientSession() as session:
        # response = await session.post('http://127.0.0.1:8080/test/', headers={'x-token':'secret'}, json={'param1':'js1'},
        #                              params={'qs1':'qs1'})
        # print(response.status)
        # print(await response.json())
        # response = await session.post('http://127.0.0.1:8080/users/', json={'username':'user3',
        #                                         'password' :'12Ks!vdfsd_3'})
        # print(response.status)
        # print(await response.json())
        #
        # response = await session.get('http://127.0.0.1:8080/users/')
        # print(response.status)
        # print(await response.json())
        # #
        # response = await session.patch('http://127.0.0.1:8080/users/39/', json={
        #     'name': 'new_name', 'password': '321'
        # })
        # print(response.status)
        # print(await response.json())
        #
        # response = await session.get('http://127.0.0.1:8080/users/8/')
        # print(response.status)
        # print(await response.json())

        # response = await session.delete("http://127.0.0.1:8080/users/3/")
        # print(response.status)
        # print(await response.json())
        #
        # response = await session.get("http://127.0.0.1:8080/users/3/")
        # print(response.status)
        # print(await response.json())


        # response = await session.post('http://127.0.0.1:8080/adv/', json={'title':'zasdfgg1',
        #                                         'description' :'opisan1', 'id_user': 1})
        # print(response.status)
        # print(await response.json())

        # response = await session.patch('http://127.0.0.1:8080/adv/1/', json={'title':'777zasdfgg1',
        #                                         'description' :'opisan12','id_user': 1 })
        # print(response.status)
        # print(await response.json())

        # response = await session.delete("http://127.0.0.1:8080/adv/1/")
        # print(response.status)
        # print(await response.json())

        response = await session.get("http://127.0.0.1:8080/adv/2/")
        print(response.status)
        print(await response.json())


asyncio.run(main())
