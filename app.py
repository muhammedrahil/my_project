
from fileinput import filename
from dbconnection import *
from flask import *
import functools
from datetime import datetime
import time
import os

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
    elif result[3] == 'director':
        session['lid'] = True
        return '''<script>alert("Director Login Successfully");window.location="/admins"</script>'''
    elif result[3] == 'manager':
        session['mid'] = True
        return '''<script>alert(" Maneger Login Successfully");window.location="/admins"</script>'''
    elif result[3] == "employee":
        session['emid'] = True
        return '''<script>alert("Login Successfully");window.location="/employee"</script>'''
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
    return '''<script>alert("New Employee Added Successfully");window.location="/addEmployee"</script>'''


@app.route("/ViewEmployee")
def ViewEmployee():
    qry = "SELECT * FROM `employee` ORDER BY emp_id DESC"
    res = select(qry)
    return render_template("admin/viewEmployee.html", val=res)


@app.route("/Search_branch", methods=['post'])
def Search_branch():
    branch = request.form['branch']
    qry = "SELECT * FROM `employee` WHERE `branch`=%s ORDER BY `employee`.`emp_id` DESC"
    res = selectall(qry, branch)
    return render_template("admin/SearchViewEmployee.html", val=res)


@app.route("/DeleteEmployee")
def DeleteEmployee():
    id = request.args.get('id')
    qry = "DELETE FROM `employee` WHERE `loginid`=%s "
    iud(qry, id)
    return '''<script>alert("Delete Succussfull");window.location="/ViewEmployee"</script>'''


@app.route("/employeepage")
def employeepage():
    return render_template("employee/home.html")




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
    t = "17:00:00"
    test_time = datetime.strptime(t, '%H:%M:%S')
    current_time = datetime.now().strftime("%H:%M:%S")
    current_time = datetime.strptime(current_time, "%H:%M:%S")
    if(test_time.time() < current_time.time()):
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
    else:
        return '''<script>alert("Not Approved");window.location="/employee"</script>'''


@ app.route("/ViewReaqusetEmployee")
def ViewReaqusetEmployee():
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='pending'  ORDER BY `leaverequest`.`LRid` DESC"
    res = select(qry)
    return render_template("admin/viewLeaveRequest.html", val=res)


@ app.route("/Search_branch_Leave", methods=['post'])
def Search_branch_Leave():
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='pending' AND `employee`.`branch`=%s ORDER BY `leaverequest`.`LRid` DESC"
    res = selectall(qry, branch)
    return render_template("admin/Search_branch_Leave.html", val=res)


@ app.route("/AcceptReaqusetEmployee")
def AcceptReaqusetEmployee():
    accept = "Accept"
    id = request.args.get('id')
    session['id'] = id
    qry = "update`leaverequest` set `status`=%s WHERE LRid =%s"
    val = (accept, session['id'])
    iud(qry, val)
    return '''<script>alert("accept successfully");window.location="/ViewReaqusetEmployee"</script>'''


@ app.route("/accept_list_leave")
def accept_list_leave():
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='accept'  ORDER BY `leaverequest`.`LRid` DESC"
    res = select(qry)
    return render_template("admin/accept_list.html", val=res)


@ app.route("/rejectReaqusetEmployee")
def rejectReaqusetEmployee():
    reject = "Reject"
    id = request.args.get('id')
    session['id'] = id
    qry = "update`leaverequest` set `status`=%s WHERE LRid =%s"
    val = (reject, session['id'])
    iud(qry, val)
    return '''<script>alert("reject successfully");window.location="/ViewReaqusetEmployee"</script>'''


@ app.route("/SetEmployeestarget")
def SetEmployeestarget():
    qry = "SELECT `login`.*,`employee`.* FROM `login`JOIN`employee`ON`login`.`loginid`=`employee`.`loginid` ORDER BY `employee`.`emp_id` DESC"
    res = select(qry)
    return render_template("admin/setTarget.html", val=res)


@ app.route("/Search_branch_SetTarget", methods=['post'])
def Search_branch_SetTarget():
    branch = request.form['branch']
    qry = "SELECT `login`.*,`employee`.* FROM `login`JOIN`employee`ON`login`.`loginid`=`employee`.`loginid` WHERE `employee`.`branch`=%s ORDER BY `employee`.`emp_id` DESC"
    res = selectall(qry, branch)
    return render_template("admin/Search_branch_SetTarget.html", val=res)


@ app.route("/SettargetEmployees")
def SettargetEmployees():
    id = request.args.get('id')
    session['id'] = id
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`loginid`=`target`.`lg_id` WHERE `employee`.`loginid`=%s"
    res = selectone(qry, id)
    if(res == None):
        return render_template("admin/target.html", val=res)
    else:
        return '''<script>alert("already set ,Please update employee target");window.location="/viewupdatetargetEmployees"</script>'''


