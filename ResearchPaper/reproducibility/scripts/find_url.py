import sqlite3, os, glob

paths = glob.glob(os.path.expanduser('~\\AppData\\Local\\*\\*\\User Data\\Default\\History'))
paths += glob.glob(os.path.expanduser('~\\AppData\\Local\\*\\User Data\\Default\\History'))

for p in paths:
    try:
        conn = sqlite3.connect(f'file:{p}?mode=ro', uri=True)
        cur = conn.cursor()
        cur.execute("SELECT target_path, tab_url FROM downloads WHERE target_path LIKE '%cwwc%'")
        for r in cur.fetchall():
            print("Found download:", r)
    except Exception as e:
        pass
