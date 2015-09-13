from distutils.core import setup

NAME='gridsafe-dn-update'

def get_ver():
    try:
        for line in open(NAME+'.spec'):
            if "Version:" in line:
                return line.split()[1]
    except IOError:
        print "Make sure that %s is in directory"  % (NAME+'.spec')
        raise SystemExit(1)

setup(name=NAME,
    version=get_ver(),
    description='Package provides simple script that synchronizes GridSAFE WebAcct\'s tomcat-users.xml cert DNs with ones found in Globus gridmap file.',
    author='SRCE',
    author_email='daniel.vrcic@srce.hr',
    license='GPL',
    long_description=''' ''',
    scripts = ['bin/tomcat-dn-update.py'],
    data_files = [
        ('/etc/cron.d/', ['cronjobs/tomcat-dn-update']),
    ]
)
