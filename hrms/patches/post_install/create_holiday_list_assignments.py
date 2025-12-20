import frappe


def execute():
	employee = frappe.qb.DocType("Employee")
	holiday_list = frappe.qb.DocType("Holiday List")

	employee_holiday_details = (
		frappe.qb.from_(employee)
		.inner_join(holiday_list)
		.on(employee.holiday_list == holiday_list.name)
		.select(
			employee.name,
			employee.holiday_list,
			holiday_list.from_date,
			holiday_list.to_date,
			employee.company,
		)
		.where(employee.status == "Active")
	).run(as_dict=True)

	for employee in employee_holiday_details:
		try:
			create_holiday_list_assignment(employee)
		except Exception as e:
			frappe.log_error(e)


def create_holiday_list_assignment(employee):
	hla = frappe.new_doc("Holiday List Assignment")
	hla.employee = employee.name
	hla.company = employee.company
	hla.holiday_list = employee.holiday_list
	hla.from_date = employee.from_date
	hla.to_date = employee.to_date
	hla.save()
	hla.submit()
