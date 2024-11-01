vcl 4.0;

import std;

backend default {
    .host = "127.0.0.1";
    .port = "10394";
}

sub vcl_recv {
    # Remove any cookies to allow caching on specific endpoints
    if (req.url ~ "^/($|api/v1/stations|api/v1/trains)") {
        unset req.http.Cookie;
    }

    # Define caching rules for specific endpoints
    if (req.url == "/") {
        set req.http.X-Cache-TTL = "31536000s"; # Cache / for 1 year
    } else if (req.url ~ "^/api/v1/stations/") {
        set req.http.X-Cache-TTL = "604800s"; # Cache /api/v1/stations/* for 1 week
    } else if (req.url ~ "^/api/v1/trains/") {
        set req.http.X-Cache-TTL = "300s"; # Cache /api/v1/trains/ for 5 minutes
    } else if (req.url ~ "^/api/v1/fares") {
        return (pass); # Don't cache /api/v1/fares
    } else {
        set req.http.X-Cache-TTL = "86400s"; # Cache everything else for 1 day
    }
}

sub vcl_backend_response {
    # Apply custom TTL from vcl_recv with duration conversion
    if (bereq.http.X-Cache-TTL) {
        set beresp.ttl = std.duration(bereq.http.X-Cache-TTL, 1s);
    }

    # Remove Server header from backend response
    unset beresp.http.Server;
}

sub vcl_deliver {
    # Set X-Cache header for HIT/MISS
    if (obj.hits > 0) {
        set resp.http.X-Cache = "HIT";
    } else {
        set resp.http.X-Cache = "MISS";
    }

    # Ensure Server header is removed in the response to the client
    unset resp.http.Server;
    unset resp.http.X-Varnish;
    unset resp.http.Via;
}