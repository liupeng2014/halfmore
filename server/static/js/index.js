var w_width, w_height, c_left, c_height;

function setFrame () {
	w_width = window.innerWidth ? window.innerWidth : $(window).width();
	c_left = 0;
	if (w_width > 1000) {
		c_left = (w_width - 1000)/2;
	}

	w_height = window.innerHeight ? window.innerHeight : $(window).height();
	if (w_height < 500) {
		c_height = 500;
	}

	$("#div_bg").css("height", c_height+30);
	$("#div_navi").css("left", c_left);
	$("#div_create").css("left", c_left);
	$("#div_profile").css("left", c_left);
	$("#div_rolelist").css("left", c_left);
//	$("#rolelist").css("height", role_height);
	$("#div_main").css("left", c_left+200);
//	$("#main").css("height", c_height);
	$("#div_right").css("left", c_left+800);
//	$("#right").css("height", c_height);
	$("#div_message").css("left", c_left);
}

function clickRoleUp (role_whole_id) {
	var hit;
	for (var i = 0; i < role_list.length; i++) {
		var role = role_list[i];
		if (role_whole_id == role["whole_id"]) {
			if (i != 0) {
				hit = role_list[i];
				for (var j = i; j > 0; j--) {
					role_list[j] = role_list[j-1];
				}
				role_list[0] = hit;

				setProfile();
				setRoleList();
			}
			break;
		}
	}
}

function clickRoleSet (role_whole_id) {
	var set_role = "\
		<table align='center'>\
			<tr>\
				<td height='50px' colspan='3'>\
			</tr>\
			<tr>\
				<td width='100px'>\
					<span>Act Name</span>\
				</td>\
				<td width='20px'></td>\
				<td width='100px'>\
					<input type='text' id='txt_act_new' size='10' maxlength='20'>\
				</td>\
			</tr>\
			<tr>\
				<td width='100px'>\
					<input type='button' value='cancle' onclick='showCreateIndex()'>\
				</td>\
				<td width='20px'></td>\
				<td width='100px'>\
					<input type='button' value='create' onclick='clickCrateAct()'>\
				</td>\
			</tr>\
		</table>\
	";

	document.getElementById("div_create").innerHTML = create_act;
}

function getRoleFromList (role_whole_id) {
	for (var i = 0; i < role_list.length; i++) {
		var role = role_list[i];
		if (role_whole_id == role["whole_id"]) {
			return role;	
		}
	}
	return null;
}

function clickDivRole (divObj) {
	clickRoleUp(divObj.id);
}

function clickBtnExit (whole_id) {
	var form_name = "frm_exit";
	var form = document.forms[form_name];
	var role = getRoleFromList(whole_id);

	if (role) {
		return;
	}

	setHidden("hdn_rol", role["name"], form_name);
	setHidden("hdn_act", role["act_name"], form_name);
	setHidden("hdn_cur", whole_id, form_name);
	form.method = "post";
	form.submit();
}

function clickBtnSet (whole_id) {
	var role = getRoleFromList(whole_id);

	if (role) {
		return;
	}
}

function writeRoleCell (role, left, top) {
  var role_html = "<div id='" + role["whole_id"] + "' class='role' style='left:" + left + ";top:" + top + "' onclick='clickDivRole(this)'>" + role["whole_name"]
				+   "<input type='button' value='Exit' id='" + role["whole_id"] + "' onclick='clickBtnExit(\"" + role["whole_id"] + "\")'></td>"
				+   "<input type='button' value='Set' id='" + role["whole_id"] + "' onclick='clickBtnSet(\"" + role["whole_id"] + "\")'></td>"
				+ "</div>";
  return role_html;
}

function setRoleList () {
	var role_cnt = role_list.length;
	var role_height = role_cnt > 3 ? 150 : role_cnt < 1 ? 50 : role_cnt * 50;
	var role_top = 380;

	$("#div_rolelist").css("height", role_height);

	if (role_list[0] != null && role_list[0]["whole_id"] != null) {
		$("#div_rolelist").html("");
		for (var i = 0; i < role_cnt; i++) {
			var r = role_list[i];
			$("#div_rolelist").append(writeRoleCell(r, c_left, role_top));
			role_top += 50;
		}
	} else {
		$("#div_rolelist").html("not login");
	}
}