@ app.route("/GettargetEmployees", methods=['post'])
def GettargetEmployees():
    Gold = request.form['Gold']
    Diamond = request.form['Diamond']
    qry = "INSERT INTO `target` VALUES (NULL,%s,%s,%s,%s,%s)"
    val = (Gold, session['id'], 00, Diamond, 00)
    iud(qry, val)
    return '''<script>alert("Target successfully ");window.location="/viewupdatetargetEmployees"</script>'''


@ app.route("/viewupdatetargetEmployees")
def viewupdatetargetEmployees():
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` ORDER BY `employee`.`emp_id` DESC"
    res = select(qry)
    return render_template("admin/ViewtargetEmp.html", val=res)


@ app.route("/Search_viewupdatetargetEmployees", methods=['post'])
def Search_viewupdatetargetEmployees():
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id`  WHERE `employee`.`branch`=%s ORDER BY `employee`.`emp_id` DESC"
    res = selectall(qry, branch)
    return render_template("admin/Search_viewupdatetargetEmployees.html", val=res)


@ app.route("/updateEmployeestarget")
def updateEmployeestarget():
    id = request.args.get('id')
    session['tid'] = id
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` where `target`. `trid`=%s "
    res = selectone(qry, id)
    return render_template("admin/updateTarget.html", val=res)


@ app.route("/GetupdatetargetEmployees", methods=['post'])
def GetupdatetargetEmployees():
    Gold = request.form['Gold']
    Diamond = request.form['Diamond']
    qry = "UPDATE `target` SET `gold`=%s ,`Diamond`=%s WHERE trid =%s"
    val = (Gold, Diamond, session['tid'])
    iud(qry, val)
    return '''<script>alert("Update Target successfully ");window.location="/viewupdatetargetEmployees"</script>'''


@ app.route("/AchiveEmployeestarget")
def AchiveEmployeestarget():
    id = request.args.get('id')
    session['tid'] = id
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` where `target`. `trid`=%s "
    res = selectone(qry, id)
    return render_template("admin/Achive.html", val=res)


@ app.route("/GetAchiveEmployeestarget", methods=['post'])
def GetAchiveEmployeestarget():
    Gold = request.form['Gold']
    Diamond = request.form['Diamond']
    qry = "UPDATE target SET `achive_gold`=%s,`achive_diamond`=%s WHERE trid =%s"
    val = (Gold, Diamond, session['tid'])
    iud(qry, val)
    return '''<script>alert(" achive Target successfully ");window.location="/viewupdatetargetEmployees"</script>'''


@ app.route("/SearchTargetEmployeeView")
def SearchTargetEmployeeView():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/SearchTargetEmployeeView.html", val=res)


@ app.route("/getvalTargetSearchEmployee", methods=['post'])
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


@ app.route("/ViewEmployeeTargetList")
def ViewEmployeeTargetList():
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`loginid`=`target`.`lg_id` WHERE `employee`.`loginid`=%s"
    res = selectone(qry, session['rid'])
    return render_template("employee/ViewEmployeeTargetList.html", val=res)


@ app.route("/ViewLeaveRequestPage")
def ViewLeaveRequestPage():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/ViewLeaveRequest.html", val=res)


@ app.route("/GetViewLeaveRequestPage", methods=['post'])
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


@ app.route("/viewLeaveRequestPage")
def viewLeaveRequestPage():
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE  `employee`.`loginid`= %s ORDER BY `leaverequest`.`LRid` DESC"
    res = selectall(qry, session['rid'])
    return render_template("employee/viewLeaveRequestPage.html", val=res)


