server {
    resolver 127.0.0.1;
    listen ${LISTEN_PORT};

    location /static {
        alias /vol/static;
    }

    location / {
        resolver 127.0.0.1;
        uwsgi_pass         ${APP_HOST}:${APP_PORT};
        include            /etc/nginx/uwsgi_params;
        client_max_body_size  10M;
    }

}