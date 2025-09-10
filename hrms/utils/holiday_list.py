import frappe
from frappe import _


def get_holiday_dates_between(
	holiday_list: str,
	start_date: str,
	end_date: str,
	skip_weekly_offs: bool = False,
	as_dict: bool = False,
	select_weekly_off: bool = False,
) -> list:
	Holiday = frappe.qb.DocType("Holiday")
	query = frappe.qb.from_(Holiday).select(Holiday.holiday_date)

	if select_weekly_off:
		query = query.select(Holiday.weekly_off)

	query = query.where(
		(Holiday.parent == holiday_list) & (Holiday.holiday_date.between(start_date, end_date))
	)

	if skip_weekly_offs:
		query = query.where(Holiday.weekly_off == 0)

	if as_dict:
		return query.run(as_dict=True)

	return query.run(pluck=True)


def get_holiday_list_for_employee(employee: str, raise_exception: bool = True, as_on=None) -> str:
	as_on = frappe.utils.getdate(as_on)
	HLA = frappe.qb.DocType("Holiday List Assignment")
	query = (
		frappe.qb.from_(HLA)
		.select(HLA.holiday_list)
		.where(HLA.employee == employee)
		.where(HLA.from_date <= as_on)
		.where(HLA.to_date >= as_on)
		.where(HLA.docstatus == 1)
		.run()
	)
	holiday_list = query[0][0] if query else None

	if not holiday_list and raise_exception:
		frappe.throw(_("Please assign Holiday List for Employee {0}").format(employee))

	return holiday_list


def invalidate_cache(doc, method=None):
	from hrms.payroll.doctype.salary_slip.salary_slip import HOLIDAYS_BETWEEN_DATES

	frappe.cache().delete_value(HOLIDAYS_BETWEEN_DATES)
