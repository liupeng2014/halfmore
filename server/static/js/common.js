function clickUserChange (btn, op) {
	document.list.userid.value = btn.id;
	document.list.op.value = op;
	document.list.submit();
}

function clickDeviceChange (btn, op) {
	document.list.deviceid.value = btn.id;
	document.list.op.value = op;
	document.list.submit();
}

function clickAPSChange (btn, op) {
	document.list.apsid.value = btn.id;
	document.list.op.value = op;
	document.list.submit();
}

function clickNetworkChange (btn, op) {
	document.list.networkid.value = btn.id;
	document.list.op.value = op;
	document.list.submit();
}

function clickPermissionChange (btn, op) {
	document.list.permissionid.value = btn.id;
	document.list.op.value = op;
	document.list.submit();
}

function clickSWNodeChange (btn, op) {
	document.list.swnodeid.value = btn.id;
	document.list.op.value = op;
	document.list.submit();
}

function clickDisassociate (btn) {
	document.connection.mac.value = btn.id;
	document.connection.submit();
}

function showLog (op) {
	document.log.logtype.value = op;
	document.log.submit();
}

function clickConnect () {
	var radiolist = document.getElementsByName("network");
	for (var i=0; i<radiolist.length; i++) {
		if (radiolist[i].checked) {
			document.networkselect.networkid.value = radiolist[i].value;
			break;
		}
	}
	document.networkselect.submit();
}

function clickPage (op) {
	if (op == "first") {
		pagenum = 1;
	} else if (op == "last") {
		pagenum = parseInt(document.getElementById("all").innerHTML);
	} else if (op == "prev") {
		pagenum = parseInt(document.getElementById("curr").innerHTML) - 1;
	} else if (op == "next") {
		pagenum = parseInt(document.getElementById("curr").innerHTML) + 1;
	}
	document.list.nextpage.value = pagenum;
	document.list.op.value = "turnpage";
	document.list.submit();
}
