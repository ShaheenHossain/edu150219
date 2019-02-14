# -*- coding: utf-8 -*-

from odoo import models, fields, api

class import_previous_students(models.Model):
    _name = 'dsblsc.import.previous.student'
    name=fields.Char("Name")
    date = fields.Date(default=fields.Date.today)
    import_qty = fields.Integer('No of Student to Import')
    register_id = fields.Many2one('education.admission.register', "Import student Of")
    level = fields.Integer(related='register_id.standard.id')
    import_group = fields.Char('From Group')
    import_section = fields.Char(string="section")  # ([('a','A'),('b','B'),('c','C'),('d','D')],'From Section')
    assign_class = fields.Many2one('education.class.division', "Assign Student to")
    students_to_assign = fields.One2many('education.application', 'import_id', "Student List")
    state = fields.Selection([(1, 'draft'), (2, 'done')], default='1')
    csv_file = fields.Binary(string='CSV File', required=True)

    @api.multi
    def _read_csv(self, options):
        """ Returns a CSV-parsed iterator of all non-empty lines in the file
            :throws csv.Error: if an error is detected during CSV parsing
        """
        csv_data = self.file or b''
        if not csv_data:
            return iter([])

        encoding = options.get('encoding')
        if not encoding:
            encoding = options['encoding'] = chardet.detect(csv_data)['encoding'].lower()

        if encoding != 'utf-8':
            csv_data = csv_data.decode(encoding).encode('utf-8')

        separator = options.get('separator')
        if not separator:
            # default for unspecified separator so user gets a message about
            # having to specify it
            separator = ','
            for candidate in (',', ';', '\t', ' ', '|', unicodedata.lookup('unit separator')):
                # pass through the CSV and check if all rows are the same
                # length & at least 2-wide assume it's the correct one
                it = pycompat.csv_reader(io.BytesIO(csv_data), quotechar=options['quoting'], delimiter=candidate)
                w = None
                for row in it:
                    width = len(row)
                    if w is None:
                        w = width
                    if width == 1 or width != w:
                        break # next candidate
                else: # nobreak
                    separator = options['separator'] = candidate
                    break

        csv_iterator = pycompat.csv_reader(
            io.BytesIO(csv_data),
            quotechar=options['quoting'],
            delimiter=separator)

        return (
            row for row in csv_iterator
            if any(x for x in row if x.strip())
        )
