# #
# Copyright 2009-2013 Ghent University
#
# This file is part of hanythingondemand
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/hanythingondemand
#
# hanythingondemand is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# hanythingondemand is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with hanythingondemand. If not, see <http://www.gnu.org/licenses/>.
# #
"""
@author: Ewan Higgs (University of Ghent)
"""

from vsc.utils import fancylogger
_log = fancylogger.getLogger(fname=False)

_XML_PREAMBLE = """<?xml version="1.0" encoding="utf-8"?>
"""

_HADOOP_STYLESHEET = """<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
"""

def _write_xml(outfile, options, template_resolver):
    output = _XML_PREAMBLE + _HADOOP_STYLESHEET + "<configuration>\n"

    for k, v in sorted(options.items()):
        name = template_resolver(k)
        value = template_resolver(v)
        output += """<property>
    <name>%s</name>
    <value>%s</value>
</property>
""" % (name, value)
    output += "</configuration>"
    return output

def _write_properties(outfile, options, template_resolver):
    output = ''
    for k, v in sorted(options.items()):
        output += '%s=%s\n' % (k, v)
    return output
 
def hadoop_xml(outfile, options, template_resolver):
    """Given a dict of options, write the resulting .xml or .properties file.
    Note: when dealing with .properties files, we don't use the templating
    system since things like log4j.properties have their own templating system
    and it's not reasonably sane to mix these.

    Params
    ------
    options : `dict`
    string key value pairs.

    template_resolver : `TemplateResolver`
    Resolver for template arguments.
    """
    if outfile.endswith('.xml'):
        return _write_xml(outfile, options, template_resolver)
    elif outfile.endswith('.properties'):
        return _write_properties(outfile, options, template_resolver)
    else:
        _log.error('Unrecognized hadoop file type: %s', outfile)
        raise RuntimeError('Unrecognized hadoop file type: %s' % outfile)
