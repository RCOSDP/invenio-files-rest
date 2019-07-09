# -*- coding: utf-8 -*-
#
# This file is part of WEKO3.
# Copyright (C) 2017 National Institute of Informatics.
#
# WEKO3 is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# WEKO3 is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

"""API for invenio files rest."""

from flask import current_app, render_template
from flask_babelex import gettext as _
from invenio_mail.api import send_mail
from weko_accounts.api import get_user_info_by_role_name

from .models import Location


def send_alert_mail(threshold_rate, name, use_rate, used_size, use_limit):
    """Send storage use rate alert mail."""
    try:
        # mail title
        subject = _('storage use rate over ') + str(threshold_rate) + '%'
        # recipient mail list
        users = []
        users += get_user_info_by_role_name('Repository Administrator')
        mail_list = []
        for user in users:
            mail_list.append(user.email)
        # send alert mail
        send_mail(subject, mail_list,
                  html=render_template('admin/alert_mail.html',
                                       location_name=name,
                                       use_rate=use_rate,
                                       used_size=used_size,
                                       use_limit=use_limit))
    except Exception as ex:
        current_app.logger.error(ex)
