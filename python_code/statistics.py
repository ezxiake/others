import cx_Oracle

cx = cx_Oracle.connect('jiayuan/jiayuan@192.168.1.38/orcl')
sql = cx.cursor()
print()
print()
rst1 = sql.execute('select sum(cnt)/10000 from (select count(*) as cnt from get_id_1 union all select count(*) from get_id_2 union all select count(*) from get_id_3 union all select count(*) from get_id_4)')
print('已经收集   :   ' + str(rst1.fetchone()[0]) + ' w')
rst2 = sql.execute('select sum(cnt)/10000 from (select count(*) as cnt from jy_data_1 union all select count(*) from jy_data_2 union all select count(*) from jy_data_3 union all select count(*) from jy_data_4)')
print('有记录的   :   ' + str(rst2.fetchone()[0]) + ' w')
rst3 = sql.execute("select 'get_id_1', count(id) from (select id from  get_id_1 group by id having count(*)>1) union all select 'get_id_2', count(id) from (select id from  get_id_2 group by id having count(*)>1) union all select 'get_id_3', count(id) from (select id from  get_id_3 group by id having count(*)>1) union all select 'get_id_4', count(id) from (select id from  get_id_4 group by id having count(*)>1)")
print()
print('重复情况')
for line in rst3:
    name = line[0]
    count = line[1]
    print(str(name) + '   :   ' + str(count))
print()
print()

sql.close()
cx.close()