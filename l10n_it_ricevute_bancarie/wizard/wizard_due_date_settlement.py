# Copyright (C) 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class RibaDueDateSettlement(models.TransientModel):
    _name = "riba.due.date.settlement"
    _description = "Riba Due Date Settlement"

    due_date = fields.Date()

    def due_date_settlement_confirm(self):
        active_ids = self.env.context.get("active_ids", False)
        active_model = self.env.context.get("active_model", False)
        if not active_ids:
            raise UserError(_("No active ID found."))
        elif not active_model:
            raise UserError(_("No active model found."))

        riba_ids = self.env[active_model].browse(active_ids)

        if not self.due_date:
            if active_model == "riba.distinta":
                for line in riba_ids.mapped("line_ids"):
                    if line.state == "accredited":
                        line.riba_line_settlement()
            elif active_model == "riba.distinta.line":
                for line in riba_ids:
                    if line.state == "accredited":
                        line.riba_line_settlement()
        else:
            if active_model == "riba.distinta":
                riba_lines = riba_ids.mapped("line_ids").filtered(
                    lambda rl: rl.state == "accredited" and rl.due_date == self.due_date
                )
            elif active_model == "riba.distinta.line":
                riba_lines = riba_ids.filtered(
                    lambda rl: rl.state == "accredited" and rl.due_date == self.due_date
                )
            riba_lines.riba_line_settlement()
