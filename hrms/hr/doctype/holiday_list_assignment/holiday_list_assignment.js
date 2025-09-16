// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Holiday List Assignment", {
	holiday_list: function (frm) {
		frm.trigger("set_to_and_from_dates");
	},
	set_to_and_from_dates: function (frm) {
		if (!frm.doc.holiday_list) return;
		frappe.db.get_value("Holiday List", frm.doc.holiday_list, "from_date", (r) => {
			frm.set_value("from_date", r.from_date);
		});
	},
});