function setProfile () {
	var role = role_list[0];
	var roleinfo ="";

	if (role) {
		var key = "";
		for (key in role) {
			roleinfo += key + ": " + role[key] + "<br>";
		}
	} else {
		roleinfo = "roleinfo is null";
	}
	$("#div_profile").html(roleinfo);
}

function setPost () {
	$("#div_main").append("<div id='post01' class='post'>post01</div>");
	$("#div_main").append("<div id='post02' class='post'>post02 post02 post02 post02 post02 post02 post02 post02 post02 post02 post02 post02 post02 post02</div>");
	$("#div_main").append("<div id='post03' class='post'>理由は半角英数の連なりは1単語として判断されるから。理由は半角英数の連なりは1単語として判断されるから。</div>");
}

function setHidden (id, value, form_name) {
	var h = document.getElementById(id);
	if (h) {
		h.value = value;
	} else {
		h = document.createElement('input');
		h.type = 'hidden';
		h.id = id;
		h.name = id;
		h.value = value;
		document.forms[form_name].appendChild(h);
	}
}

function clickEnter () {
	var form_name = "frm_enter";
	var form = document.forms[form_name];
	var txt_rol = document.getElementById("txt_rol_usr");
	var txt_act = document.getElementById("txt_act_usr");
	var txt_pwd = document.getElementById("txt_pwd_usr");

	if (txt_rol.value.length == 0 ) {
		alert("rol.length=" + txt_rol.value.length);
		return false;
	}
	if (txt_act.value.length == 0 ) {
		alert("act.length=" + txt_act.value.length);
		return false;
	}
	if (txt_pwd.value.length < 4 ) {
		alert("pwd.length=" + txt_pwd.value.length);
		return false;
	}

	setHidden("hdn_rol", txt_rol.value, form_name);
	setHidden("hdn_act", txt_act.value, form_name);
	setHidden("hdn_pwd", txt_pwd.value, form_name);

	form.method = "post";
	form.submit();
}

function onKeyDown (e) {
	if((e.which && e.which == 13) ||
		(e.keyCode && e.keyCode ==13)) {
		clickEnter();
		return false;
	}
}

function clickAddNew () {
	document.getElementById("div_grey").style.display = "block";
	document.getElementById("div_create").style.display = "block";
}

function clickCreate () {
	document.getElementById("div_grey").style.display = "none";
	document.getElementById("div_create").style.display = "none";
}

function loadNavi () {
	var navi = "<table>"
		+	"<tr>"
		+		"<td>HalfMore LOGO</td>"
		+		"<td width='20px'></td>"
		+		"<td><input type='button' value='Add New' onclick='loadCreate()'></td>"
		+		"<td width='20px'></td>"
		+		"<td><input type='text' id='txt_rol_usr' size='10' maxlength='20' onkeydown='onKeyDown(event)'></td>"
		+		"<td>@</td>"
		+		"<td><input type='text' id='txt_act_usr' size='10' maxlength='20' onkeydown='onKeyDown(event)'></td>"
		+		"<td width='10px'></td>"
		+		"<td><input type='password' id='txt_pwd_usr' size='10' maxlength='20' onkeydown='onKeyDown(event)'></td>"
		+		"<td width='10px'></td>"
		+		"<td><input type='button' value='Enter' onclick='clickEnter()'></td>"
		+	"</tr>"
		+ "</table>";

	document.getElementById("div_navi").innerHTML = navi;
	document.getElementById("txt_rol_usr").focus();
}

function loadMessage () {
	if (error.length == 0) {
		setFrame();
		return;
	}

	document.getElementById("div_message").innerHTML = "<ul><li>" + error + "</li></ul>";
	document.getElementById("div_message").style.display = "block";

	$("#div_close").css("left", c_left+950);
	document.getElementById("div_close").innerHTML = "<p><font size='6'>&times;</font></p>";
	document.getElementById("div_close").style.display = "block";
}

