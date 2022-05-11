
from dbconnection import *
from flask import *
import functools

app = Flask(__name__)
app.secret_key = "key"


# def login_required(func):
#     @functools.wraps(func)
#     def secure_function():
#         if "lid"  not in session:
#             return redirect("/")
#         return func() 
#     return secure_function


@app.route("/")
def login():
    return render_template("admin/login.html")


@app.route("/getLogin", methods=['post'])
def getLogin():
    uname = request.form['uname']
    pwd = request.form['pwd']
    qry = "select * from login where username =%s and ecode=%s"
    vals = (uname, pwd)
    result = selectone(qry, vals)
    if result is None:
        return '''<script>alert ("Invalid User Name OR Password");window.location="/"</script>'''
    elif result[3] == 'admin':
        session['lid'] = True
        return '''<script>alert("admin login successfully");window.location="/admins"</script>'''
    elif result[3] == 'manager':
        session['mid'] = True
        return '''<script>alert(" maneger login successfully");window.location="/admins"</script>'''
    elif result[3] == "employee":
        session['emid']=True
        return '''<script>alert("login successfull");window.location="/employee"</script>'''
    else:
        return '''<script>alert("invalid");window.location="/"</script>'''


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


@app.route("/admins")
def admins():
    return render_template("admin/home.html")
  


@app.route("/addEmployee")
def addEmployee():
    return render_template("admin/addEmployee.html")



@app.route("/GetaddEmployee", methods=['post'])
def GetaddEmployee():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    logqry = "INSERT INTO login VALUES (NULL,%s,%s,'employee')"
    logval = (ename, ecode)
    lid = iud(logqry, logval)
    qry = "INSERT INTO `employee` VALUES (NULL,%s,%s,%s,%s)"
    val = (ename, ecode, branch, str(lid))
    iud(qry, val)
    return '''<script>alert("New Employee added successfully");window.location="/admins"</script>'''


@app.route("/ViewEmployee")
def ViewEmployee():
    qry = "SELECT * FROM `employee` ORDER BY emp_id DESC"
    res = select(qry)
    return render_template("admin/viewEmployee.html", val=res)

@app.route("/Search_branch", methods=['post'])
def Search_branch():
    branch = request.form['branch']
    qry = "SELECT * FROM `employee` WHERE `branch`=%s ORDER BY `employee`.`emp_id` DESC"
    res = selectall(qry,branch)
    return render_template("admin/SearchViewEmployee.html", val=res)


@app.route("/DeleteEmployee")
def DeleteEmployee():
    id = request.args.get('id')
    qry = "DELETE FROM `employee` WHERE `loginid`=%s "
    iud(qry, id)
    return '''<script>alert("delete succussfull");window.location="/ViewEmployee"</script>'''

@app.route("/employeepage")
def employeepage():
    return render_template("employee/home.html")


@app.route("/about")
def about():
    return render_template("temp/about.html")


@app.route("/employee")
def employee():
    return redirect('/employeepage')


@app.route("/SearchEmployee")
def SearchEmployee():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/SearchEmployye.html", val=res)


