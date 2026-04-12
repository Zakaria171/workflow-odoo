from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    promo_active = fields.Boolean(string="Promo Active", default=False)

    def _check_promotion_rights(self):
        """
        Vérifier les droits de l'utilisateur pour gérer l'état de la promotion
        """
        if not self.env.user.has_group('sale_order_control.group_sale_order_promotion_manager'):
            raise UserError("Vous n’êtes pas autorisé à modifier l’état de promotion de cette commande.")

    @api.model
    def create(self, vals):
        """
        Logique de création avec vérification des droits sur promo_active
        """
        # Vérifier s'il y a tentative d'activer promo_active à la création
        if vals.get('promo_active', False):
            self._check_promotion_rights()
        
        return super().create(vals)

    def write(self, vals):
        """
        Logique de modification avec vérification des droits et de l'état des commandes
        """
        # Vérifier si promo_active fait partie des champs modifiés (peu importe la valeur)
        if 'promo_active' in vals:
            self._check_promotion_rights()
            
            # Vérifier si au moins une commande dans le lot est en état sale ou cancel
            for record in self:
                if record.state in ['sale', 'cancel']:
                    raise UserError("Modification impossible : une ou plusieurs commandes du lot sont déjà confirmées ou annulées.")
        
        return super().write(vals)