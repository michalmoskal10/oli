import psycopg2.extras
import pandas as pd
import pandas.io.sql as sqlio
import os
import sql_statements
from server import db, Course, Module, Session, ModuleInfo
import config

conn_url = "dbname={} host={} port={} user={} password={}".format(config.dbname, config.host, config.port, config.user, config.password)
conn=psycopg2.connect(conn_url)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cur.execute('select * from courses where course_name= %s', ('Robotics: Aerial Robotics',))

course_id = cur.fetchone()['course_id']

course = Course(course_id=course_id, name='Robotics: Aerial Robotics')
db.session.add(course)
db.session.commit()


cur.execute('select * from course_branch_modules where course_branch_id = %s', (course_id,))
for (course_id, mod_id, ord, name, desc) in cur.fetchall():
    module = Module(module_id=mod_id, course_id=course_id, name=name, order=ord)
    db.session.add(module)
    db.session.commit()

cur.execute('select * from on_demand_sessions where course_id = %s', (course_id,))
for (course_id, session_id, start, end, _,  branch_id) in cur.fetchall():
    if db.session.query(Session).filter(Session.start_date==start).count():
        s = Session.query.filter(Session.start_date==start).order_by(Session.version.desc()).first()
        session = Session(session_id=session_id, course_id=course_id, start_date=start, end_date=end,
                          version=s.version+1, course_branch_id=branch_id)
    else:
        session = Session(session_id=session_id, course_id=course_id, start_date=start, end_date=end,
                          version=1, course_branch_id=branch_id)

    db.session.add(session)
    db.session.commit()




session = Session.query.filter(Session.session_id=='mGhKAXoWEee1jApzGcQi8A')[0]
start = session.start_date.strftime('%Y-%m-%d %H:%M:%S')
end = session.end_date.strftime('%Y-%m-%d %H:%M:%S')

cur.execute(sql_statements.users_enrolled, (session.session_id,))
session.users_enrolled = cur.fetchone()[0]

cur.execute(sql_statements.active_users_enrolled, (session.session_id, session.course_branch_id, start, end))
session.active_users_enrolled = cur.fetchone()[0]

cur.execute(sql_statements.active_users_time, (session.course_branch_id, start, end))
session.active_users_time = cur.fetchone()[0]

db.session.commit()


# This assumes that different branches of the same course have the same modules (which might not always be the case probably)
modules = Module.query.filter(Module.course_id==session.course_id).order_by(Module.order)
path = os.path.join("data_all3", session.session_id)
os.mkdir(path)
df_all = pd.DataFrame()

dfs = []
assignments_tables = []
for module in modules:
    cur.execute(sql_statements.active_users_module, (session.session_id, session.course_branch_id, module.module_id, start, end))
    moduleInfo = ModuleInfo(session_id=session.session_id, module_id=module.module_id, active_users=cur.fetchone()[0])
    db.session.add(moduleInfo)
    db.session.commit()

    df_last = sqlio.read_sql(sql_statements.last_video_seen, conn, params=(session.course_branch_id,
                    module.module_id, session.course_branch_id, module.module_id, session.start_date, session.end_date))

    df_watched = sqlio.read_sql(sql_statements.watched, conn, params=(session.course_branch_id,
                    module.module_id, session.course_branch_id, module.module_id, session.start_date, session.end_date))

    df = df_last.merge(df_watched, on='video')
    #df.to_csv(os.path.join(path, "{}.csv".format(module.module_id)), columns=["video", "last_seen", "watched"], index=False)
    dfs.append(df)

    df_assignments = sqlio.read_sql(sql_statements.last_assignment, conn, params=(session.course_branch_id,
                    module.module_id, session.course_branch_id, module.module_id, session.start_date, session.end_date))
    df_assignments.to_csv(os.path.join(path, "{}_assignments.csv".format(module.module_id)), columns=["name", "last_seen"],
              index=False)
    assignments_tables.append(df_assignments)


all = pd.concat(dfs)
sum_last_seen = all['last_seen'].sum()
sum_watched = all['watched'].sum()
for df, module in zip(dfs, modules):
    df['last_seen'] /= sum_last_seen
    df['watched'] /= sum_watched
    df.to_csv(os.path.join(path, "{}.csv".format(module.module_id)), columns=["video", "last_seen", "watched"],
              index=False)

all['last_seen'] /= sum_last_seen
all['watched'] /= sum_watched
all.to_csv(os.path.join(path, "all.csv"), columns=["video", "last_seen", "watched"], index=False)

assignments = pd.concat(assignments_tables)
assignments['ord'] = assignments.reset_index(drop=True).index
assignments.to_csv(os.path.join(path, "assignments_table.csv"), columns=["ord", "name", "last_seen"])