@app.route("/getvalSearchEmployee", methods=['post'])
def getvalSearchEmployee():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s"
    val = (ename, ecode, branch)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("Invalid ");window.location="/SearchEmployee"</script>'''
    elif result[8] == "employee":
        session['eid'] = result[4]
        return '''<script>alert("Thank you,Please Request Your Leave");window.location="/leaveRequest"</script>'''
    else:
        return '''<script>alert("invalid ");window.location="/SearchEmployee"</script>'''


@app.route("/leaveRequestPage")
def leaveRequestPage():
    return render_template("employee/leaveRequest.html")
    

@app.route("/leaveRequest")
def leaveRequest():
    return redirect('/leaveRequestPage')


@app.route("/GetLeaveRequest", methods=['post'])
def GetLeaveRequest():
    LRid = session['eid']
    reason = request.form['reason']
    date = request.form['date']
    expdate = request.form['expdate']
    if(reason == 'others'):
        reason = request.form['discription']
    qry = "INSERT INTO `leaverequest` VALUES (NULL,%s,'pending',%s,%s,%s,CURDATE())"
    val = (reason, LRid, date, expdate)
    iud(qry, val)
    return '''<script>alert("leave reaquest succussfull");window.location="/employee"</script>'''


@app.route("/ViewReaqusetEmployee")
def ViewReaqusetEmployee():
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='pending'  ORDER BY `leaverequest`.`LRid` DESC"
    res = select(qry)
    return render_template("admin/viewLeaveRequest.html", val=res)

@app.route("/Search_branch_Leave", methods=['post'])
def Search_branch_Leave():
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='pending' AND `employee`.`branch`=%s ORDER BY `leaverequest`.`LRid` DESC"
    res = selectall(qry,branch)
    return render_template("admin/Search_branch_Leave.html", val=res)


@app.route("/AcceptReaqusetEmployee")
def AcceptReaqusetEmployee():
    accept = "accept"
    id = request.args.get('id')
    session['id'] = id
    qry = "update`leaverequest` set `status`=%s WHERE LRid =%s"
    val = (accept, session['id'])
    iud(qry, val)
    return '''<script>alert("accept successfully");window.location="/ViewReaqusetEmployee"</script>'''

@app.route("/accept_list_leave")
def accept_list_leave():   
    qry="SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='accept'  ORDER BY `leaverequest`.`LRid` DESC"
    res = select(qry)
    return render_template("admin/accept_list.html",val=res) 


@app.route("/rejectReaqusetEmployee")
def rejectReaqusetEmployee():
    reject = "reject"
    id = request.args.get('id')
    session['id'] = id
    qry = "update`leaverequest` set `status`=%s WHERE LRid =%s"
    val = (reject, session['id'])
    iud(qry, val)
    return '''<script>alert("reject successfully");window.location="/ViewReaqusetEmployee"</script>'''


@app.route("/SetEmployeestarget")
def SetEmployeestarget():
    qry = "SELECT `login`.*,`employee`.* FROM `login`JOIN`employee`ON`login`.`loginid`=`employee`.`loginid` ORDER BY `employee`.`emp_id` DESC"
    res = select(qry)
    return render_template("admin/setTarget.html", val=res)

@app.route("/Search_branch_SetTarget", methods=['post'])
def Search_branch_SetTarget():
    branch = request.form['branch']
    qry = "SELECT `login`.*,`employee`.* FROM `login`JOIN`employee`ON`login`.`loginid`=`employee`.`loginid` WHERE `employee`.`branch`=%s ORDER BY `employee`.`emp_id` DESC"
    res = selectall(qry,branch)
    return render_template("admin/Search_branch_SetTarget.html", val=res)

@app.route("/SettargetEmployees")
def SettargetEmployees():
    id = request.args.get('id')
    session['id'] = id
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`loginid`=`target`.`lg_id` WHERE `employee`.`loginid`=%s"
    res = selectone(qry, id)
    if(res == None):
        return render_template("admin/target.html", val=res)
    else:
        return '''<script>alert("already set ,Please update employee target");window.location="/viewupdatetargetEmployees"</script>'''


@app.route("/GettargetEmployees", methods=['post'])
def GettargetEmployees():
    number = request.form['number']
    qry = "INSERT INTO `target` VALUES (NULL,%s,%s,%s)"
    val = (number, session['id'], 00)
    iud(qry, val)
    return '''<script>alert("Target successfully ");window.location="/viewupdatetargetEmployees"</script>'''


@app.route("/viewupdatetargetEmployees")
def viewupdatetargetEmployees():
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` ORDER BY `employee`.`emp_id` DESC"
    res = select(qry)
    return render_template("admin/ViewtargetEmp.html", val=res)

@app.route("/Search_viewupdatetargetEmployees", methods=['post'])
def Search_viewupdatetargetEmployees():
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id`  WHERE `employee`.`branch`=%s ORDER BY `employee`.`emp_id` DESC"
    res = selectall(qry,branch)
    return render_template("admin/Search_viewupdatetargetEmployees.html", val=res)

@app.route("/updateEmployeestarget")
def updateEmployeestarget():
    id = request.args.get('id')
    session['tid'] = id
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` where `target`. `trid`=%s "
    res = selectone(qry, id)
    return render_template("admin/updateTarget.html", val=res)


@app.route("/GetupdatetargetEmployees", methods=['post'])
def GetupdatetargetEmployees():
    number = request.form['number']
    qry = "update target set target=%s WHERE trid =%s"
    val = (number, session['tid'])
    iud(qry, val)
    return '''<script>alert("Update Target successfully ");window.location="/viewupdatetargetEmployees"</script>'''


@app.route("/AchiveEmployeestarget")
def AchiveEmployeestarget():
    id = request.args.get('id')
    session['tid'] = id
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` where `target`. `trid`=%s "
    res = selectone(qry, id)
    return render_template("admin/Achive.html", val=res)


@app.route("/GetAchiveEmployeestarget", methods=['post'])
def GetAchiveEmployeestarget():
    number = request.form['number']
    qry = "UPDATE target SET `achive`=%s WHERE trid =%s"
    val = (number, session['tid'])
    iud(qry, val)
    return '''<script>alert(" achive Target successfully ");window.location="/viewupdatetargetEmployees"</script>'''


@app.route("/SearchTargetEmployeeView")
def SearchTargetEmployeeView():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/SearchTargetEmployeeView.html", val=res)


@app.route("/getvalTargetSearchEmployee", methods=['post'])
def getvalTargetSearchEmployee():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s"
    val = (ename, ecode, branch)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("invalid");window.location="/SearchEmployee"</script>'''
    elif result[8] == "employee":
        session['rid'] = result[4]
        return '''<script>alert("Thank you , Please View Your Target And Achive Target ");window.location="/ViewEmployeeTargetList"</script>'''
    else:
        return '''<script>alert("invalid ");window.location="/SearchEmployee"</script>'''


