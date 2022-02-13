import schedule
import psycopg2
from time import sleep
from instagrapi import Client
from datetime import datetime
from config import config


def insert_vendor_list(vendor_list):
    # Connect to the database and insert the vendor list
    sql = "INSERT INTO instagram(insta_id,category,post,followers,following,video" \
          ",album,photo,average_video_view,average_video_like,average_video_comment,average_album_like" \
          ",average_album_comment,average_photo_like,average_photo_comment,average_all_like" \
          ",average_all_comment,date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.executemany(sql, vendor_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def info_medias():
    # login to instagram
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    # enter the number of last media you want to get
    num_last = int(input("Enter the number of last medias: "))
    cl = Client()
    cl.login(username, password)
    # open the text file to write the data(users
    with open('/home/amin/Desktop/InstAve/A/users_name.text', 'r') as users:
        users_name = users.read().splitlines()
    # get the data of the last medias
    # loop through the users and not login again

    def loop():
        try:
            list_dict = []
            for user in users_name:
                dic = dict()
                user_id = cl.user_id_from_username(user)
                medias = cl.user_medias(user_id, num_last)
                user_info = cl.user_info(user_id).dict()
                dic['user'] = user
                dic['cat'] = user_info['category_name']
                dic['post'] = user_info['media_count']
                dic['followers'] = user_info['follower_count']
                dic['following'] = user_info['following_count']

                video = 0
                photo = 0
                album = 0
                photo_like_count = 0
                photo_comment_count = 0
                video_like_count = 0
                video_comment_count = 0
                video_view_count = 0
                album_like_count = 0
                album_comment_count = 0
                for j in medias:
                    media_t = j.dict()['media_type']
                    comment_c = j.dict()['comment_count']
                    like_c = j.dict()['like_count']
                    view_c = j.dict()['view_count']
                    if media_t == 1:
                        photo_like_count += like_c
                        photo_comment_count += comment_c
                        photo += 1
                    if media_t == 2:
                        video_view_count = view_c
                        video_like_count += like_c
                        video_comment_count += comment_c
                        video += 1
                    if media_t == 8:
                        album_like_count += like_c
                        album_comment_count += comment_c
                        album += 1
                if video != 0:
                    av_video_like = video_like_count // video
                    av_video_comment = video_comment_count // video
                    av_view = video_view_count // video
                    dic['average_video_view'] = av_view
                    dic['average_video_like'] = av_video_like
                    dic['average_video_comment'] = av_video_comment
                else:
                    dic['average_video_view'] = 0
                    dic['average_video_like'] = 0
                    dic['average_video_comment'] = 0

                if photo != 0:
                    av_photo_like = photo_like_count // photo
                    av_photo_comment = photo_comment_count // photo

                    dic['average_photo_like'] = av_photo_like
                    dic['average_photo_comment'] = av_photo_comment
                else:
                    dic['average_photo_like'] = 0
                    dic['average_photo_comment'] = 0
                if album != 0:
                    av_album_like = album_like_count // album
                    av_album_comment = album_comment_count // album
                    dic['average_album_like'] = av_album_like
                    dic['average_album_comment'] = av_album_comment
                else:
                    dic['average_album_like'] = 0
                    dic['average_album_comment'] = 0
                av_all_like = (photo_like_count + video_like_count + album_like_count) // (photo + video + album)
                av_all_comment = (photo_comment_count + video_comment_count + album_comment_count) // (
                        photo + video + album)
                dic['video'] = video
                dic['photo'] = photo
                dic['album'] = album
                dic['average_all_like'] = av_all_like
                dic['average_all_comment'] = av_all_comment
                dic['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                list_dict.append(dic)

                insert_vendor_list([
                    (dic['user'],
                     dic['cat'],
                     dic['post'],
                     dic['followers'],
                     dic['following'],
                     dic['video'],
                     dic['album'],
                     dic['photo'],
                     dic['average_video_view'],
                     dic['average_video_like'],
                     dic['average_video_comment'],
                     dic['average_album_like'],
                     dic['average_album_comment'],
                     dic['average_photo_like'],
                     dic['average_photo_comment'],
                     dic['average_all_like'],
                     dic['average_all_comment'],
                     dic['date'])
                ])
        except (Exception, Client.handle_exception) as error:
            return print(error)

    # for testing
    schedule.every(2).minutes.do(loop)
    # set time for running
    # schedule.every(1).days.at("20:13").do(loop)

    while True:
        schedule.run_pending()
        sleep(20)
