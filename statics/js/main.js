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