@ app.route("/StatusviewLeaveRequest")
def StatusviewLeaveRequest():
    id = request.args.get('id')
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id`WHERE`leaverequest`.`LRid`=%s"
    res = selectone(qry, id)
    return render_template("employee/ViewEmployeeLeaveList.html", val=res)


@ app.route("/SearchPymentPage")
def SearchPymentPage():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/SearchPyment.html", val=res)


@ app.route("/GetSearchPymentPage", methods=['post'])
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


@ app.route("/PymentPage")
def PymentPage():
    return render_template("employee/pymentPage.html")


@ app.route("/GetPymentPage", methods=['post'])
def GetPymentPage():
    PymentOption = request.form['PymentOption']
    pyment = request.form['pyment']
    if (PymentOption == "others"):
        PymentOption = request.form['discription']
    qry = "INSERT INTO `pyment` VALUES (NULL,%s,%s,%s,'pending',CURDATE())"
    val = (PymentOption, pyment, session['rid'])
    iud(qry, val)
    return '''<script>alert("Pyment Request Succesfully");window.location="/employee"</script>'''


@ app.route("/BranchEmployeePymentPage")
def BranchEmployeePymentPage():
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='pending' ORDER BY `pyment`.`pid` DESC"
    res = select(qry)
    return render_template("maneger/viewPymentEmployee.html", val=res)


@ app.route("/Search_branch_Pyment", methods=['post'])
def Search_branch_Pyment():
    branch = request.form['branch']
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='pending' AND `employee`.`branch`=%s ORDER BY `pyment`.`pid` DESC"
    res = selectall(qry, branch)
    return render_template("maneger/Search_branch_Pyment.html", val=res)


@ app.route("/AcceptBranchEmployeePymentPage")
def AcceptBranchEmployeePymentPage():
    accept = "Accept"
    id = request.args.get('id')
    qry = "update pyment set `status`=%s WHERE pid =%s"
    val = (accept, id)
    iud(qry, val)
    return '''<script>alert("accept successfully");window.location="/BranchEmployeePymentPage"</script>'''


@ app.route("/rejectBranchEmployeePymentPage")
def rejectBranchEmployeePymentPage():
    reject = "Reject"
    id = request.args.get('id')
    qry = "update pyment set `status`=%s WHERE pid =%s"
    val = (reject, id)
    iud(qry, val)
    return '''<script>alert("reject successfully");window.location="/BranchEmployeePymentPage"</script>'''


@ app.route("/EditBranchEmployeePymentPage")
def EditBranchEmployeePymentPage():
    id = request.args.get('id')
    session['pid'] = id
    qry = "SELECT * FROM `pyment` WHERE`pid`=%s"
    res = selectone(qry, id)
    return render_template("maneger/EditPyment.html", val=res)


@ app.route("/GetEditBranchEmployeePymentPage", methods=['post'])
def GetEditBranchEmployeePymentPage():
    money = request.form['number']
    qry = "update pyment set `moneny`=%s WHERE pid =%s"
    val = (money, session['pid'])
    iud(qry, val)
    return '''<script>alert("Edit successfully");window.location="/BranchEmployeePymentPage"</script>'''


@ app.route("/SearchViewPayment")
def SearchViewPayment():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/SearchViewPayment.html", val=res)


@ app.route("/GetSearchViewPayment", methods=['post'])
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
        return '''<script>alert("invalid");window.location="/ViewLeaveRequestPage"</script>'''


@ app.route("/listPymentListseployee")
def listPymentListseployee():
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE `employee`.`loginid`=%s ORDER BY `pyment`.`pid` DESC"
    res = selectall(qry, session['rid'])
    return render_template("employee/listPymentListseployee.html", val=res)


@ app.route("/StatusviewlistPymentListseployee")
def StatusviewlistPymentListseployee():
    id = request.args.get('id')
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `pyment`.`pid`=%s WHERE `pyment`.`status`='accept' OR `pyment`.`status`='reject'OR `pyment`.`status`='pending' "
    res = selectone(qry, id)
    return render_template("employee/SearchViewPaymentList.html", val=res)


@ app.route("/accept_list")
def accept_list():
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='accept' ORDER BY `pyment`.`pid` DESC"
    res = select(qry)
    return render_template("maneger/accept_list.html", val=res)


@ app.route("/memo_page")
def memo_page():
    return render_template("admin/memo.html")


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


@ app.route("/Get_memo_page", methods=['GET', 'POST'])
def Get_memo_page():
    upload_file = request.files['files']
    file_name = upload_file.filename
    Discription = request.form['Discription']
    upload_file.save(upload_file.filename)
    file = convertToBinaryData(upload_file.filename)
    qry = "INSERT INTO `memo` VALUES(NULL,%s,%s,%s)"
    val = (Discription, file, file_name)
    iud(qry, val)
    return '''<script>alert("Memo Add Successfully");window.location="/memo_page"</script>'''


@ app.route("/memo_list")
def memo_list():
    qry = "Select * From memo ORDER BY `memoid` DESC"
    res = select(qry)
    return render_template("admin/Memo_List.html", val=res)


@ app.route("/Delete_memo")
def Delete_memo():
    id = request.args.get('id')
    qry = "DELETE FROM `memo` WHERE `memoid`=%s"
    res = iud(qry, id)
    return '''<script>alert("Delete Succussfull");window.location="/memo_list"</script>'''


def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def Remove(filename):
    time.sleep(3)
    os.remove(filename)


@app.route("/download_file")
def download_file():
    id = request.args.get('id')
    qry = "select * from memo WHERE `memoid`=%s"
    res = selectone(qry, id)
    print("Id = ", res[0], )
    print("discription = ", res[1])
    file = res[2]
    filename = res[3]
    write_file(file, filename)
    return send_file(filename,
                     attachment_filename=filename,
                     as_attachment=True)
                     


@ app.route("/memo_list_employee")
def memo_list_employee():
    qry = "Select * From memo ORDER BY `memoid` DESC"
    res = select(qry)
    return render_template("employee/Memo_List.html", val=res)


if __name__ == "__main__":
    app.run(debug=True)
