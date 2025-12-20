// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Holiday List Assignment", {
	assigned_entity: function (frm) {
		frm.trigger("toggle_fields");
		frm.trigger("clear_fields");
	},
	toggle_fields: function (frm) {
		frm.toggle_display(
			["employee_name", "employee_company"],
			frm.doc.assigned_entity == "Employee",
		);
	},
	clear_fields: function (frm) {
		frm.set_value("assigned_to", "");
		frm.set_value("employee_name", "");
		frm.set_value("employee_company", "");
	},
	assigned_to: function (frm) {
		if (frm.doc.assigned_entity == "Employee" && frm.doc.assigned_to) {
			frm.trigger("toggle_fields");
			frappe.db.get_value(
				"Employee",
				frm.doc.assigned_to,
				["employee_name", "company"],
				(r) => {
					frm.set_value("employee_name", r.employee_name);
					frm.set_value("employee_company", r.company);
				},
			);
		}
	},
	holiday_list: function (frm) {
		frm.trigger("set_to_and_from_dates");
	},
	set_to_and_from_dates: function (frm) {
		if (!frm.doc.holiday_list) return;
		frappe.db.get_value(
			"Holiday List",
			frm.doc.holiday_list,
			["from_date", "to_date"],
			(r) => {
				frm.set_value("from_date", r.from_date);
				frm.set_value("to_date", r.to_date);
			},
		);
	},
});
