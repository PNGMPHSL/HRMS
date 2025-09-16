# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import frappe
from frappe.utils import add_months, get_year_ending, get_year_start, getdate

from hrms.payroll.doctype.salary_slip.test_salary_slip import make_holiday_list
from hrms.tests.utils import HRMSTestSuite

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list


class IntegrationTestHolidayListAssignment(HRMSTestSuite):
	"""
	Integration tests for HolidayListAssignment.
	Use this class for testing interactions between multiple components.
	"""

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.make_employees()

	def setUp(self):
		self.holiday_list = make_holiday_list(
			list_name="Test HLA", from_date=get_year_start(getdate()), to_date=get_year_ending(getdate())
		)

	def test_overlap_with_exisitng_assignment(self):
		create_holiday_list_assignment(employee=self.employees[0].name, holiday_list=self.holiday_list)
		from_date = add_months(get_year_start(getdate()), 6)
		to_date = add_months(get_year_start(getdate()), 12)
		self.assertRaises(
			frappe.ValidationError,
			create_holiday_list_assignment,
			employee=self.employees[0].name,
			holiday_list=self.holiday_list,
			from_date=from_date,
			to_date=to_date,
		)


def create_holiday_list_assignment(
	employee, holiday_list, company="_Test Company", do_not_submit=False, **kwargs
):
	hla = frappe.new_doc("Holiday List Assignment")
	hla.employee = (employee,)
	hla.holiday_list = (holiday_list,)
	hla.company = company
	if kwargs:
		hla.update(kwargs)
	hla.save()
	if do_not_submit:
		return hla
	hla.submit()

	return hla