function clickClose () {
	document.getElementById("div_close").style.display = "none";

	if (document.getElementById("div_message").style.display == "block") {
		document.getElementById("div_message").style.display = "none";
	}

	if (document.getElementById("div_create").style.display == "block") {
		document.getElementById("div_create").style.display = "none";
	}
}

function clickCrateAct () {
	var form_name = "frm_create";
	var form = document.forms[form_name];
	var txt_act_new = document.getElementById("txt_act_new");

	if (txt_act_new.value.length == 0 ) {
		alert("rol.length=0");
		return false;
	}

	setHidden("hdn_act_new", txt_act_new.value, form_name);
	setHidden("hdn_new_type", "act", form_name);

	form.method = "post";
	form.submit();
}

function clickCreateNewAct () {
	var create_act = "<table align='center'>"
		+	"<tr>"
		+		"<td height='50px' colspan='3'>"
		+	"</tr>"
		+	"<tr>"
		+		"<td width='100px'>"
		+			"<span>Act Name</span>"
		+		"</td>"
		+		"<td width='20px'></td>"
		+		"<td width='100px'>"
		+			"<input type='text' id='txt_act_new' size='10' maxlength='20'>"
		+		"</td>"
		+	"</tr>"
		+	"<tr>"
		+		"<td width='100px'>"
		+			"<input type='button' value='cancle' onclick='showCreateIndex()'>"
		+		"</td>"
		+		"<td width='20px'></td>"
		+		"<td width='100px'>"
		+			"<input type='button' value='create' onclick='clickCrateAct()'>"
		+		"</td>"
		+	"</tr>"
		+ "</table>";

	document.getElementById("div_create").innerHTML = create_act;
	document.getElementById("div_create").style.display = "block";
}

function clickCreateNewRole () {
	var create_role = "<table align='center'>"
		+	"<tr>"
		+		"<td height='50px' colspan='3'>"
		+	"</tr>"
		+	"<tr>"
		+		"<td width='100px'>"
		+			"<span>Role Name</span>"
		+		"</td>"
		+		"<td width='20px'></td>"
		+		"<td width='100px'>"
		+			"<input type='text' id='txt_act_role' size='10' maxlength='20'>"
		+			"<span>@act_name</span>"
		+		"</td>"
		+	"</tr>"
		+	"<tr>"
		+		"<td width='100px'>"
		+			"<input type='button' value='cancel' onclick='showCreateIndex()'>"
		+		"</td>"
		+		"<td width='20px'></td>"
		+		"<td width='100px'>"
		+			"<input type='button' value='create' onclick='clickCrateRole()'>"
		+		"</td>"
		+	"</tr>"
		+ "</table>";

	document.getElementById("div_create").innerHTML = create_role;
	document.getElementById("div_create").style.display = "block";
}

function showCreateIndex () {
	var create_index = "<table align='center'>"
		+	"<tr>"
		+		"<td height='50px' colspan='3'>"
		+	"</tr>"
		+	"<tr>"
		+		"<td width='300px' height='300px'>"
		+			"<div width='300px' height='300px' onclick='clickCreateNewAct()'>Create new act</div>"
		+		"</td>"
		+		"<td width='50px' height='300px'></td>"
		+		"<td width='300px' height='300px'>"
		+			"<div width='300px' height='300px' onclick='clickCreateNewRole()'>Create new role</div>"
		+		"</td>"
		+	"</tr>"
		+	"<tr>"
		+		"<td height='50px' colspan='3'>"
		+	"</tr>"
		+ "</table>";

	document.getElementById("div_create").innerHTML = create_index;
	document.getElementById("div_create").style.display = "block";
}

function loadCreate () {
	showCreateIndex();

	$("#div_close").css("left", c_left+950);
	document.getElementById("div_close").innerHTML = "<font size='6'>X</font>";
	document.getElementById("div_close").style.display = "block";
}

