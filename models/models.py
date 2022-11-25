# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError, ValidationError


class Pegawai(models.Model):
    _name = 'hrpm.pegawai'
    _description = 'Pegawai'


    name = fields.Char(string="Nama")
    rate_gaji = fields.Integer(string='Rate Gaji (/jam)', required=True)
    role = fields.Selection([('runner', 'Runner'), ('server', 'Server'), ('kitchen','Kitchen'), ('rm', 'Restaurant Manager'), ('arm','Asisstant Restaurant Manager'), ('captain', 'Captain'), ('spv', 'Supervisor')], string='Role', required=True)

class Shift(models.Model):
    _name = 'hrpm.shift'
    _description = 'Shift'
    _rec_name = 'sesi'


    sesi = fields.Selection([('pagi', 'Pagi'), ('sore', 'Sore')], string='Sesi Shift', required=True)
    tanggal = fields.Date(string="Tanggal", required=True)
    kebutuhan = fields.Many2many('hrpm.kebutuhan',string='Kebutuhan')
    pengisi = fields.Many2many('hrpm.pegawai',string='Pengisi')
    status = fields.Selection([('terpenuhi', 'Terpenuhi'), ('belum', 'Belum Terpenuhi')], string='Status',default='belum')
    is_duplicate = fields.Boolean(string='Duplicate?', default=False)
    tanggal_akhir = fields.Date(string="Sampai")

    @api.onchange('pengisi','kebutuhan')	
    def _status_control(self):
        self.write({'status': self.update_status()})

    def generate_duplicate(self):
        for rec in self:
            if rec.is_duplicate:
                if rec.tanggal and rec.tanggal_akhir:
                    range_date = rec.calc_dates(
                        rec.tanggal, rec.tanggal_akhir)
                    if range_date is None:
                        raise ValidationError("Something went wrong")
                    else:
                        for day in range_date:
                            val = {
                                'sesi': rec.sesi,
                                'tanggal': day,
                                'tanggal_akhir': rec.tanggal_akhir,
                                'kebutuhan': [(6, 0, rec.kebutuhan.ids)],
                                'pengisi': [(6, 0, rec.pengisi.ids)],
                                'status': rec.status,
                                'is_duplicate': True
        }
                            self.create(val)
                            self._cr.commit()

    def calc_dates(self, date1, date2):
        date_from = date1
        date_to = date2

        delta = date_to - date_from

        if delta.days < 0:
            return None

        dates = []

        for n in range(delta.days + 1):
            dates.append(date_from + timedelta(days=n))

        return dates 
    
    def update_status(self):
        for rec in self:
            list_kebutuhan = {}
            for kebutuhan in rec.kebutuhan:
                role = kebutuhan.role
                jumlah = kebutuhan.jumlah
                if not role in list_kebutuhan.keys():
                    list_kebutuhan[role] = 0
                list_kebutuhan[role] += jumlah

            for pengisi in rec.pengisi:
                role = pengisi.role
                if role in list_kebutuhan.keys():
                    list_kebutuhan[role] -= 1

            status = 'terpenuhi'
            for key, value in list_kebutuhan.items():
                if value != 0:
                    status = 'belum'
                    break
            return status


class Kebutuhan(models.Model):
    _name = 'hrpm.kebutuhan'
    _description = 'Kebutuhan'


    role = fields.Selection([('runner', 'Runner'), ('server', 'Server'), ('kitchen','Kitchen'), ('rm', 'Restaurant Manager'), ('arm','Asisstant Restaurant Manager'), ('captain', 'Captain'), ('spv', 'Supervisor')], string='Role', required=True)
    jumlah = fields.Integer(string="Jumlah", required=True)

    



