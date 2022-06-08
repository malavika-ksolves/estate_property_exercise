# -*- coding: utf-8 -*-

from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from odoo import api,fields, models

class Estate(models.Model):

    _name = "estate.model"
    _description = 'Estate Business Data'
    # _rec_name = 'property_name'

    name = fields.Char('Estate Name', required=True)
    # property_name = fields.Char('Property Name', required=True)
    description = fields.Text('Provide you requirements')
    postcode = fields.Char('Postal Code')
    date_availability = fields.Date('Available from', required=True, default=fields.Datetime.now, copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', required=True, copy=False)
    bedrooms = fields.Integer('Number of bedrooms')
    living_area = fields.Integer('Living room area')
    facades = fields.Integer('Number of facades')
    garage = fields.Boolean('Number of garage')
    garden = fields.Boolean('Number of garden')
    garden_area = fields.Integer('Area of garden')
    garden_orientation = fields.Selection(string='Orientation',selection=[('north','North'),('south','South'),('east','East'),('west','West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')], default='new', store=True, required=True, copy=False)
    property_type_id = fields.Many2one("estate.property.type.model","PropertyType")
    buyer_id = fields.Many2one("res.partner", "Buyer")
    seller_id = fields.Many2one("res.partner", "Seller")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    _sql_constraints = [('check_expected_price', 'CHECK(expected_price >= 0)','Expected price must be positive number'),
                        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive number'),
                        ]

    total = fields.Integer(
        "Total Area (sqm)",compute="_compute_total"
                                   "",help="Total area computed by summing the living area and the garden area",)
    best_price = fields.Float("Best Offer", compute="_compute_best_price", help="Best offer received")

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    @api.depends('living_area','garden_area')
    def _compute_total(self):
        for record in self:
            record.total = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                    not float_is_zero(prop.selling_price, precision_rounding=0.01)
                    and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0,
                                      precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    def unlink(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")
        return super().unlink()


    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = ""

    def property_proposal_sold(self):
        for rec in self:
            if rec.state:
                rec.state ="sold"

    def property_proposal_cancel(self):
        for rec in self:
            if rec.state:
                rec.state ="sold"
                raise ValidationError('Property is already sold cannot be cancelled')
            else:
                if rec.state == "new":
                    rec.state = "cancel"

class EstatePropertyType(models.Model):

    _name = "estate.property.type.model"
    _description = 'Estate Property Details'
    _order = "sequence, name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),]

    name = fields.Char('Property Name', required=True)
    sequence = fields.Integer("Sequence", default=10)
    property_ids = fields.One2many('estate.model', 'property_type_id',string="Properties")
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer")
    offer_ids = fields.Many2many("estate.property.offer", string="Offers", compute="_compute_offer")

    def _compute_offer(self):
        data = self.env["estate.property.offer"].read_group(
            [("property_id.state", "!=", "canceled"), ("property_type_id", "!=", False)],
            ["ids:array_agg(id)", "property_type_id"],
            ["property_type_id"],
        )
        mapped_count = {d["property_type_id"][0]: d["property_type_id_count"] for d in data}
        mapped_ids = {d["property_type_id"][0]: d["ids"] for d in data}
        for prop_type in self:
            prop_type.offer_count = mapped_count.get(prop_type.id, 0)
            prop_type.offer_ids = mapped_ids.get(prop_type.id, [])

    def action_view_offers(self):
        res = self.env.ref("estate.estate_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive")]

    price = fields.Float("Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    state = fields.Selection(selection=[("accepted", "Accepted"),("refused", "Refused")], string="Status", copy=False, default=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.model", string="Property", required=True)
    property_type_id = fields.Many2one("estate.property.type.model", related="property_id.property_type_id", string="Property Type", store=True)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days


    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env["estate.model"].browse(vals["property_id"])
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer must be higher than %.2f" % max_offer)
            prop.state = "offer_received"
        return super().create(vals)


    def action_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer as already been accepted.")
        self.write(
            {
                "state": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )


    def action_refuse(self):
        return self.write(
            {
                "state": "refused",
            }
        )

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color Index")

class ResUsers(models.Model):

    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.model", "seller_id", string="Properties", domain=[("state", "in", ["new", "offer_received"])]
    )



