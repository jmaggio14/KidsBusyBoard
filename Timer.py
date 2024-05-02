import time

class Timer(object):
    """
    Timer which can be used to time processes

    Attributes:
        _start (float): start time in seconds since the epoch
        _last (float): last time the lap timer was called
        _countdown (float): countdown time if set (recalculated with
                            the countdown property)
        _last_countdown (float): last countdown time check

    Example:
        #we need to do an action for 10 seconds
        timer = Timer()
        timer.countdown = 10

        while timer.countdown:
            do_action()
            #this action will run for (about) 10 seconds


        # maybe we want to record how long a part of our code runs
        timer.reset()

        do_action()
        print( timer.lap() )

        do_action2()
        print( timer.lap() )


    """
    def __init__(self):
        self._start = time.time()
        self._last = self._start

        self._countdown_timer = None
        self._countdown_start = None


    def reset(self):
        """ resets the timer start time """
        self.__init__()

    def time(self):
        """returns the time in seconds since the timer started or since it was
         last reset"""
        return round(self.raw_time(),3)

    def raw_time(self):
        """returns the unrounded time in seconds since the timer started"""
        return time.time() - self._start

    def lap(self):
        """returns time in seconds since last time the lap was called"""
        now = time.time()
        lap = now - self._last
        self._last = now
        return round(lap,3)

    def time_ms(self):
        """returns the time in milliseonds since the timer started or since it
        was last reset"""
        return round(self.raw_time()*1000,3)

    def lap_ms(self):
        """returns time in milliseconds since last time the lap was called"""
        return round(self.lap()*1000,3)


    @property
    def countdown(self):
        if self._countdown_timer is None:
            return 0

        countdown = self._countdown_start - self._countdown_timer.raw_time()
        countdown = max(countdown,0)
        return countdown


    @countdown.setter
    def countdown(self,value):
        """sets the countdown timer"""
        if not isinstance(value,(int,float)):
            error_msg = "countdown must be set using a float \
                        or an int, current type is {0}".format(type(value))
            core.error(error_msg)
            raise TypeError(error_msg)

        self._countdown_timer = Timer()
        self._countdown_start = float(value)


    @property
    def start(self):
        return self._start


    def __str__(self):
        return "Timer @{}sec".format( self.time() )

    def __repr__(self):
        return str(self)