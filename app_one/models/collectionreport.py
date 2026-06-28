from odoo import models, fields, tools

class CollectionReport(models.Model):
    _name = 'collection.report'
    _description = 'تقرير التحصيل'
    _auto = False  # ✅ مش هيعمل جدول — هو View فقط

    salesperson_id = fields.Many2one('res.users', string='المندوب')
    partner_id = fields.Many2one('res.partner', string='العميل')
    invoice_id = fields.Many2one('account.move', string='الفاتورة')
    invoice_date = fields.Date(string='تاريخ الفاتورة')
    amount_total = fields.Float(string='إجمالي الفاتورة')
    amount_residual = fields.Float(string='المتبقي')
    amount_collected = fields.Float(string='المحصّل')
    payment_date = fields.Date(string='تاريخ الدفعة')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW collection_report AS (
                SELECT
                    ROW_NUMBER() OVER () AS id,
                    inv.invoice_user_id     AS salesperson_id,
                    inv.partner_id          AS partner_id,
                    inv.id                  AS invoice_id,
                    inv.invoice_date        AS invoice_date,
                    inv.amount_total        AS amount_total,
                    inv.amount_residual     AS amount_residual,
                    apr.amount              AS amount_collected,
                    pay.date                AS payment_date
                FROM account_partial_reconcile apr
                JOIN account_move_line crl ON crl.id = apr.credit_move_id
                JOIN account_move pay      ON pay.id = crl.move_id
                JOIN account_move_line dbl ON dbl.id = apr.debit_move_id
                JOIN account_move inv      ON inv.id = dbl.move_id
                WHERE inv.move_type IN ('out_invoice', 'out_refund')
                  AND inv.state = 'posted'
            )
        """)