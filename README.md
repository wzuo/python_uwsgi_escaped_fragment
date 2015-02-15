# python_uwsgi_escaped_fragment
Python UWSGI script that handles _escaped_fragment_ rendering for Google Bot

## Required libraries
For Python they are listed in requirements.txt file. Selenium needs PhantomJS to work. You can install it via `npm install -g phantomjs` (it requires node.js & npm)

## Run script for UWSGI
```
uwsgi --socket socket.sock --chdir /path/to/sock --wsgi-file application.py
```

## Configuration for NGINX
```
upstream python_escaped_fragment {
    server unix:///path/to/sock/socket.sock;
}

server {
    listen 80;
    server_name my_virtualhost.localhost;
        
    # Passing escaped fragment URLs into other python script
    if ( $args ~ _escaped_fragment_ ) {
        rewrite ^(.*)$ /python-escaped-fragment/$scheme://$host:$server_port$uri last;
    }

    location ^~ /python-escaped-fragment {
        uwsgi_pass python_escaped_fragment;

        uwsgi_param  QUERY_STRING       $query_string;
        uwsgi_param  REQUEST_METHOD     $request_method;
        uwsgi_param  CONTENT_TYPE       $content_type;
        uwsgi_param  CONTENT_LENGTH     $content_length;

        uwsgi_param  REQUEST_URI        $request_uri;
        uwsgi_param  PATH_INFO          $document_uri;
        uwsgi_param  DOCUMENT_ROOT      $document_root;
        uwsgi_param  SERVER_PROTOCOL    $server_protocol;
        uwsgi_param  HTTPS              $https if_not_empty;

        uwsgi_param  REMOTE_ADDR        $remote_addr;
        uwsgi_param  REMOTE_PORT        $remote_port;
        uwsgi_param  SERVER_PORT        $server_port;
        uwsgi_param  SERVER_NAME        $server_name;
    }
}
```

#### 502 Bad gateway error
Check the path & permissions of socket (they should be 777 with executable)

### DELETE_FRAGMENT_SCRIPT
This is script executed after DOMReady event.

### Docs
If you still have problems with uWSGI configuration, please visit: http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html