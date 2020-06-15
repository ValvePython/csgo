User Guide
**********

This part of the documentation is a quick start for writing applications that
interact with the game coordinator for CSGO.


Initialization
==============

This is the minimal code we need to get a session with the game coordnator.

.. code:: python

    from steam.client import SteamClient
    from csgo.client import CSGOClient

    client = SteamClient()
    cs = CSGOClient(client)

    @client.on('logged_on')
    def start_csgo():
        cs.launch()

    @cs.on('ready')
    def gc_ready():
        # send messages to gc
        pass

    client.cli_login()
    client.run_forever()


| You won't see any output running the code above.
| In order to peek inside we need to setup debug logging.

See the :ref:`logging_config` section

Sending/Recieving messages
==========================

Let's request profile of the currently logged on user. We only need the account id.
If need to convert from steam id or any other format see `SteamID <https://steam.readthedocs.io/en/latest/api/steam.steamid.html>`_.

.. code:: python

    from csgo.enums import ECsgoGCMsg

    # send request message
    self.send(ECsgoGCMsg.EMsgGCCStrike15_v2_ClientRequestPlayersProfile, {
                'account_id': cs.account_id,
                'request_level': 32,
             })

    # listen for the response
    response, = cs.wait_event(ECsgoGCMsg.EMsgGCCStrike15_v2_PlayersProfile, timeout=10)
    player_profle = response.account_profiles[0]

Alternatively, we can do the same using one of the methods from :any:`csgo.features`, which implements
that particular request for us. Specifically :attr:`csgo.features.player.Player.request_player_profile`

.. code:: python

    cs.request_player_profile(cs.account_id)
    response, = cs.wait_event('player_profile')

.. code:: python

    >>> str(response)
    account_id: 12345678
    ranking {
      account_id: 12345678
      rank_id: 0
      wins: 123
    }
    commendation {
      cmd_friendly: 1
      cmd_teaching: 2
      cmd_leader: 3
    }
    medals {
      medal_team: 0
      medal_combat: 0
      medal_weapon: 0
      medal_global: 0
      medal_arms: 0
    }
    player_level: 1
    player_cur_xp: 262840000

.. _working_with_events:

Working with events
===================

The module makes use of `gevent <http://www.gevent.org/>`_ 
and `gevent-eventemitter <https://github.com/rossengeorgiev/gevent-eventemitter>`_.
Events work similiarly to ``EventEmitter`` in javascript.
Nevertheless, here is quick rundown.

To catch an event we need to register a callback

.. code:: python

    @cs.on('my event')
    def do_stuff(a, b):
        print "Hey!"

    cs.on('my event', do_stuff)
    cs.once('my event', do_stuff)  # call do_stuff just one time
    cs.wait_event('my event')      # blocks and returns arguments, if any

.. note::
    ``wait_event`` may block forever, so use the ``timeout`` parameter

Emitting an event is just as simple.

.. code:: python

    cs.emit("my event")
    cs.emit("my event", 1, [3,4,5])  # optional arguments


That's it. For more details see `gevent-eventemitter <https://github.com/rossengeorgiev/gevent-eventemitter>`_.


.. _logging_config:

Configure console logging
=========================

Here is a basic configuration to get debug messages in the console.

.. code:: python

    import logging

    logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)

The we run the program and the console ouput should look something like this:

.. code::

    [2016-01-01 12:34:56,000] DEBUG CMClient: Connect initiated.
    [2016-01-01 12:34:56,000] DEBUG Connection: Attempting connection to ('208.78.164.13', 27018)
    [2016-01-01 12:34:56,000] DEBUG Connection: Connected.
    [2016-01-01 12:34:56,000] DEBUG CMClient: Emit event: 'connected'
    [2016-01-01 12:34:56,000] DEBUG SteamClient: Emit event: 'connected'
    [2016-01-01 12:34:56,000] DEBUG SteamClient: Attempting login
    [2016-01-01 12:34:56,000] DEBUG CMClient: Incoming: <Msg <EMsg.ChannelEncryptRequest: 1303>>
    [2016-01-01 12:34:56,000] DEBUG CMClient: Emit event: <EMsg.ChannelEncryptRequest: 1303>
    ...


