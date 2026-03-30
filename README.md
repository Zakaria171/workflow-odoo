# workflow_odoo

Projet Odoo Docker pour développer un module personnalisé `sale_order_control`.

Stack : Odoo 17 + PostgreSQL + Docker Compose.

Lancer : `docker compose up` puis accéder à `http://localhost:8070`.

Module custom : `sale_order_control`, qui étend `sale.order' pour activer les promotions sur une commande en ajoutant le champ promo_active
