from odoo import models, fields, api, _


class DesignationMaster(models.Model):
    _name = 'designation.master'
    designation_value = fields.Char(string='Designation')


class GradeMaster(models.Model):
    _name = 'grade.master'
    grade_new = fields.Char(string='Grade')


class CadreMaster(models.Model):
    _name = 'cadre.master'
    cadre_new = fields.Char(string='Cadre')


class GradeTitleMaster(models.Model):
    _name = 'grade.title.master'
    grade_title_line = fields.Char(string='Grade Title')
