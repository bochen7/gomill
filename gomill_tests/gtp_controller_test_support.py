import errno
from cStringIO import StringIO

from gomill import gtp_controller
from gomill.gtp_controller import (
    GtpChannelError, GtpProtocolError, GtpTransportError, GtpChannelClosed,
    BadGtpResponse)

class Mock_writing_pipe(object):
    """Mock writeable pipe object, built on a cStringIO."""
    def __init__(self):
        self.is_broken = False
        self.sink = StringIO()

    def write(self, s):
        if self.is_broken:
            raise IOError(errno.EPIPE, "Broken pipe")
        try:
            self.sink.write(s)
        except ValueError, e:
            raise IOError(errno.EIO, str(e))

    def flush(self):
        self.sink.flush()

    def close(self):
        self.sink.close()

    def simulate_broken_pipe(self):
        self.is_broken = True

    def getvalue(self):
        return self.sink.getvalue()


class Preprogrammed_gtp_channel(gtp_controller.Subprocess_gtp_channel):
    """A Linebased_gtp_channel with preprogrammed response stream.

    Instantiate with a string containing the complete response stream.

    This will send the contents of the response stream, irrespective of what
    commands are received.

    The command stream is available from get_command_stream().

    """
    def __init__(self, response):
        gtp_controller.Linebased_gtp_channel.__init__(self)
        self.command_pipe = Mock_writing_pipe()
        self.response_pipe = StringIO(response)
        #raise GtpChannelError(s)

    def close(self):
        self.command_pipe.close()
        self.response_pipe.close()
        #self.resource_usage = rusage
        #raise GtpTransportError("\n".join(errors))

    def get_command_stream(self):
        """Return the complete contents of the command stream sent so far."""
        return self.command_pipe.getvalue()

    def break_command_stream(self):
        """Break the simulated pipe for the command stream."""
        self.command_pipe.simulate_broken_pipe()

    def close_response_stream(self):
        """Forcibly close the response stream."""
        self.response_pipe.close()
