import pymysql

pymysql.version_info = (2, 2, 1, "final", 0)  # This "tricks" Django into thinking the version is new enough
pymysql.install_as_MySQLdb()