"""Input loaders for traces and incidents.

Supported formats:

* ``.json``  - a single object or an array of objects.
* ``.jsonl`` - one JSON object per line (blank lines ignored).

A record is routed to an :class:`Incident` when it carries an ``incident_id``
or a ``severity``/``title`` pair; otherwise it is parsed as a bare
:class:`Trace`.
"""
