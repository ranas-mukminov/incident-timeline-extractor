from incident_timeline_extractor.parsing.nginx_parser import (
    parse_access_line,
    parse_error_line,
)

ACCESS = '192.0.2.1 - - [19/Nov/2025:08:12:01 +0000] "GET / HTTP/1.1" 502 612 "-" "curl/8.0"'
ERROR = (
    "2025/11/19 08:12:10 [error] 12345#0: *1 upstream timed out (110: Connection timed out) "
    "while connecting to upstream, client: 192.0.2.1, server: example.com, "
    'request: "GET / HTTP/1.1", upstream: "http://127.0.0.1:8080/", host: "example.com"'
)


def test_parse_access_line_sets_severity_by_status():
    parsed = parse_access_line(ACCESS)
    assert parsed is not None
    assert parsed["severity"] == "error"
    assert parsed["metadata"]["status"] == 502


def test_parse_error_line_maps_level():
    parsed = parse_error_line(ERROR)
    assert parsed is not None
    assert parsed["severity"] == "error"
    assert "upstream timed out" in parsed["message"]
