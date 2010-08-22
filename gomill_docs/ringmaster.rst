The ringmaster
==============

The ringmaster can run different kinds of competition. A competition is a
resumable processing job based on playing many GTP games. It could be:

a :dfn:`tournament`
  In a tournament, the ringmaster plays many games between a fixed set of
  players, to compare their strength.

a :dfn:`tuning event`
  In a tuning event, the ringmaster runs an algorithm for adjusting player
  parameters to find a good configuration.


Tournament files
----------------

Commands are strings. They're not run via a shell, but they're split into
arguments in a shell-like way (see :func:`shlex.split`). '~' expansion for the
current user's home directory is applied to the first element (ie, the
pathname of the executable).

.. confval:: number_of_games

  the total number of games for the tournament. If you omit this setting or
  set it to :const:`None`, the tournament will continue until explicitly
  stopped.



Usage
-----

For example::

  $ ringmaster ../tournaments/<code>.tourn

runs a competition; continues from where it left off if interrupted.

::

  $ ringmaster ../tournaments/<code>.tourn stop

tells a running competition to stop after current game(s).

::

  $ ringmaster ../tournaments/<code>.tourn show

prints a report from a competition's current status.

::

  $ ringmaster ../tournaments/<code>.tourn reset

deletes all state and output for the competition.


.. program:: ringmaster

Command-line options:

.. cmdoption:: --parallel=<N>

   use multiple processes

.. cmdoption:: --quiet

   disable printing results after each game

.. cmdoption:: --max-games=<N>

   maximum number of games to play in the run

:option:`!--max-games` is independent of any :confval:`number_of_games`
setting in the tournament file; the competition will stop if either limit is
reached.

It's ok to stop a tournament with :kbd:`Ctrl-C`; incomplete games will be
rerun from scratch on the next run.
