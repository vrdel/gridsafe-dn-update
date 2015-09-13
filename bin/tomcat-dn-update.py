#!/usr/bin/python

# Copyright (C) 2015 SRCE <daniel.vrcic@srce.hr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA


import argparse
import os
import re
import sys
import logging
import logging.handlers
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(re.sub('\n\s*', '', rough_string))
    return reparsed.toprettyxml(indent=" ")

def main():
    lfs = '%(name)s[%(process)s]: %(levelname)s %(message)s'
    lf = logging.Formatter(lfs)
    lv = logging.INFO

    logging.basicConfig(level=lv, format=lfs)
    logger = logging.getLogger(os.path.basename(sys.argv[0]))
    sh = logging.handlers.SysLogHandler('/dev/log', logging.handlers.SysLogHandler.LOG_USER)
    sh.setFormatter(lf)
    sh.setLevel(lv)
    logger.addHandler(sh)

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', dest='mapfile', nargs=1, metavar='grid-mapfile', type=str, required=True)
    parser.add_argument('-t', dest='tomcat', nargs=1, metavar='tomcat-users', type=str, required=True)
    parser.add_argument('-o', dest='output', nargs=1, metavar='tomcat-users', type=str, required=True)
    args = parser.parse_args()

    try:
        maps, mapl = set(), []
        with open(args.mapfile[0]) as f:
            for line in f:
                dn = line.split('\"', 2)[1]
                dnrev = [e for e in reversed(dn.split('/')) if e]
                mapl.append(', '.join(dnrev))
        maps = set(mapl)
    except (IOError, KeyError) as e:
        logger.error(str(e))
        raise SystemExit(1)

    try:
        tomusers, tomuserl = set(), []
        with open(args.tomcat[0]) as f:
            tree = ElementTree.parse(f)
        for node in tree.findall('user'):
            username = node.attrib.get('username')
            if username and username != 'gridsafe':
                tomuserl.append(username)
        tomusers = set(tomuserl)
    except IOError as e:
        logger.error(str(e))
        raise SystemExit(1)

    diff = maps.difference(tomusers)

    if diff:
        root = tree.getroot()
        for u in diff:
            e = Element('user')
            e.set('username', u)
            e.set('password', 'null')
            e.set('roles', 'user')
            child = root.append(e)
        try:
            with open(args.output[0], 'w') as f:
                f.write(prettify(root))
        except IOError as e:
            logger.error(str(e))
            raise SystemExit(1)

        logger.info('Updated %d DNs in tomcat-users.xml' % (len(diff)))

        raise SystemExit(0)
    else:
        raise SystemExit(1)


main()
