from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    promo_active = fields.Boolean(string="Promo Active", default=False)
    external_id = fields.Char(string="External ID", index=True)

    def _check_promotion_rights(self):
        """
        Vérifier les droits de l'utilisateur pour gérer l'état de la promotion
        """
        if not self.env.user.has_group('sale_order_control.group_sale_order_manager'):
            raise UserError("Vous n'êtes pas autorisé à modifier l'état de promotion de cette commande.")

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
            
            if any(order.state in ['sale', 'cancel'] for order in self):
                raise UserError("Modification impossible : une ou plusieurs commandes du lot sont déjà confirmées ou annulées.")
        
        return super().write(vals)

    def unlink(self):
        """
        Bloquer la suppression des commandes non brouillon
        ou synchronisées avec un système externe.
        """
        if any(order.external_id for order in self):
            raise UserError(
                "Suppression impossible : une ou plusieurs commandes sont déjà synchronisées."
            )
        if any(order.state != 'draft' for order in self):
            raise UserError(
                "Suppression impossible : une ou plusieurs commandes ne sont pas en brouillon."
            )
        return super().unlink()