"""Network limits for the unauthenticated local demos."""

from urllib.parse import urlsplit


def loopback_host(host):
    # Deliberately avoid DNS and wildcard aliases; localhost is pinned to IPv4.
    if host not in ('localhost', '127.0.0.1'):
        raise ValueError('Local demos only support localhost or 127.0.0.1.')
    return '127.0.0.1'


def local_authority(value, port):
    try:
        parsed = urlsplit('//' + value)
        return (parsed.hostname in ('localhost', '127.0.0.1')
                and parsed.port == port and not parsed.username
                and not parsed.password and not parsed.path
                and not parsed.query and not parsed.fragment)
    except (ValueError, TypeError):
        return False


def local_origin(value, port):
    try:
        parsed = urlsplit(value)
        return (parsed.scheme == 'http' and local_authority(parsed.netloc, port)
                and parsed.path in ('', '/') and not parsed.query
                and not parsed.fragment)
    except (ValueError, TypeError):
        return False


class LocalRequestHandler:
    """Reject DNS rebinding and cross-site form/fetch requests before dispatch."""

    def parse_request(self):
        if not super().parse_request():
            return False
        port = self.server.server_port
        if not local_authority(self.headers.get('Host', ''), port):
            self.send_error(403, 'Local Host required')
            return False
        origin = self.headers.get('Origin')
        if origin and not local_origin(origin, port):
            self.send_error(403, 'Local Origin required')
            return False
        if self.command == 'POST' and self.headers.get('Sec-Fetch-Site') == 'cross-site':
            self.send_error(403, 'Cross-site request refused')
            return False
        if self.command == 'POST':
            try:
                length = int(self.headers.get('Content-Length', ''))
                if not 0 <= length <= 65536:
                    raise ValueError
            except ValueError:
                self.send_error(413, 'Body must be at most 65536 bytes')
                return False
        return True
