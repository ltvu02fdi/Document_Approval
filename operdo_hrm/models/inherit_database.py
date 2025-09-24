# -*- coding: utf-8 -*-
import odoo
from odoo import http
from odoo.http import request
from odoo.tools.misc import file_open
from lxml import html
from odoo.addons.base.models.ir_qweb import render as qweb_render
from odoo.addons.web.controllers.database import Database as WebDatabase, DBNAME_PATTERN

class Database(WebDatabase):
    def _render_template(self, **d):
        d.setdefault("manage", True)
        d["insecure"] = odoo.tools.config.verify_admin_password("admin")
        d["list_db"] = odoo.tools.config["list_db"]
        d["langs"] = odoo.service.db.exp_list_lang()
        d["countries"] = odoo.service.db.exp_list_countries()
        d["pattern"] = DBNAME_PATTERN
        try:
            d["databases"] = http.db_list()
            d["incompatible_databases"] = odoo.service.db.list_db_incompatible(d["databases"])
        except odoo.exceptions.AccessDenied:
            d["databases"] = [request.db] if request.db else []

        templates = {}
        # Đọc file gốc rồi thay đường dẫn logo bằng logo của module mình
        with file_open("web/static/src/public/database_manager.qweb.html", "r") as fd:
            html_str = fd.read().replace(
                '<img src="/web/static/img/logo2.png"',
                '<img id="my_db_logo" src="/operdo_hrm/static/src/img/operdo_logo.svg" style="padding-bottom: 10px; padding-top: 10px;"',
            )
            templates["database_manager"] = html_str
        with file_open("web/static/src/public/database_manager.master_input.qweb.html", "r") as fd:
            templates["master_input"] = fd.read()
        with file_open("web/static/src/public/database_manager.create_form.qweb.html", "r") as fd:
            templates["create_form"] = fd.read()

        def load(template_name):
            fromstring = html.document_fromstring if template_name == "database_manager" else html.fragment_fromstring
            return (fromstring(templates[template_name]), template_name)

        return qweb_render("database_manager", d, load)

    @http.route("/web/database/selector", type="http", auth="none")
    def selector(self, **kw):
        if request.db:
            request.env.cr.close()
        return self._render_template(manage=False)

    @http.route("/web/database/manager", type="http", auth="none")
    def manager(self, **kw):
        if request.db:
            request.env.cr.close()
        return self._render_template()
