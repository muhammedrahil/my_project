
from dbconnection import *
from flask import *
import functools

app = Flask(__name__)
app.secret_key = "key"


# def login_required(func):
#     @functools.wraps(func)
#     def secure_function():
#         if "lid" not in session:
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
        return '''<script>alert ("invalid");window.location="/"</script>'''
    elif result[3] == 'admin':
        session['lid'] = True
        return '''<script>alert("login successfull");window.location="/admins"</script>'''
    elif result[3] == 'manager':
        return '''<script>alert("login successfull");window.location="/manager"</script>'''
    elif result[3] == "employee":
        # session['lid']=True
        return '''<script>alert("login successfull");window.location="/employee"</script>'''
    else:
        return '''<script>alert("invalid");window.location="/"</script>'''


@app.route("/logout")
# @login_required
def logout():
    session.clear()
    return redirect('/')


@app.route("/admins")
# @login_required
def admins():
    # if(session['lid']):
    return render_template("admin/admins.html")
    # else:
    #     return redirect('/')


@app.route("/addEmployee")
def addEmployee():
    return render_template("admin/addEmployee.html")


@app.route("/manager")
def manager():
    return render_template("maneger/maneger.html")


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
    return '''<script>alert("added successfully");window.location="/admins"</script>'''


@app.route("/ViewEmployee")
def ViewEmployee():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("admin/viewEmployee.html", val=res)


@app.route("/DeleteEmployee")
def DeleteEmployee():
    id = request.args.get('id')
    qry = "DELETE FROM `employee` WHERE `loginid`=%s "
    iud(qry, id)
    return '''<script>alert("delete succussfull");window.location="/ViewEmployee"</script>'''


@app.route("/employee")
def employee():
    return render_template("employee/employee.html")


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
        return '''<script>alert ("invalid");window.location="/SearchEmployee"</script>'''
    elif result[8] == "employee":
        session['eid'] = result[0]
        return '''<script>alert("leave request");window.location="/leaveRequest"</script>'''
    else:
        return '''<script>alert("invalid request");window.location="/SearchEmployee"</script>'''


@app.route("/leaveRequest")
def leaveRequest():
    return render_template("employee/leaveRequest.html")


@app.route("/GetLeaveRequest", methods=['post'])
def GetLeaveRequest():
    LRid = session['eid']
    reason = request.form['reason']
    date = request.form['date']
    expdate = request.form['expdate']
    print(reason)
    if(reason == 'others'):
        reason = request.form['discription']
    qry = "INSERT INTO `leaverequest` VALUES (NULL,%s,'pending',%s,%s,%s)"
    val = (reason, LRid, date, expdate)
    iud(qry, val)
    return '''<script>alert("leave reaquest succussfull");window.location="/employee"</script>'''


@app.route("/ViewReaqusetEmployee")
def ViewReaqusetEmployee():
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`emp_id`=`leaverequest`.`emp_id` WHERE `leaverequest`.`status`='pending'"
    res = select(qry)
    return render_template("admin/viewLeaveRequest.html", val=res)


@app.route("/AcceptReaqusetEmployee")
def AcceptReaqusetEmployee():
    accept = "accept"
    id = request.args.get('id')
    session['id'] = id
    qry = "update`leaverequest` set `status`=%s WHERE LRid =%s"
    val = (accept, session['id'])
    iud(qry, val)
    return '''<script>alert("accept successfully");window.location="/ViewReaqusetEmployee"</script>'''


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
    qry = "SELECT `login`.*,`employee`.* FROM `login`JOIN`employee`ON`login`.`loginid`=`employee`.`loginid`"
    res = select(qry)
    return render_template("admin/setTarget.html", val=res)


@app.route("/SettargetEmployees")
def SettargetEmployees():
    id = request.args.get('id')
    session['id'] = id
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`emp_id`=`target`.`emp_id`WHERE employee.emp_id=%s"
    res = selectone(qry, id)
    print(res)
    if(res == None):
        return render_template("admin/target.html", val=res)
    else:
        return '''<script>alert("already set ,update employee target");window.location="/SetEmployeestarget"</script>'''


@app.route("/GettargetEmployees", methods=['post'])
def GettargetEmployees():
    number = request.form['number']
    qry = "INSERT INTO `target` VALUES (NULL,%s,%s,%s)"
    val = (number, session['id'], 00)
    iud(qry, val)
    return '''<script>alert("Target successfully Set");window.location="/viewupdatetargetEmployees"</script>'''


