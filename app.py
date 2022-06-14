
from fileinput import filename
from dbconnection import *
from flask import *
import functools
from datetime import datetime
import time
import os
import pytz
app = Flask(__name__)
app.secret_key = "key"


def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return redirect("/")
        return func()
    return secure_function


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
        return '''<script>alert ("Invalid UserName OR Password");window.location="/"</script>'''
    elif result[3] == 'DIRECTOR':
        session['lid'] = 'director'

        if result[1] == 'PMNDIR':
            session['branch'] = 'Perinthalmanna'
        elif result[1] == 'RMKDIR':
            session['branch'] = 'Ramanatukara'
        elif result[1] == 'PTBDIR':
            session['branch'] = 'Pattambi'
        elif result[1] == 'VLCDIR':
            session['branch'] = 'Valanchery'

        return '''<script>alert("Director Login Successfull");window.location="/admins"</script>'''
    elif result[3] == 'MANAGER':
        session['lid'] = 'manager'

        if result[1] == 'PMNMNGR':
            session['branch'] = 'Perinthalmanna'
        elif result[1] == 'RMKMNGR':
            session['branch'] = 'Ramanatukara'
        elif result[1] == 'PTBMNGR':
            session['branch'] = 'Pattambi'
        elif result[1] == 'VLCMNGR':
            session['branch'] = 'Valanchery'

        return '''<script>alert("Manager Login Successfull");window.location="/admins"</script>'''
    elif result[3] == "EMPLOYEES":
        session['lid'] = 'employees'

        if result[1] == 'PMNEMP':
            session['EmpBranch'] = 'Perinthalmanna'
        elif result[1] == 'RMKEMP':
            session['EmpBranch'] = 'Ramanatukara'
        elif result[1] == 'PTBEMP':
            session['EmpBranch'] = 'Pattambi'
        elif result[1] == 'VLCEMP':
            session['EmpBranch'] = 'Valanchery'

        return '''<script>alert("Login Successfull");window.location="/employeepage"</script>'''
    elif result[3] == "COO":
        session['lid'] = 'coo'
        return '''<script>alert("Coo Login Successfull");window.location="/home_coo"</script>'''
    else:
        return '''<script>alert("invalid");window.location="/"</script>'''


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect('/')


# director and Manager modules codes ................#######################################...........................


# director and Manager home page start ..................########################################