@app.route("/ViewEmployeeTargetList")
def ViewEmployeeTargetList():
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`loginid`=`target`.`lg_id` WHERE `employee`.`loginid`=%s"
    res = selectone(qry, session['rid'])
    return render_template("employee/ViewEmployeeTargetList.html", val=res)


@app.route("/ViewLeaveRequestPage")
def ViewLeaveRequestPage():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/ViewLeaveRequest.html", val=res)


@app.route("/GetViewLeaveRequestPage", methods=['post'])
def GetViewLeaveRequestPage():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s"
    val = (ename, ecode, branch)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("invalid");window.location="/ViewLeaveRequestPage"</script>'''
    elif result[8] == "employee":
        session['rid'] = result[4]
        return '''<script>alert("Thank you,Please View Your Leave Request Status");window.location="/viewLeaveRequestPage"</script>'''
    else:
        return '''<script>alert("invalid ");window.location="/ViewLeaveRequestPage"</script>'''


@app.route("/viewLeaveRequestPage")
def viewLeaveRequestPage():
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE  `employee`.`loginid`= %s ORDER BY `leaverequest`.`LRid` DESC"
    res = selectall(qry,session['rid'])
    return render_template("employee/viewLeaveRequestPage.html", val=res)


@app.route("/StatusviewLeaveRequest")
def StatusviewLeaveRequest():
    id = request.args.get('id')
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `leaverequest`.`LRid`=%s "
    res = selectone(qry, id)
    return render_template("employee/ViewEmployeeLeaveList.html", val=res)


@app.route("/SearchPymentPage")
def SearchPymentPage():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/SearchPyment.html", val=res)


@app.route("/GetSearchPymentPage", methods=['post'])
def GetSearchPymentPage():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s"
    val = (ename, ecode, branch)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("invalid");window.location="/ViewLeaveRequestPage"</script>'''
    elif result[8] == "employee":
        session['rid'] = result[4]
        return '''<script>alert("Thank you,Please Request Your Pyment");window.location="/PymentPage"</script>'''
    else:
        return '''<script>alert("invalid ");window.location="/ViewLeaveRequestPage"</script>'''



@app.route("/PymentPage")
def PymentPage():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/PymentPage.html", val=res)


