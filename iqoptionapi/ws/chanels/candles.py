"""Module for IQ option candles websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class GetCandles(Base):
    """Class for IQ option candles websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "candles"

    def __call__(self, active_id, duration, startTimestamp, endTimestamp, chunkSize, callback):
        """Method to send message to candles websocket chanel.

        :param active_id: The active identifier.
        :param duration: The candle duration.
        """
        data = {"active_id": active_id,
                "duration": duration,
                "chunk_size": chunkSize,
                "from": startTimestamp,
                "till": endTimestamp}
        self.api.oncandles = callback
        self.send_websocket_request(self.name, data)
