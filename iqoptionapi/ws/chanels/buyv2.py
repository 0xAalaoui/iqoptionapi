"""Module for IQ Option buyV2 websocket chanel."""

from iqoptionapi.ws.chanels.base import Base
from iqoptionapi.ws.chanels.base import Base
import datetime
import time
import math

class Buyv2(Base):
    """Class for IQ option buy websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "buyV2"

    def __call__(self, price, active, option, direction, duration):
        """Method to send message to buyv2 websocket chanel.
        :param price: The buying price.
        :param active: The buying active.
        :param option: The buying option.
        :param direction: The buying direction.
        """
        #current_time = self.api.timesync.server_timestamp 
        current_time = int(time.time()-1)
        nearest = duration if option == 'turbo' else 15
        
        # endpoints must be less than 5 or > 15 
        if 5 < duration < 15:
            duration = 15
            nearest = 15
        
        def round_up(tm, nearest):
            upmins = math.ceil(float(tm.minute)/nearest)*nearest
            diffmins = upmins - tm.minute
            newtime = tm + datetime.timedelta(minutes=diffmins)
            newtime = newtime.replace(second=0)
            return newtime
        
        c = datetime.datetime.fromtimestamp(current_time) 
        tm = datetime.timedelta(minutes=duration)
        requested_exp = c + tm 
        expiration_time = int(time.mktime(round_up(requested_exp, nearest).timetuple()))
        e = datetime.datetime.fromtimestamp(expiration_time)
        if (c - e).total_seconds() < 60: expiration_time += 60

        data = {
            "price": price,
            "act": active,
            "exp": expiration_time,
            "type": option,
            "direction": direction,
            "time": current_time,
        }
        self.send_websocket_request(self.name, data)
