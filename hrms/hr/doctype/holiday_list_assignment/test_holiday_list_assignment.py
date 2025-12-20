# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import frappe
from frappe.utils import add_months, get_year_ending, get_year_start, getdate

from erpnext.setup.doctype.employee.test_employee import make_employee

from hrms.payroll.doctype.salary_slip.test_salary_slip import make_holiday_list
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import DuplicateAssignment
from hrms.tests.utils import HRMSTestSuite
from hrms.utils.holiday_list import get_holiday_list_for_employee

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
		for d in ["Holiday List Assignment"]:
			frappe.db.delete(d)

		self.holiday_list = make_holiday_list(
			list_name="Test HLA", from_date=get_year_start(getdate()), to_date=get_year_ending(getdate())
		)

	def test_exisitng_assignment(self):
		from_date = get_year_start(getdate())
		to_date = get_year_ending(getdate())
		create_holiday_list_assignment(
			employee=self.employees[0].name,
			holiday_list=self.holiday_list,
			from_date=from_date,
			to_date=to_date,
		)

		self.assertRaises(
			DuplicateAssignment,
			create_holiday_list_assignment,
			employee=self.employees[0].name,
			holiday_list=self.holiday_list,
			from_date=from_date,
			to_date=to_date,
		)

	def test_set_dates_according_to_joining_and_relieving_date(self):
		date_of_joining = add_months(get_year_start(getdate()), 2)
		relieving_date = add_months(get_year_start(getdate()), 8)
		employee = make_employee(
			"test_hla@example.com",
			company="_Test Company",
			date_of_joining=date_of_joining,
			relieving_date=relieving_date,
		)
		hla = create_holiday_list_assignment(
			employee=employee,
			holiday_list=self.holiday_list,
			from_date=get_year_start(getdate()),
			to_date=get_year_ending(getdate()),
		)
		self.assertEqual(hla.from_date, date_of_joining)
		self.assertEqual(hla.to_date, relieving_date)

	def test_fetch_correct_holiday_list_assignment(self):
		employee = make_employee("test_hla@example.com", company="_Test Company")
		new_holiday_list = make_holiday_list(
			list_name="Test HLA New", from_date=get_year_start(getdate()), to_date=get_year_ending(getdate())
		)
		create_holiday_list_assignment(
			employee=employee,
			holiday_list=self.holiday_list,
			from_date=get_year_start(getdate()),
			to_date=get_year_ending(getdate()),
		)
		create_holiday_list_assignment(
			employee=employee,
			holiday_list=new_holiday_list,
			from_date=add_months(get_year_start(getdate()), 6),
			to_date=get_year_ending(getdate()),
		)
		applicable_holiday_list = get_holiday_list_for_employee(
			employee=employee, as_on=add_months(get_year_start(getdate()), 7)
		)
		self.assertEqual(applicable_holiday_list, "Test HLA New")


def create_holiday_list_assignment(
	employee, holiday_list, company="_Test Company", do_not_submit=False, from_date=None, to_date=None
):
	hla = frappe.new_doc("Holiday List Assignment")
	hla.employee = employee
	hla.holiday_list = holiday_list
	hla.company = company
	if not from_date:
		from_date = frappe.db.get_value("Holiday List", holiday_list, "from_date")
	if not to_date:
		to_date = frappe.db.get_value("Holiday List", holiday_list, "to_date")
	hla.from_date = from_date
	hla.to_date = to_date
	hla.save()
	if do_not_submit:
		return hla
	hla.submit()

	return hla
