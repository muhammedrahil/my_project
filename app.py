from flask import *


app = Flask(__name__)
app.secret_key = "key"

from dbconnection import *


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
        return '''<script>alert("login successfull");window.location="/admins"</script>'''
    elif result[3] == "employee":
        return '''<script>alert("login successfull");window.location="/employee"</script>'''
    else:
        return '''<script>alert("invalid");window.location="/"</script>'''


@app.route("/logout")
def logout():
    return redirect('/')


@app.route("/admins")
def admins():
    return render_template("admin/admins.html")



@app.route("/addEmployee")
def addEmployee():
    return render_template("admin/addEmployee.html")

@app.route("/GetaddEmployee" ,methods=['post'])
def GetaddEmployee():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    logqry = "INSERT INTO login VALUES (NULL,%s,%s,'employee')"
    logval=(ename,ecode)
    lid=iud(logqry,logval)
    qry="INSERT INTO `employee` VALUES (NULL,%s,%s,%s,%s)"
    val=(ename,ecode,branch,str(lid))
    iud(qry,val)
    return '''<script>alert("added successfully");window.location="/admins"</script>'''

@app.route("/ViewEmployee")
def ViewEmployee():
    qry="SELECT * FROM `employee`"
    res =select(qry)
    return render_template("admin/viewEmployee.html", val=res)

@app.route("/DeleteEmployee")
def DeleteEmployee():
    id=request.args.get('id')
    qry="DELETE FROM `employee` WHERE `loginid`=%s "
    iud(qry,id)
    return '''<script>alert("delete succussfull");window.location="/ViewEmployee"</script>'''



@app.route("/employee")
def employee():
    return render_template("employee/employee.html")



@app.route("/SearchEmployee")
def SearchEmployee():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/SearchEmployye.html",val=res)

@app.route("/getvalSearchEmployee",methods=['post'])
def getvalSearchEmployee():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    qry="SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s"
    val=(ename,ecode,branch)
    result=selectone(qry,val)
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

@app.route("/GetLeaveRequest",methods=['post'])
def GetLeaveRequest():
    LRid=session['eid']
    reason = request.form['reason']
    date = request.form['date']
    expdate = request.form['expdate']
    print(reason)
    if(reason=='others'):
        reason=request.form['discription']
    qry = "INSERT INTO `leaverequest` VALUES (NULL,%s,'pending',%s,%s,%s)"
    val = (reason,LRid,date,expdate)
    iud(qry, val)
    return '''<script>alert("leave reaquest succussfull");window.location="/employee"</script>'''

@app.route("/ViewReaqusetEmployee")
def ViewReaqusetEmployee():
    qry="SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `employee`.`emp_id`=`leaverequest`.`emp_id` WHERE `leaverequest`.`status`='pending'"
    res =select(qry)
    return render_template("admin/viewLeaveRequest.html", val=res)

@app.route("/AcceptReaqusetEmployee")
def AcceptReaqusetEmployee():
    accept = "accept"
    id = request.args.get('id')
    session['id'] = id
    qry="update`leaverequest` set `status`=%s WHERE LRid =%s"
    val = (accept, session['id'])
    iud(qry,val)
    return '''<script>alert("accept successfully");window.location="/ViewReaqusetEmployee"</script>'''

@app.route("/rejectReaqusetEmployee")
def rejectReaqusetEmployee():
    reject = "reject"
    id = request.args.get('id')
    session['id'] = id
    qry="update`leaverequest` set `status`=%s WHERE LRid =%s"
    val = (reject, session['id'])
    iud(qry,val)
    return '''<script>alert("reject successfully");window.location="/ViewReaqusetEmployee"</script>'''





@app.route("/SetEmployeestarget")
def SetEmployeestarget():
    qry = "SELECT `login`.*,`employee`.* FROM `login`JOIN`employee`ON`login`.`loginid`=`employee`.`loginid`"
    res = select(qry)
    return render_template("admin/setTarget.html",val=res )

@app.route("/SettargetEmployees")
def SettargetEmployees():
    id = request.args.get('id')
    session['id'] = id
    qry = "SELECT * FROM `employee` WHERE emp_id=%s"
    res = selectone(qry,id)
    return render_template("admin/target.html",val=res )

@app.route("/GettargetEmployees",methods=['post'])
def GettargetEmployees():
    number = request.form['number']
    qry="INSERT INTO `target` VALUES (NULL,%s,%s)"
    val=(number,session['id'])
    iud(qry,val)
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
    qry = "SELECT `employee`.*,`target`.* FROM `target` JOIN `employee` ON `employee`.`emp_id`=`target`.`emp_id`where employee.emp_id=%s "
    res = selectone(qry,id)
    return render_template("admin/updateTarget.html",val=res )

@app.route("/GetupdatetargetEmployees",methods=['post'])
def GetupdatetargetEmployees():
    number = request.form['number']
    qry = "update target set target=%s WHERE trid =%s"
    val=(number,session['tid'])
    iud(qry,val)
    return '''<script>alert("Target successfully Set");window.location="/viewupdatetargetEmployees"</script>'''


@app.route("/SearchTargetEmployeeView")
def SearchTargetEmployeeView():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/SearchTargetEmployeeView.html",val=res )

@app.route("/getvalTargetSearchEmployee",methods=['post'])
def getvalTargetSearchEmployee():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    qry="SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s"
    val=(ename,ecode,branch)
    result=selectone(qry,val)
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
    res = selectone(qry,session['rid'] )
    return render_template("employee/ViewEmployeeTargetList.html",val=res )

@app.route("/ViewLeaveRequestPage")
def ViewLeaveRequestPage():
    qry = "SELECT * FROM `employee`"
    res = select(qry)
    return render_template("employee/ViewLeaveRequest.html",val=res )

@app.route("/GetViewLeaveRequestPage",methods=['post'])
def GetViewLeaveRequestPage():
    ename = request.form['ename']
    ecode = request.form['ecode']
    branch = request.form['branch']
    qry="SELECT `employee`.*,`login`.* FROM `login` JOIN `employee` ON `employee`.`loginid`=`login`.`loginid` WHERE `employee`.`emp_name`=%s AND `employee`.`e-code`=%s AND `employee`.`branch`=%s"
    val=(ename,ecode,branch)
    result=selectone(qry,val)
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
    return render_template("employee/viewLeaveRequestPage.html",val=res )

@app.route("/StatusviewLeaveRequest")
def StatusviewLeaveRequest():
    id = request.args.get('id')
    qry = "SELECT `employee`.*,`leaverequest`.* FROM `leaverequest` JOIN `employee` ON `leaverequest`.`LRid`=%s WHERE `leaverequest`.`status`='accept' OR `leaverequest`.`status`='reject'"
    res = selectone(qry, id)
    return render_template("employee/ViewEmployeeLeaveList.html",val=res )


if __name__ == "__main__":
    app.run(debug=True)
