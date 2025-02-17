import json

from odoo import fields, models


class WizardCheckIntermediaryVat(models.TransientModel):
    _name = "wizard.check.intermediary"
    _description = "Intermediary VAT Check"

    line_ids = fields.One2many(
        comodel_name="wizard.check.intermediary.line", inverse_name="wizard_id"
    )
    invoice_ids = fields.Many2many(comodel_name="account.move")

    def action_confirm(self):
        for line in self.line_ids:
            data = json.loads(line.intermediary_data_json)
            if isinstance(data, str):
                data = json.loads(data)
            partner = self.env["res.partner"].create(data)
            line.invoice_id.write({"intermediary": partner.id})

        return self.action()

    def action_cancel(self):
        return self.action()

    def action(self):
        return {
            "view_type": "form",
            "name": "Electronic Bills",
            "view_mode": "tree,form",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "domain": [("id", "in", self.invoice_ids.ids)],
        }


class WizardCheckIntermediaryVatLine(models.TransientModel):
    _name = "wizard.check.intermediary.line"
    _description = "Intermediary VAT Check Line"

    invoice_id = fields.Many2one("account.move", string="Invoice", readonly=True)
    firstname = fields.Char()
    lastname = fields.Char()
    vat = fields.Char()
    intermediary_data_json = fields.Text()
    wizard_id = fields.Many2one("wizard.check.intermediary")
