"""
Bluesound API

This file implements HTML requests that can be sent to a Bluesound player

Future implementation:
Most of the API are based on this link:
https://helpdesk.bluesound.com/discussions/viewtopic.php?f=4&t=2293

-- Grouping and Ungrouping
You can group player together
http://192.168.1.38:11000/AddSlave?slave=192.168.1.41&group=Study%20Player
(Study Player is the group name)
http://192.168.1.38:11000/RemoveSlave?slave=192.168.1.41

-- Get list of services
You can get the list of Services that the player can use using
http://192.168.1.38:11000/Services
Or browse through the Radio Service using
http://192.168.1.38:11000/RadioBrowse

-- Jump to
http://192.168.1.38:11000/Playlists
http://192.168.1.38:11000/Genres?service=LocalMusic (Library)
http://192.168.1.38:11000/RadioBrowse?service=TuneIn (TuneIn Radio)

This command appears to provide a list of all the Inputs
http://192.168.1.38:11000/RadioBrowse?service=Capture

Then you can switch to them using
http://192.168.1.38:11000/Play?url=Capture%3Ahw%3A1%2C0%2F1%2F25%2F2&preset_id&image=/images/inputIcon.png (Optical Input)
http://192.168.1.38:11000/Play?url=Capture%3Abluez%3Abluetooth&preset_id&image=/images/BluetoothIcon.png (Bluetooth Input)
http://192.168.1.38:11000/Play?url=RadioParadise%3Ahttp%3A%2F%2Fstream-tx3.radioparadise.com%2Faac-320&preset_id&image=/images/ParadiseRadioIcon.png
http://192.168.1.38:11000/Play?url=Capture%3Aspotify%3Aplay&preset_id&image=/images/SpotifyIcon.png
"""
from enum import Enum
import urllib.request
import xmltodict


class RepeatOption(Enum):
    """
    Repeat option for repeat command
    """
    on = "0"
    track = "1"
    off = "2"