@app.route("/GetPymentPage",methods=['post'])
def GetPymentPage():
    PymentOption = request.form['PymentOption']
    pyment = request.form['pyment']
    if (PymentOption == "others"):
        PymentOption = request.form['discription']
    qry="INSERT INTO `pyment` VALUES (NULL,%s,%s,%s,'pending',CURDATE())"
    val=(PymentOption,pyment,session['rid'])
    iud(qry,val)
    return '''<script>alert("Pyment Request Succesfully");window.location="/employee"</script>'''


@app.route("/BranchEmployeePymentPage")
def BranchEmployeePymentPage():
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='pending' ORDER BY `pyment`.`pid` DESC"
    res = select(qry)
    return render_template("maneger/viewPymentEmployee.html", val=res)

@app.route("/Search_branch_Pyment",methods=['post'])
def Search_branch_Pyment():
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='pending' AND `employee`.`branch`=%s ORDER BY `pyment`.`pid` DESC"
    res = selectall(qry,branch)
    return render_template("maneger/Search_branch_Pyment.html", val=res)

@app.route("/AcceptBranchEmployeePymentPage")
def AcceptBranchEmployeePymentPage():
    accept = "accept"
    id = request.args.get('id')
    qry = "update pyment set `status`=%s WHERE pid =%s"
    val = (accept, id)
    iud(qry, val)
    return '''<script>alert("accept successfully");window.location="/BranchEmployeePymentPage"</script>'''


@app.route("/rejectBranchEmployeePymentPage")
def rejectBranchEmployeePymentPage():
    reject = "reject"
    id = request.args.get('id')
    qry = "update pyment set `status`=%s WHERE pid =%s"
    val = (reject, id)
    iud(qry, val)
    return '''<script>alert("reject successfully");window.location="/BranchEmployeePymentPage"</script>'''


@app.route("/EditBranchEmployeePymentPage")
def EditBranchEmployeePymentPage():
    id = request.args.get('id')
    session['pid'] = id
    qry = "SELECT * FROM `pyment` WHERE`pid`=%s"
    res = selectone(qry,id)
    return render_template("maneger/EditPyment.html", val=res)

@app.route("/GetEditBranchEmployeePymentPage",methods=['post'])
def GetEditBranchEmployeePymentPage():
    money = request.form['number']
    qry = "update pyment set `moneny`=%s WHERE pid =%s"
    val=(money,session['pid'])
    iud(qry, val)
    return '''<script>alert("Edit successfully");window.location="/BranchEmployeePymentPage"</script>'''

@app.route("/SearchViewPayment")
def SearchViewPayment():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/SearchViewPayment.html", val=res)


@app.route("/GetSearchViewPayment", methods=['post'])
def GetSearchViewPayment():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s"
    val = (ename, ecode, branch)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("invalid");window.location="/ViewLeaveRequestPage"</script>'''
    elif result[8] == "employee":
        session['rid'] = result[4]
        return '''<script>alert("Thank you,Please View Your Pyment Status");window.location="/listPymentListseployee"</script>'''
    else:
        return '''<script>alert("invalid");window.location="/ViewLeaveRequestPage"</script>'''\

@app.route("/listPymentListseployee")
def listPymentListseployee():
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE `employee`.`loginid`=%s ORDER BY `pyment`.`pid` DESC"
    res = selectall(qry,session['rid'])
    return render_template("employee/listPymentListseployee.html", val=res)

@app.route("/StatusviewlistPymentListseployee")
def StatusviewlistPymentListseployee():
    id = request.args.get('id')
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `pyment`.`pid`=%s WHERE `pyment`.`status`='accept' OR `pyment`.`status`='reject'OR `pyment`.`status`='pending' "
    res = selectone(qry, id)
    return render_template("employee/SearchViewPaymentList.html", val=res)    

@app.route("/accept_list")
def accept_list():   
    qry="SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='accept' ORDER BY `pyment`.`pid` DESC"
    res = select(qry)
    return render_template("maneger/accept_list.html",val=res) 

if __name__ == "__main__":
    app.run(debug=True)
