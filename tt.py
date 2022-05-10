from pybase import databaseOperator

host = '127.0.0.1'
user = 'ks1'
psd = '1sk'
db = 'KS1'
a = databaseOperator.sqlOperator(host, user, psd, db)
a.active()

ww = {'length': 4, 'area': 5, 'JBnum': 2, 'GZnum': 1, 'FeelerNum': 4}

a.add_sys01('123', ww)
