# -*- coding:utf-8 -*-
from flask import current_app
from flask import render_template
from flask import request
from flask import url_for as _url_for

__all__ = ['tmpl']


def tmpl(*name_or_list, **context):
    if name_or_list:
        name_or_list = name_or_list[0]
    else:
        path_list = request.endpoint.split('.')
        name_or_list = [
            '/'.join(path_list[x:]) + '.html' for x in range(len(path_list))
            ]
    return render_template(name_or_list, **context)


def url_for(endpoint, app=None, **values):
    if app is None:
        return _url_for(endpoint, **values)
    else:
        status, url = current_app.config['OTHERS_MAPS'][app][endpoint] \
            .build(values)
        return current_app.config['APP_HOSTS'][app]+url