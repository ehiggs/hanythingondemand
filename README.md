# HanythingOnDemand  (HOD for short)

## Goal
HanythingOnDemand is a set of scripts to start a Hadoop cluster from within
another resource management system (i.e. Torque/PBS). It allows traditional
users of HPC systems to experiment with Hadoop or use it as a production setup
if there is no deciated setup available.

## History
Hadoop used to ship it's own HOD (Hadoop On Demand) but it was non-maintained
and only supported Hadoop without tuning. (The HOD code that was shipped with
Hadoop 1.0.0 release was buggy to say the least.) An attempt was made to make
it work on UGent HPC infrastructure, but although a working Hadoop cluster was
realised, it was a nightmare to extend it's functionality.  At that point
(April 2012) HanythingOnDemand was started to be better maintainable and
support more tuning and functionality out of the box (eg HBase was minimum
requirement), hence it's name.  Apart from the acronym HOD nothing of the
Hadoop On Demand was reused.

More on the history of HOD can be found in section 2 of [this paper on Yarn
(PDF)](http://www.cs.cmu.edu/~garth/15719/papers/yarn.pdf)

## How does it work?
HanythingOnDemand works by launching an MPI job which uses the reserved nodes as a
cluster-in-a-cluster. These nodes then have the various Hadoop services started
on them. Users can launch a job at startup or login to the master node and run
attach to a screen session where they can interact with their services.

## Prerequisites
* A cluster using [Torque](http://www.adaptivecomputing.com/products/open-source/torque/).
* [environment-modules](http://modules.sourceforge.net/) (used to test HOD) to manage the environment
 * This is optional if everything is setup and usable (eg `PATH`, `JAVA_HOME`, `PYTHONPATH`)
* Python and various libraries.
 * [`mpi4py`](http://mpi4py.scipy.org/) 
  * eg on fedora `yum install -y mpi4py-mpich2`
  * If you build this yourself, you will probably need to set the MPICC envvar.
 * [`vsc-base`](https://github.com/hpcugent/vsc-base) - Used for command line parsing.
 * [`vsc-mympirun`](https://github.com/hpcugent/vsc-mympirun) - Used for setting up the MPI job.
 * [`pbs_python`](https://oss.trac.surfsara.nl/pbs_python) - Used for interacting with the PBS (aka Torque) server.
* Java 
 * Oracle JDK 
 * FC16 `java-1.6.0-openjdk-1.6.0.0-65.1.11.1.fc16.x86_64`
 * Also installable with Easybuild
* Hadoop binaries
 * e.g. the [Cloudera distribution versions](http://archive.cloudera.com/cdh4/cdh/4/) (used to test HOD)

We prefer to use [Easybuild](https://github.com/hpcugent/easybuild) for
installing all of this software on our clusters.

## Usage
### On a cluster
 Use `hod_pbs.py` for pbs support
### On localhost
 * Set the environment
  * Create a small script so that the environment is setup
  * eg FC16
   * Download [hadoop-2.0.0-cdh4.4.0.tar.gz](http://archive.cloudera.com/cdh4/cdh/4/) in `$HOME/hadoop/cdh4.4.0` and unpack.
   * Install mpi4py and java: `yum install -y mpi4py-mpich2 java-1.6.0-openjdk`
   * Install HanythingOnDemand in $HOME/hod
   * Sourcing the following script will setup the correct environment.
 
```shell
cat > $HOME/hod/localenv <<EOF

module load mpich2-x86_64
HODPATH=$HOME/hod
if [ -z $PYTHONPATH ]
then
    export PYTHONPATH=$HODPATH
else
    export PYTHONPATH=$HODPATH:$PYTHONPATH
fi
export JAVA_HOME=/usr/lib/jvm/java
export PATH=$HOME/hadoop/cdh3u3/hadoop-0.20.2-cdh3u3/bin:$HODPATH/bin/:$PATH

EOF
```
 
 * Use hod with option `--hod_envscript=$HOME/hod/localenv`
 * Use `hod_main.py`
  * don't forget the `--hod_envscript` option
