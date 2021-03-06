.. _cmdline_job_options:

Command line interface (job options)
====================================

The ``create`` and ``batch`` subcommands accept the following options to specify requested resources.

.. _cmdline_job_options_mail:

``--job-mail``/``-m <string>``
++++++++++++++++++++++++++++++

Send a mail when the cluster has started (``b`` for '*begin*'), stopped (``e`` for '*ended*') or got aborted (``a``).

For example, using ``-m a`` will result in receiving a mail whn the cluster has started running.

.. _cmdline_job_options_mail_others:

``--job-mailothers``/``-M <main addresses>``
++++++++++++++++++++++++++++++++++++++++++++

List of other mail adresses to send mails to.

.. _cmdline_job_options_name:

``--job-name``/``-N <name>``
++++++++++++++++++++++++++++

Specify the name for the job that will be submitted.

.. _cmdline_job_options_nodes:

``--job-nodes``/``-n <int>``
++++++++++++++++++++++++++++

The number of (full) workernodes to request for the job being submitted (default: 5).


.. _cmdline_job_options_ppn:

``--job-ppn <int>``
+++++++++++++++++++

The number of cores per workernode to request; by default: ``-1``, i.e. full workernodes (request all available cores).


.. _cmdline_job_options_queue:

``--job-queue``/``-q <int>``
++++++++++++++++++++++++++++

Name of job queue to submit to (default: none specified).


.. _cmdline_job_options_walltime:

``--job-walltime``/``-l <int>``
+++++++++++++++++++++++++++++++

Number of hours of walltime to request (default: 48).
