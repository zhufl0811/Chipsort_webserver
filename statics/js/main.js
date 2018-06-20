function dopost(URL, PARAMS) {
    var temp = document.createElement("form");
    temp.action = URL;
    temp.method = "post";
    temp.style.display = "none";
    var opt = document.createElement("input");
    opt.name = 'delete';
    opt.value = PARAMS;
    temp.appendChild(opt);
    document.body.appendChild(temp);
    alert_info = '确定要删除'+PARAMS+'吗？';
    if (confirm(alert_info)===true){
        temp.submit();
        return temp;
    }
    else{
        return 0;
    }
}

function easychose(that) {
    $(that).prev().prop('checked','checked');
}

var url_to_name=new Array()
url_to_name['']='首页';
url_to_name['attendance']='考勤首页';
url_to_name['admin']='后台管理';
url_to_name['workday']='工作日设定';
url_to_name['workarrangement.html']='排班';
url_to_name['adduser']='添加用户';
url_to_name['deluser']='删除用户';
url_to_name['edituser']='修改用户';
url_to_name['addrole']='添加角色';
url_to_name['delrole']='删除角色';
url_to_name['editrole']='修改角色';
url_to_name['addper']='添加权限';
url_to_name['editper']='修改权限';
url_to_name['delper']='删除权限';

function navbar() {
    var navdiv = document.getElementById('navbar');
    var url_splited=(window.location.pathname).split('/');
    if(url_splited[1]==''){
        var index_bar=document.createElement('div');
        index_bar.innerHTML="<a href='/' />>首页";
        navdiv.appendChild(index_bar);
    }
    else{
        for(var i=0;i<url_splited.length;i++){
            if(i==0){
                var href_url='/'
            }
            else{
                var href_url='';
                for(var j=1;j<=i;j++){
                    href_url+=('/'+url_splited[j])
                }
            }
            var sub_bar = document.createElement('div');
            sub_bar.innerHTML='<a href='+href_url+' />>'+url_to_name[url_splited[i]];
            navdiv.appendChild(sub_bar)
        }
    }
}
