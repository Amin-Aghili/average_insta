import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE IF NOT EXISTS instagram (
            vendor_id SERIAL PRIMARY KEY,
            insta_id VARCHAR(255) NOT NULL,
            category VARCHAR(255),
            post INTEGER NOT NULL,
            followers INTEGER NOT NULL,
            following INTEGER,
            video INTEGER DEFAULT 0,
            album INTEGER DEFAULT 0,
            photo INTEGER   DEFAULT 0,
            average_video_view INTEGER DEFAULT 0,
            average_video_like INTEGER DEFAULT 0,
            average_video_comment INTEGER DEFAULT 0,
            average_album_like INTEGER DEFAULT 0,
            average_album_comment INTEGER DEFAULT 0,
            average_photo_like INTEGER DEFAULT 0,
            average_photo_comment INTEGER DEFAULT 0,
            average_all_like INTEGER DEFAULT 0,
            average_all_comment INTEGER DEFAULT 0,
            date TIMESTAMP NOT NULL
        )
        """)
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()