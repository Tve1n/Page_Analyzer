from datetime import date

from psycopg2 import extras


def get_all_urls(conn):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cursor:
        cursor.execute("""
            SELECT
                id,
                name,
                created_at
            FROM
                urls
            ORDER BY
                id DESC;
            """)
        return cursor.fetchall()


def create_url(conn, name):
    date_create = date.today()
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cursor:
        cursor.execute("""
            INSERT INTO urls(name, created_at)
            VALUES
                (%s, %s) RETURNING id;
            """, (name, date_create))
        return cursor.fetchone()[0]


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cursor:
        cursor.execute("""
            SELECT
                id,
                name,
                created_at
            FROM
                urls
            WHERE
                id = (%s);
            """, (id,))
        return cursor.fetchone()