@app.route("/admins")
@login_required
def admins():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        return render_template("admin/home.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

# director and Manager home page end..................########################################


# employee add manger and director start..................########################################


@app.route("/addEmployee")
@login_required
def addEmployee():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        return render_template("admin/addEmployee.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@app.route("/GetaddEmployee", methods=['post'])
@login_required
def GetaddEmployee():
    ename = request.form['ename']
    ecode = request.form['ecode']
    Department = request.form['Department']
    branch = session['branch']
    logqry = "INSERT INTO login VALUES (NULL,%s,%s,'employee')"
    logval = (ename, ecode)
    lid = iud(logqry, logval)
    qry = "INSERT INTO `employee` VALUES (NULL,%s,%s,%s,%s,%s)"
    val = (ename, ecode, branch, str(lid), Department)
    iud(qry, val)
    return '''<script>alert("New Employee Added Successfully");window.location="/addEmployee"</script>'''


# employee add manger and director end..................########################################


# employee view manger and director start..................########################################

@app.route("/ViewEmployee")
@login_required
def ViewEmployee():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        qry = "SELECT * FROM `employee` WHERE `branch` =%s ORDER BY emp_id DESC"
        res = selectall(qry, session['branch'])
        return render_template("admin/viewEmployee.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


# employee delete manger and director ..................

@app.route("/DeleteEmployee")
@login_required
def DeleteEmployee():
    id = request.args.get('id')
    qry = "DELETE employee ,login FROM `employee` join login on employee.loginid = login.loginid WHERE login.`loginid`=%s "
    iud(qry, id)
    return '''<script>window.location="/ViewEmployee"</script>'''


# search employee view manger and director..................

@app.route("/Search_department", methods=['post'])
@login_required
def Search_branch():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        department = request.form['department']
        qry = "SELECT * FROM `employee` WHERE `department`=%s AND branch=%s     ORDER BY `employee`.`emp_id` DESC"
        val=(department,session['branch'])
        res = selectall(qry, val)
        return render_template("admin/SearchViewEmployee.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


# employee view manger and director end..................########################################


#  employee leave request view manger and director start..................########################################


# view leave request...................................

@ app.route("/ViewReaqusetEmployee")
@login_required
def ViewReaqusetEmployee():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='pending' AND `branch`=%s ORDER BY `leaverequest`.`LRid` DESC"
        res = selectall(qry, session['branch'])
        return render_template("admin/viewLeaveRequest.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

# search leave request employee branch............................


@ app.route("/Search_branch_Leave", methods=['post'])
@login_required
def Search_branch_Leave():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        department = request.form['department']
        qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='pending' AND `employee`.`department`=%s AND employee.branch=%s ORDER BY `leaverequest`.`LRid` DESC"
        val = (department, session['branch'])
        res = selectall(qry, val)
        return render_template("admin/Search_branch_Leave.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


# search branch ways accepted list display...............................

@ app.route("/Search_branch_Leave_accepted", methods=['post'])
@login_required
def Search_branch_Leave_accepted():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        department = request.form['department']
        qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='Accepted' AND `employee`.`department`=%s AND `employee`.`branch`=%sORDER BY `leaverequest`.`LRid` DESC"
        val = (department, session['branch'])
        res = selectall(qry, val)
        return render_template("admin/accept_list.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

# accept list page search branch accepet lists..............................


@ app.route("/accept_list_leave")
@login_required
def accept_list_leave():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='Accepted' AND `employee`.`branch`=%s  ORDER BY `leaverequest`.`LRid` DESC"
        res = selectall(qry, session['branch'])
        return render_template("admin/accept_list.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


# leave request accepted  .............................................

@ app.route("/AcceptReaqusetEmployee")
@login_required
def AcceptReaqusetEmployee():
    accept = "Accepted"
    id = request.args.get('id')
    session['id'] = id
    qry = "update`leaverequest` set `status`=%s WHERE LRid =%s"
    val = (accept, session['id'])
    iud(qry, val)
    return '''<script>window.location="/ViewReaqusetEmployee"</script>'''


# leave requested Rejected................................

@ app.route("/rejectReaqusetEmployee")
@login_required
def rejectReaqusetEmployee():
    reject = "Rejected"
    id = request.args.get('id')
    session['id'] = id
    qry = "update`leaverequest` set `status`=%s WHERE LRid =%s"
    val = (reject, session['id'])
    iud(qry, val)
    return '''<script>window.location="/ViewReaqusetEmployee"</script>'''

# date filter code......................................................


@ app.route("/datefilter", methods=['post'])
@login_required
def datefilter():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        date = request.form['date']
        query = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='Accepted' AND `employee`.`branch`=%s  AND DATE(`leaverequest`.`date`)=%s ORDER BY `leaverequest`.`LRid` DESC"
        val = (session['branch'], date)
        res = selectall(query, val)
        return render_template("admin/accept_list.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''
#  employee leave request view manger and director end..................########################################


#  employee set target manger and director start..................########################################

# view set target list page ................................................

@ app.route("/SetEmployeestarget")
@login_required
def SetEmployeestarget():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        qry = "SELECT `login`.*,`employee`.* FROM `login`JOIN`employee`ON`login`.`loginid`=`employee`.`loginid` WHERE `employee`.`branch`=%s ORDER BY `employee`.`emp_id` DESC"
        res = selectall(qry, session['branch'])
        return render_template("admin/setTarget.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

# search targrt branch ways................................................


@ app.route("/Search_branch_SetTarget", methods=['post'])
@login_required
def Search_branch_SetTarget():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        department = request.form['department']
        qry = "SELECT `login`.*,`employee`.* FROM `login`JOIN`employee`ON`login`.`loginid`=`employee`.`loginid` WHERE `employee`.`department`=%s AND `employee`.`branch`=%s ORDER BY `employee`.`emp_id` DESC"
        val=(department,session['branch'])
        res = selectall(qry, val)
        return render_template("admin/Search_branch_SetTarget.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


# set taget button goto page...........................................

@ app.route("/SettargetEmployees")
@login_required
def SettargetEmployees():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        id = request.args.get('id')
        session['id'] = id
        qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`loginid`=`target`.`lg_id` WHERE `employee`.`loginid`=%s"
        res = selectone(qry, id)
        qry1 = "SELECT `employee`.`emp_name` FROM `employee` JOIN `login` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`branch`='Ramanatukara' AND `employee`.`loginid`=%s"
        res1 = selectone(qry1, id)
        print(res1)
        if(res == None):
            return render_template("admin/target.html", val=res1)
        else:
            return '''<script>alert("already set, Please update employee target");window.location="/viewupdatetargetEmployees"</script>'''
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

# set target.....................................................


@ app.route("/GettargetEmployees", methods=['post'])
@login_required
def GettargetEmployees():
    Gold = request.form['Gold']
    Diamond = request.form['Diamond']
    qry = "INSERT INTO `target` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s)"
    val = (Gold, session['id'], 00, Diamond, 00, 00, 00)
    iud(qry, val)
    return '''<script>window.location="/SetEmployeestarget"</script>'''


#  employee set target manger and director end..................########################################


#  employee update target manger and director start..................########################################

# view update target list page................................................

@ app.route("/viewupdatetargetEmployees")
@login_required
def viewupdatetargetEmployees():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` WHERE `employee`.`branch`=%s ORDER BY `target`.`trid` DESC"
        res = selectall(qry, session['branch'])
        return render_template("admin/ViewtargetEmp.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

#  Search branch......................................


@ app.route("/Search_viewupdatetargetEmployees", methods=['post'])
@login_required
def Search_viewupdatetargetEmployees():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        department = request.form['department']
        qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id`  WHERE `employee`.`department`=%s AND employee.branch=%s ORDER BY `employee`.`emp_id` DESC"
        val=(department,session['branch'])
        res = selectall(qry,val)
        return render_template("admin/Search_viewupdatetargetEmployees.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/updateEmployeestarget")
@login_required
def updateEmployeestarget():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        id = request.args.get('id')
        session['tid'] = id
        qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` where `target`. `trid`=%s "
        res = selectone(qry, id)
        return render_template("admin/updateTarget.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/GetupdatetargetEmployees", methods=['post'])
@login_required
def GetupdatetargetEmployees():
    Gold = request.form['Gold']
    Diamond = request.form['Diamond']
    qry = "UPDATE `target` SET `gold`=%s ,`Diamond`=%s,`achive_gold`='0',`achive_diamond`='0',`gold_achive_pers`='0',`dmn__achive_perse`='0' WHERE trid =%s"
    val = (Gold, Diamond, session['tid'])
    iud(qry, val)
    return '''<script>window.location="/viewupdatetargetEmployees"</script>'''


@ app.route("/AchiveEmployeestarget")
@login_required
def AchiveEmployeestarget():
    if(session['lid'] == 'manager' or session['lid'] == 'director'):
        id = request.args.get('id')
        session['tid'] = id
        qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` where `target`. `trid`=%s "
        res = selectone(qry, id)
        return render_template("admin/Achive.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/GetAchiveEmployeestarget", methods=['post'])
@login_required
def GetAchiveEmployeestarget():
    Gold = request.form['Gold']
    Diamond = request.form['Diamond']
    qry1 = "SELECT * FROM `target` WHERE `trid` =%s"
    res = selectone(qry1, session['tid'])
    cur_gold = res[1]
    achive_gold = res[3]
    cur_dimond = res[4]
    achive_dimond = res[5]
    gold_totel_achive = float(achive_gold)+float(Gold)
    Diamond_totel_achive = float(achive_dimond)+float(Diamond)
    perse_gold_totel_achive = (gold_totel_achive / float(cur_gold)) * 100
    roundNogold=round(perse_gold_totel_achive,2)
    perse_Diamond_totel_achive = (
        Diamond_totel_achive / float(cur_dimond)) * 100
    roundNodimond=round(perse_Diamond_totel_achive,2)
    qry = "UPDATE target SET `achive_gold`=%s,`achive_diamond`=%s ,`gold_achive_pers`=%s ,`dmn__achive_perse`=%s WHERE trid =%s"
    val = (gold_totel_achive, Diamond_totel_achive,
           roundNogold,roundNodimond, session['tid'])
    iud(qry, val)
    return '''<script>window.location="/viewupdatetargetEmployees"</script>'''


#  employee update target manger and director end..................########################################


# memo page display and download_file start ...............############################################

@ app.route("/memo_page")
@login_required
def memo_page():
    return render_template("admin/memo.html")


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


@ app.route("/Get_memo_page", methods=['GET', 'POST'])
@login_required
def Get_memo_page():
    upload_file = request.files['files']
    file_name = upload_file.filename
    Discription = request.form['Discription']
    upload_file.save(upload_file.filename)
    file = convertToBinaryData(upload_file.filename)
    qry = "INSERT INTO `memo` VALUES(NULL,%s,%s,%s)"
    val = (Discription, file, file_name)
    iud(qry, val)
    return '''<script>alert("Memo Added Successfully");window.location="/memo_page"</script>'''


@ app.route("/memo_list")
@login_required
def memo_list():
    qry = "Select * From memo ORDER BY `memoid` DESC"
    res = select(qry)
    return render_template("admin/Memo_List.html", val=res)


@ app.route("/Delete_memo")
@login_required
def Delete_memo():
    id = request.args.get('id')
    qry = "DELETE FROM `memo` WHERE `memoid`=%s"
    res = iud(qry, id)
    return '''<script>alert("Deleted Successfully");window.location="/memo_list"</script>'''


def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)


def Remove(filename):
    time.sleep(3)
    os.remove(filename)


@app.route("/download_file")
@login_required
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

# memo page display and download_file end  ...............############################################

# manager urgent leave request start..................................#############################


@ app.route("/manager_leave_Request")
@login_required
def manager_leave_Request():
    if(session['lid'] == 'manager'):
        return render_template("maneger/leaveRequest.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/get_manager_leave_Request", methods=['GET', 'POST'])
@login_required
def get_manager_leave_Request():
    ename = request.form['ename']
    ecode = request.form['ecode']
    department = request.form['department']
    reason = request.form['reason']
    date = request.form['date']
    expdate = request.form['expdate']
    if(reason == 'others'):
        reason = request.form['discription']
    qry = "SELECT `employee`.* FROM `employee`  WHERE `emp_name`=%s AND `e-code`=%s AND `branch`=%s AND department=%s"
    print(qry)
    val = (ename, ecode, session['branch'], department)
    res = selectone(qry, val)
    id = res[4]
    qry1 = "INSERT INTO `leaverequest` VALUES (NULL,%s,'Accepted',%s,%s,%s,CURDATE())"
    val1 = (reason, id, date, expdate)
    iud(qry1, val1)
    return '''<script>alert(" Successfull");window.location="/manager_leave_Request"</script>'''

# manager urgent leave request end..................................#############################


# director only payment page start..................................#############################


@ app.route("/BranchEmployeePymentPage")
@login_required
def BranchEmployeePymentPage():
    if(session['lid'] == 'director'):
        qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='pending' AND `employee`.`branch`=%s ORDER BY `pyment`.`pid` DESC"
        res = selectall(qry, session['branch'])
        return render_template("maneger/viewPymentEmployee.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/Search_branch_Pyment", methods=['post'])
@login_required
def Search_branch_Pyment():
    if(session['lid'] == 'director'):
        department = request.form['department']
        qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='pending' AND `employee`.`department`=%s AND `employee`.`branch`=%s ORDER BY `pyment`.`pid` DESC"
        val = (department, session['branch'])
        res = selectall(qry, val)
        return render_template("maneger/Search_branch_Pyment.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/accept_list")
@login_required
def accept_list():
    qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='Accepted' AND `employee`.`branch`=%s ORDER BY `pyment`.`pid` DESC"
    res = selectall(qry, session['branch'])
    return render_template("maneger/accept_list.html", val=res)


@ app.route("/Search_branch_Pyment_accepted", methods=['post'])
@login_required
def Search_branch_Pyment_accepted():
    if(session['lid'] == 'director'):
        department = request.form['department']
        qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`status`='Accepted' AND `employee`.`department`=%s AND `employee`.`branch`=%s  ORDER BY `pyment`.`pid` DESC"
        val = (department, session['branch'])
        res = selectall(qry, val)
        return render_template("maneger/accept_list.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/AcceptBranchEmployeePymentPage")
@login_required
def AcceptBranchEmployeePymentPage():
    accept = "Accepted"
    id = request.args.get('id')
    qry = "update pyment set `status`=%s WHERE pid =%s"
    val = (accept, id)
    iud(qry, val)
    return '''<script>window.location="/BranchEmployeePymentPage"</script>'''


@ app.route("/rejectBranchEmployeePymentPage")
@login_required
def rejectBranchEmployeePymentPage():
    reject = "Rejected"
    id = request.args.get('id')
    qry = "update pyment set `status`=%s WHERE pid =%s"
    val = (reject, id)
    iud(qry, val)
    return '''<script>window.location="/BranchEmployeePymentPage"</script>'''


@ app.route("/EditBranchEmployeePymentPage")
@login_required
def EditBranchEmployeePymentPage():
    if(session['lid'] == 'director'):
        id = request.args.get('id')
        session['pid'] = id
        qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE`pyment`.`pid`=%s"
        res = selectone(qry, id)
        return render_template("maneger/EditPyment.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/GetEditBranchEmployeePymentPage", methods=['post'])
@login_required
def GetEditBranchEmployeePymentPage():
    money = request.form['number']
    qry = "update pyment set `moneny`=%s WHERE pid =%s"
    val = (money, session['pid'])
    iud(qry, val)
    return '''<script>window.location="/BranchEmployeePymentPage"</script>'''


@ app.route("/StatusviewlistPymentListsmanager")
@login_required
def StatusviewlistPymentListsmanager():
    if(session['lid'] == 'director'):
        id = request.args.get('id')
        qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id`  WHERE `pyment`.`pid`=%s"
        res = selectone(qry, id)
        return render_template("maneger/SearchViewPaymentList.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


# director only payment page end..................................#############################


# coo modules start..................................################################################

@ app.route("/home_coo")
@login_required
def home_coo():
    if(session['lid'] == 'coo'):
        return render_template("coo/home.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''



@ app.route("/accept_list_leave_coo")
@login_required
def accept_list_leave_coo():
    if(session['lid'] == 'coo'):
        qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='Accepted'  ORDER BY `leaverequest`.`LRid` DESC"
        res = select(qry)
        return render_template("coo/accept_list.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''



@ app.route("/Search_branch_Leave_coo", methods=['post'])
@login_required
def Search_branch_Leave_coo():
    if(session['lid'] == 'coo'):
        branch = request.form['branch']
        qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE `leaverequest`.`status`='Accepted' AND `employee`.`branch`=%s ORDER BY `leaverequest`.`LRid` DESC"
        res = selectall(qry, branch)
        return render_template("coo/Search_branch_Leave.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/viewupdatetargetEmployees_coo")
@login_required
def viewupdatetargetEmployees_coo():
    if(session['lid'] == 'coo'):
        qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id` ORDER BY `target`.`trid` DESC"
        res = select(qry)
        print(res)
        return render_template("coo/ViewtargetEmp.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/Search_viewupdatetargetEmployees_coo", methods=['post'])
@login_required
def Search_viewupdatetargetEmployees_coo():
    if(session['lid'] == 'coo'):
        branch = request.form['branch']
        qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON employee.`loginid`=`target`.`lg_id`  WHERE `employee`.`branch`=%s ORDER BY `target`.`trid` DESC"
        res = selectall(qry, branch)
        return render_template("coo/Search_viewupdatetargetEmployees.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

# coo modules end..................................################################################


# auto suggection start..................................################################################

@app.route("/ajaxpost", methods=["POST", "GET"])
def ajaxpost():
    if request.method == 'POST':
        queryString = request.form['queryString']
        query = "SELECT emp_name from employee WHERE emp_name LIKE '{}%' LIMIT 10".format(
            queryString)
        employee = select(query)
        employee = list(employee[0])

    return jsonify({'htmlresponse': render_template('employee/response.html', employee=employee)})

# SELECT emp_name from employee WHERE loginid in (SELECT lg_id from leaverequest WHERE date >= '{}%' and expDate <= '{}%')  LIMIT 10".format(
#             date, expdate)AND `leaverequest`.`status`='Accepted' AND `employee`.`branch`=%s



@app.route("/ajaxpost_leave", methods=["POST", "GET"])
def ajaxpost_leave():
    if request.method == 'POST':
        date = request.form['date']
        expdate = request.form['expdate']
        query = "SELECT emp_name FROM employee WHERE `branch`=%s AND loginid IN (SELECT lg_id FROM leaverequest WHERE DATE >=%s AND expDate <=%s )  LIMIT 10"
        val = (session['EmpBranch'], date, expdate)
        employee = selectall(query, val)
        print(employee)
        list_employee = [list(i) for i in employee]
        length = len(list_employee)
        list_final = []
        print(list_employee)
        for i in list_employee:
            for j in i:
                list_final.append(j)
    return jsonify({'htmlresponse': render_template('employee/response.html', employee=list_final)})
# auto suggection end..................................################################################


# employye pages module start......................#################################


@app.route("/employeepage")
@login_required
def employeepage():
    if(session['lid'] == 'employees'):
        return render_template("employee/home.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

# add leave request .....................................


@app.route("/SearchEmployee")
@login_required
def SearchEmployee():
    if(session['lid'] == 'employees'):
        qry = "SELECT * FROM `employee`"
        res = select(qry)
        return render_template("employee/SearchEmployye.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@app.route("/getvalSearchEmployee", methods=['post'])
@login_required
def getvalSearchEmployee():
    ename = request.form['ename']
    ecode = request.form['ecode']
    department = request.form['department']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s AND `employee`.`department`=%s"
    val = (ename, ecode, session['EmpBranch'], department)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("Invalid ");window.location="/SearchEmployee"</script>'''
    elif result[9] == "employee":
        session['eid'] = result[4]
        return '''<script>alert("Thank you! Please Request Your Leave");window.location="/leaveRequestPage"</script>'''
    else:
        return '''<script>alert("invalid ");window.location="/SearchEmployee"</script>'''


@app.route("/leaveRequestPage")
@login_required
def leaveRequestPage():
    if(session['lid'] == 'employees'):
        return render_template("employee/leaveRequest.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@app.route("/GetLeaveRequest", methods=['post'])
@login_required
def GetLeaveRequest():
    t = "17:00:00"
    test_time = datetime.strptime(t, '%H:%M:%S')
    country_time_zone = pytz.timezone('Asia/Calcutta')
    country_time = datetime.now(country_time_zone)
    country_time = country_time.strftime("%H:%M:%S")
    current_time = datetime.strptime(country_time, "%H:%M:%S")
    if(test_time.time() > current_time.time()):
        LRid = session['eid']
        reason = request.form['reason']
        date = request.form['date']
        expdate = request.form['expdate']
        if(reason == 'others'):
            reason = request.form['discription']
        qry = "INSERT INTO `leaverequest` VALUES (NULL,%s,'pending',%s,%s,%s,CURDATE())"
        val = (reason, LRid, date, expdate)
        iud(qry, val)
        return '''<script>alert("leave request successfull");window.location="/employeepage"</script>'''
    else:
        return '''<script>alert("Not Approved");window.location="/employeepage"</script>'''

 # search target page list status ...............................


@ app.route("/SearchTargetEmployeeView")
@login_required
def SearchTargetEmployeeView():
    if(session['lid'] == 'employees'):
        return render_template("employee/SearchTargetEmployeeView.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/getvalTargetSearchEmployee", methods=['post'])
@login_required
def getvalTargetSearchEmployee():
    ename = request.form['ename']
    ecode = request.form['ecode']
    department = request.form['department']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s AND `employee`.`department`=%s"
    val = (ename, ecode, session['EmpBranch'], department)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("invalid");window.location="/SearchTargetEmployeeView"</script>'''
    elif result[9] == "employee":
        session['rid'] = result[4]
        return '''<script>alert("Thank you , Please View Your Target And Achived Target ");window.location="/ViewEmployeeTargetList"</script>'''
    else:
        return '''<script>alert("invalid ");window.location="/SearchTargetEmployeeView"</script>'''


@ app.route("/ViewEmployeeTargetList")
@login_required
def ViewEmployeeTargetList():
    if(session['lid'] == 'employees'):
        qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`loginid`=`target`.`lg_id` WHERE `employee`.`loginid`=%s"
        res = selectone(qry, session['rid'])
        return render_template("employee/ViewEmployeeTargetList.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


# search leave request status......................................


@ app.route("/ViewLeaveRequest_statusPages")
@login_required
def ViewLeaveRequest_statusPages():
    if(session['lid'] == 'employees'):
        return render_template("employee/ViewLeaveRequest.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/GetViewLeaveRequestPage", methods=['post'])
@login_required
def GetViewLeaveRequestPage():
    ename = request.form['ename']
    ecode = request.form['ecode']
    department = request.form['department']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s AND `employee`.`department`=%s"
    val = (ename, ecode, session['EmpBranch'], department)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("Invalid");window.location="/ViewLeaveRequest_statusPages"</script>'''
    elif result[9] == "employee":
        session['rlid'] = result[4]
        return '''<script>alert("Thank you, Please View Your Leave Request Status");window.location="/viewLeaveRequestPage"</script>'''
    else:
        return '''<script>alert("invalid ");window.location="/ViewLeaveRequest_statusPages"</script>'''


@ app.route("/viewLeaveRequestPage")
@login_required
def viewLeaveRequestPage():
    if(session['lid'] == 'employees'):
        qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id` WHERE  `employee`.`loginid`= %s  ORDER BY `leaverequest`.`LRid` DESC"
        res = selectall(qry, session['rlid'])
        return render_template("employee/viewLeaveRequestPage.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/RemoveLeaveRequestEmployee")
@login_required
def RemoveLeaveRequestEmployee():
    id = request.args.get('id')
    qry = "DELETE FROM leaverequest WHERE LRid =%s"
    iud(qry, id)
    return '''<script>window.location="/viewLeaveRequestPage"</script>'''

@ app.route("/StatusviewLeaveRequest")
@login_required
def StatusviewLeaveRequest():
    id = request.args.get('id')
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`loginid`=`leaverequest`.`lg_id`WHERE`leaverequest`.`LRid`=%s"
    res = selectone(qry, id)
    return render_template("employee/ViewEmployeeLeaveList.html", val=res)


# search payment pages .....................................

@ app.route("/SearchPymentPage")
@login_required
def SearchPymentPage():
    if(session['lid'] == 'employees'):
        return render_template("employee/SearchPyment.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/GetSearchPymentPage", methods=['post'])
@login_required
def GetSearchPymentPage():
    ename = request.form['ename']
    ecode = request.form['ecode']
    department = request.form['department']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s AND `employee`.`department`=%s"
    val = (ename, ecode, session['EmpBranch'], department)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("Invalid");window.location="/SearchPymentPage"</script>'''
    elif result[9] == "employee":
        session['rid'] = result[4]
        return '''<script>alert("Thank you,Please Request Your Pyment");window.location="/PymentPage"</script>'''
    else:
        return '''<script>alert("Invalid ");window.location="/SearchPymentPage"</script>'''


@ app.route("/PymentPage")
@login_required
def PymentPage():
    if(session['lid'] == 'employees'):
        return render_template("employee/pymentPage.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/GetPymentPage", methods=['post'])
@login_required
def GetPymentPage():
    PymentOption = request.form['PymentOption']
    pyment = request.form['pyment']
    if (PymentOption == "others"):
        PymentOption = request.form['discription']
    qry = "INSERT INTO `pyment` VALUES (NULL,%s,%s,%s,'pending',CURDATE())"
    val = (PymentOption, pyment, session['rid'])
    iud(qry, val)
    return '''<script>alert("Payment Request Succesfully");window.location="/employeepage"</script>'''


# search payment status..........................................


@ app.route("/SearchViewPayment_Status")
@login_required
def SearchViewPayment_Status():
    if(session['lid'] == 'employees'):
        return render_template("employee/SearchViewPayment.html")
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


@ app.route("/GetSearchViewPayment", methods=['post'])
@login_required
def GetSearchViewPayment():
    ename = request.form['ename']
    ecode = request.form['ecode']
    department = request.form['department']
    qry = "SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s AND `employee`.`department`=%s"
    val = (ename, ecode, session['EmpBranch'], department)
    result = selectone(qry, val)
    if result is None:
        return '''<script>alert ("Invalid");window.location="/SearchViewPayment_Status"</script>'''
    elif result[9] == "employee":
        session['rid'] = result[4]
        return '''<script>alert("Thank you, Please View Your Payment Status");window.location="/listPymentListseployee"</script>'''
    else:
        return '''<script>alert("Invalid");window.location="/SearchViewPayment_Status"</script>'''


@ app.route("/listPymentListseployee")
@login_required
def listPymentListseployee():
    if(session['lid'] == 'employees'):
        qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id` WHERE `employee`.`loginid`=%s ORDER BY `pyment`.`pid` DESC"
        res = selectall(qry, session['rid'])
        return render_template("employee/listPymentListseployee.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

@ app.route("/RemovePaymentstatuslist")
@login_required
def RemovePaymentstatuslist():
    if(session['lid'] == 'employees'):
        id = request.args.get('id')
        qry="DELETE FROM pyment WHERE pid=%s"
        iud(qry,id)
        return '''<script>window.location="/listPymentListseployee"</script>'''
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''

@ app.route("/StatusviewlistPymentListseployee")
@login_required
def StatusviewlistPymentListseployee():
    if(session['lid'] == 'employees'):
        id = request.args.get('id')
        qry = "SELECT `employee`.*,`pyment`.* FROM `pyment` JOIN `employee` ON `employee`.`loginid`=`pyment`.`lg_id`  WHERE `pyment`.`pid`=%s"
        res = selectone(qry, id)
        return render_template("employee/SearchViewPaymentList.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


# memo pages ...............................

@ app.route("/memo_list_employee")
@login_required
def memo_list_employee():
    if(session['lid'] == 'employees'):
        qry = "Select * From memo ORDER BY `memoid` DESC"
        res = select(qry)
        return render_template("employee/Memo_List.html", val=res)
    else:
        return '''<script>alert("Unavailable");window.history.back()</script>'''


# employye pages module end......................#################################
if __name__ == "__main__":
    app.run(debug=True)
