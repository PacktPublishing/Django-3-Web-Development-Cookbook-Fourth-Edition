# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now as tz_now


@login_required
def start_page(request):
    # dummy view to illustrate all custom template filters and tags
    obj = {
        "created": tz_now() - timedelta(days=3),
        "content": f"""
        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        <figure>
            <img src="{settings.STATIC_URL}site/img/logo.svg" alt="" />
            <figcaption>Logo</figcaption>
        </figure>
        <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</p>
        """,
        "website": "https://docs.djangoproject.com/en/dev/howto/custom-template-tags/",
        "content_to_parse": u"""
            {% if request.user.is_authenticated %}
                Hello, {{ request.user.username }}!
            {% else %}
                Hello anonymous visitor!
            {% endif %}
        """,
    }
    return render(request, "index.html", {
        "object": obj,
    })