class BluesoundApi:
    """
    Bluesound API for sending commands and receiving status from Bluesound devices.
    """

    def __init__(self, ip_address):
        self.baseUrl = "http://" + ip_address + ":11000/"

    def play(self, id=None, url=None, seek=None):
        """
        Send Play command to Bluesound player

        Arguments:
            No arguments: Continue playing after a pause.
            id: Start playing track id + 1 (id=o, starts track 1 from playlist)
            url: Play radio station defined by url as returned by getRadioPresets()
            seek: Jumps to seek number of seconds in to current track.

        Do have some problem with Spotify
        """
        play = self.baseUrl + "Play"
        if id:
            play += ("?id=" + str(id))
        elif url:
            play += ("?url=" + str(url))
        elif seek:
            play += ("?seek=" + str(seek))

        urllib.request.urlopen(play)

    def pause(self):
        """
        Send pause command to Bluesound player
        """
        urllib.request.urlopen(self.baseUrl + "Pause")

    def skip(self):
        """
        Send skip command to Bluesound player
        Can be used to skip to next song
        """
        urllib.request.urlopen(self.baseUrl + "Skip")

    def back(self):
        """
        Send back command to Bluesound player
        Can be used to start current track at the beginning
        """
        urllib.request.urlopen(self.baseUrl + "Back")

    def volume(self, level):
        """
        Send volume command to Bluesound player

        Arguments:
            level: Volume to set in percent. 0 is mute

        Note:
            Can set limits for what 100% means, thus not with this API yet.
        """
        urllib.request.urlopen(self.baseUrl + "Volume?level=" + str(level))

    def repeat(self, state):
        """
        Send Repeat command to Bluesound player

        Arguments:
            state: Use RepeatOption enum

        Note:
            Do have some problem with Spotify
        """
        urllib.request.urlopen(self.baseUrl + "Repeat?state=" + state.value)

    def shuffle(self, shuffleOn):
        """
        Send Shuffle command to Bluesound player

        Arguments:
            shuffleOn: True shuffle on, False Shuffle off

        Note:
            Do have some problem with Spotify
        """
        urllib.request.urlopen(self.baseUrl + "Shuffle?state=" + str(int(shuffleOn)))

    def getInputs(self):
        """
        Get all input for player.

        Note:
            The radio service TuneIn and Local Music is not listed here.

        Returns:
            Dictionary radiotime. All values are string
            The result will vary from which player you have.
            {
                ('@service', 'Capture'),
                ('item',
                    {
                        ('@URL', 'RadioParadise%3Ahttp%3A%2F%2Fstream-tx3.radioparadise.com%2Faac-320'),
                        ('@image', '/images/ParadiseRadioIcon.png'),
                        ('@serviceType', 'CloudService'),
                        ('@text', 'Radio Paradise'),
                        ('@type', 'audio')
                    },
                    {
                        ('@URL', 'Capture%3Aspotify%3Aplay'),
                        ('@image', '/images/SpotifyIcon.png'),
                        ('@serviceType', 'CloudService'),
                        ('@text', 'Spotify'),
                        ('@type', 'audio')
                    },
                    {
                        ('@URL', 'Capture%3Abluez%3Abluetooth'),
                        ('@image', '/images/BluetoothIcon.png'),
                        ('@text', 'Bluetooth'),
                        ('@type', 'audio')
                    }
                )
            }
        """
        with urllib.request.urlopen(self.baseUrl + "RadioBrowse?service=Capture") as respons:
            return xmltodict.parse(respons.read())['radiotime']

    def getRadioPresets(self):
        """
        Get all Radio Presets.

        Returns:
            Dictionary radiotime. All values are string
            The result will vary from which player you have.
            {
                ('@service', 'TuneIn'),
                ('item',
                    {
                        ('@URL', 'RadioParadise%3Ahttp%3A%2F%2Fstream-tx3.radioparadise.com%2Faac-320'),
                        ('@image', '/images/ParadiseRadioIcon.png'),
                        ('@serviceType', 'CloudService'),
                        ('@text', 'Radio Paradise'),
                        ('@type', 'audio')
                    },
                    {
                        ('@URL', 'Capture%3Aspotify%3Aplay'),
                        ('@image', '/images/SpotifyIcon.png'),
                        ('@serviceType', 'CloudService'),
                        ('@text', 'Spotify'),
                        ('@type', 'audio')
                    },
                    {
                        ('@URL', 'Capture%3Abluez%3Abluetooth'),
                        ('@image', '/images/BluetoothIcon.png'),
                        ('@text', 'Bluetooth'),
                        ('@type', 'audio')
                    }
                )
            }
        """
        with urllib.request.urlopen(self.baseUrl + "RadioPresets") as respons:
            return xmltodict.parse(respons.read())['radiotime']

    def getSyncStatus(self):
        """
        Request Sync Status from Bluesound player
        Can be called every second to get player information

        Return:
            Dictionary SyncStatus. All values are string
            {
                ('@icon', '/images/players/C390DD_nt.png'),
                ('@volume', '50'),
                ('@modelName', 'C390'),
                ('@name', 'NAD C390'),
                ('@model', 'C390'),
                ('@brand', 'NAD'),
                ('@etag', '11'),
                ('@schemaVersion', '15'),
                ('@syncStat', '11'),
                ('@id', '192.168.1.8:11000'),
                ('@mac', 'xx:xx:xx:xx:xx:xx')
            }

        Raises:
            RuntimeError if it can't connect to player
        """
        with urllib.request.urlopen(self.baseUrl + "SyncStatus") as respons:
            return xmltodict.parse(respons.read())['SyncStatus']

        raise RuntimeError("Could not get SyncStatus from Bluesound device")

    def getStatus(self):
        """
        Request Status from Bluesound player
        Can be called every second to get player information

        Return:
            Dictionary status. The dict will vary depending on chosen input channel.
            This example is with TuneIn. All values is string.
            {
                ('@etag', '3b85bc61da52c3341aa12c66eddbbd91'),
                ('canMovePlayback', 'true'),
                ('canSeek', '0'),
                ('cursor', '0'),
                ('image', 'http://cdn-radiotime-logos.tunein.com/s84118q.png'),
                ('indexing', '0'),
                ('is_preset', '1'),
                ('mid', '1'),
                ('mode', '1'),
                ('pid', '1'),
                ('preset_id', 's84118'),
                ('preset_name', '103.9 | Radio Norge'),
                ('prid', '0'),
                ('quality', '128000'),
                ('repeat', '0'),
                ('service', 'TuneIn'),
                ('shuffle', '0'),
                ('sid', '5'),
                ('sleep', None),
                ('song', '0'),
                ('state', 'stream'),
                ('stationImage', 'http://cdn-radiotime-logos.tunein.com/s84118q.png'),
                ('streamFormat', 'MP3 128 kb/s'),
                ('streamUrl', 'URL to stream'),
                ('syncStat', '13'),
                ('title1', 'Variert Musikk Fra De 4 Siste Tiaar - ' 'Oslo'),
                ('title2', 'Golden Brown - The Stranglers'),
                ('title3', 'Radio Norge'),
                ('volume', '88'),
                ('secs', '5')
            }

        Raises:
            RuntimeError if it can't connect to player
        """
        with urllib.request.urlopen(self.baseUrl + "Status") as respons:
            return xmltodict.parse(respons.read())['status']

        raise RuntimeError("Could not get Status from Bluesound device")