@app.route("/viewupdatetargetEmployees")
def viewupdatetargetEmployees():
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`emp_id`=`target`.`emp_id` "
    res = select(qry)
    return render_template("admin/ViewtargetEmp.html", val=res)


@app.route("/updateEmployeestarget")
def updateEmployeestarget():
    id = request.args.get('id')
    session['tid'] = id
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`emp_id`=`target`.`emp_id`where `target`. `trid`=%s "
    res = selectone(qry, id)
    return render_template("admin/updateTarget.html", val=res)


@app.route("/GetupdatetargetEmployees", methods=['post'])
def GetupdatetargetEmployees():
    number = request.form['number']
    qry = "update target set target=%s WHERE trid =%s"
    val = (number, session['tid'])
    iud(qry, val)
    return '''<script>alert("Target successfully Set");window.location="/viewupdatetargetEmployees"</script>'''


@app.route("/AchiveEmployeestarget")
def AchiveEmployeestarget():
    id = request.args.get('id')
    session['tid'] = id
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`emp_id`=`target`.`emp_id`where `target`. `trid`=%s "
    res = selectone(qry, id)
    return render_template("admin/Achive.html", val=res)


@app.route("/GetAchiveEmployeestarget", methods=['post'])
def GetAchiveEmployeestarget():
    number = request.form['number']
    qry = "UPDATE target SET `achive`=%s WHERE trid =%s"
    val = (number, session['tid'])
    iud(qry, val)
    return '''<script>alert(" achive Target successfully Set");window.location="/viewupdatetargetEmployees"</script>'''


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
        session['rid'] = result[0]
        return '''<script>alert("thanks");window.location="/ViewEmployeeTargetList"</script>'''
    else:
        return '''<script>alert("invalid request");window.location="/SearchEmployee"</script>'''


@app.route("/ViewEmployeeTargetList")
def ViewEmployeeTargetList():
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`emp_id`=%s"
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
        session['rid'] = result[0]
        return '''<script>alert("thanks");window.location="/viewLeaveRequestPage"</script>'''
    else:
        return '''<script>alert("invalid request");window.location="/ViewLeaveRequestPage"</script>'''


@app.route("/viewLeaveRequestPage")
def viewLeaveRequestPage():
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`emp_id`=`leaverequest`.`emp_id`WHERE `leaverequest`.`status`='accept' OR `leaverequest`.`status`='reject' "
    res = select(qry)
    return render_template("employee/viewLeaveRequestPage.html", val=res)


@app.route("/StatusviewLeaveRequest")
def StatusviewLeaveRequest():
    id = request.args.get('id')
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `leaverequest`.`LRid`=%s WHERE `leaverequest`.`status`='accept' OR `leaverequest`.`status`='reject'"
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
        session['rid'] = result[0]
        return '''<script>alert("thanks");window.location="/PymentPage"</script>'''
    else:
        return '''<script>alert("invalid request");window.location="/ViewLeaveRequestPage"</script>'''



@app.route("/PymentPage")
def PymentPage():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/PymentPage.html", val=res)


@app.route("/GetPymentPage",methods=['post'])
def GetPymentPage():
    PymentOption = request.form['PymentOption']
    pyment = request.form['pyment']
    qry="INSERT INTO `pyment` VALUES (NULL,%s,%s,%s,'pending')"
    val=(PymentOption,pyment,session['rid'])
    iud(qry,val)
    return '''<script>alert(" succesfully");window.location="/employee"</script>'''


@app.route("/BranchEmployeePymentPage")
def BranchEmployeePymentPage():
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`emp_id`=`pyment`.`emp_id` WHERE`pyment`.`status`='pending'"
    res = select(qry)
    return render_template("maneger/viewPymentEmployee.html", val=res)

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
        session['rid'] = result[0]
        return '''<script>alert("thanks");window.location="/listPymentListseployee"</script>'''
    else:
        return '''<script>alert("invalid request");window.location="/ViewLeaveRequestPage"</script>'''\

@app.route("/listPymentListseployee")
def listPymentListseployee():
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`emp_id`=`pyment`.`emp_id`WHERE `pyment`.`status`='accept' OR `pyment`.`status`='reject'  "
    res = select(qry)
    return render_template("employee/listPymentListseployee.html", val=res)

@app.route("/StatusviewlistPymentListseployee")
def StatusviewlistPymentListseployee():
    id = request.args.get('id')
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `pyment`.`pid`=%sWHERE `pyment`.`status`='accept' OR `pyment`.`status`='reject' "
    res = selectone(qry, id)
    return render_template("employee/SearchViewPaymentList.html", val=res)    

if __name__ == "__main__":
    app.run(debug=True)
