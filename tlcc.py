""" Tinychat LiveCountClient by Nortxort (https://github.com/nortxort) """
import json
import time
import websocket


class LiveCountClient:
    """
    A live user count class.

    Apparently tinychat sends out data containing room statistics.
    Once connected, the client receives data containing room
    statistic information every ~5 second.
    """
    def __init__(self):
        """
        Initialize the LiveCountClient class.
        """
        self.is_connected = False
        self._connection = None

    def connect(self):
        """
        Connect the client to the websocket.
        """
        error = None

        tc_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-WebSocket-Extensions': 'permessage-deflate'
        }

        # websocket.enableTrace(True)

        try:
            self._connection = websocket.create_connection(
                'wss://lb-stat.tinychat.com/leaderboard',
                header=tc_header,
                origin='https://tinychat.com'
            )
        except Exception as e:
            error = e
        finally:
            if error is not None:
                print ('Connect error: %s' % error)
            elif self._connection.connected:
                    self.is_connected = True
                    self.__callback()

    def __callback(self):
        """
        Main loop reading data from the websocket.
        """
        while self.is_connected:
            data = self._connection.next()
            json_data = json.loads(data)

            event = json_data['ev']

            if event == 'update':
                self.on_update(json_data['data'])

            else:
                print ('Unknown event: %s' % event)

    @staticmethod
    def on_update(data):
        """
        Received on `update` events.

        :param data: A list containing room statistics.
        :type data: list
        """
        ts = time.strftime('%H:%M:%S')
        print ('\n[%s] Updating %s rooms.' % (ts, len(data)))

        for i, room in enumerate(data):
            print ('(%s) Room: %s, Users: %s, Broadcasters: %s' %
                   (i, room['room'], room['users'], room['broadcasters']))
