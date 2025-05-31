import httpx
from fastapi import HTTPException
import asyncio
from collections import defaultdict

async def get_github_user(username):
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/users/{username}"
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")

        data = response.json()
        print(data)
        return {
            "login": data["login"],
            "name": data.get("name"),
            "public_repos": data["public_repos"],
            "followers": data["followers"]
        }
    
async def fetch_and_filter_posts():
    async with httpx.AsyncClient() as client:
        posts_res = await client.get("https://jsonplaceholder.typicode.com/posts")
        users_res = await client.get("https://jsonplaceholder.typicode.com/users")
        posts = posts_res.json()
        users = users_res.json()

        res=[]

        user_post_counts = defaultdict(int)
        for post in posts:
            user_post_counts[post["userId"]] += 1

        for user in users:
            res.append({
                "user_id":user["id"],
                "user_name":user["username"],
                "email":user["email"],
                "post_count":user_post_counts[user["id"]]
                })

        res.sort(key=lambda x: x["post_count"], reverse=True)
        return res
    
async def fetch_and_filter_albums():
    async with httpx.AsyncClient() as client:
        albums_res = await client.get("https://jsonplaceholder.typicode.com/albums")
        photos_res = await client.get("https://jsonplaceholder.typicode.com/photos")
        albums=albums_res.json()
        photos=photos_res.json()
        photos.sort(key=lambda x: x['id'])
        print(albums[0])
        print(photos[0])

        album_count = defaultdict(int)
        cover_photo = defaultdict(dict)
        for p in photos:
            album_count[p["albumId"]]+=1
            if not cover_photo[p["albumId"]]:
                cover_photo[p["albumId"]]=p

        res=[]
        for album in albums:
            res.append({
                "album_id": album["id"],
                "album_title": album["title"],
                "photo_count": album_count[album["id"]],
                "cover_photo": cover_photo[album["id"]]})
        return res
    
if __name__ == "__main__":
    #result = asyncio.run(get_github_user("yashwanth15"))
    #print(result)

    # results = asyncio.run(fetch_and_filter_posts())
    # for user in results:
    #     print(user)

    results = asyncio.run(fetch_and_filter_albums())
    for album in results:
        print(album)