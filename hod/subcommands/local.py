#!/usr/bin/env python
# ##
# Copyright 2009-2015 Ghent University
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
"""
Main hanythingondemand script, should be invoked in a job

@author: Ewan Higgs (Universiteit Gent)
"""

from textwrap import dedent

from hod.subcommands.subcommand import SubCommand

from vsc.utils import fancylogger
_log = fancylogger.getLogger(fname=False)

from hod.subcommands.create import CreateOptions
from hod.hodproc import ConfiguredSlave, ConfiguredMaster
from hod.mpiservice import MASTERRANK, run_tasks, setup_tasks

from mpi4py import MPI

class LocalSubCommand(SubCommand):
    '''Run hod cluster locally.'''
    CMD = "local"
    HELP = "Run the hod program locally. Generally not run from the command line"

    def run(self, args):
        options = CreateOptions(go_args=args)

        if MPI.COMM_WORLD.rank == MASTERRANK:
            _log.debug('Starting master process')
            svc = ConfiguredMaster(options)
        else:
            _log.debug('Starting slave process')
            svc = ConfiguredSlave(options)
        try:
            setup_tasks(svc)
            run_tasks(svc)
            svc.stop_service()
        except Exception, e:
            _log.error(str(e))
            _log.exception("HanythingOnDemand failed")
            return 1
