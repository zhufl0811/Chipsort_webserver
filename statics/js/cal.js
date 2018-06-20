function get_sumdays(year, month){
    var d = new Date(year, month+1, 0);
    return d.getDate();
}

function get_days_before_sat(year,month) {
    var first_day = new Date(year,month,1);
    var days_before_sat = Number(first_day.getDay());
    return days_before_sat
}

function createcell(date,weekday,year,month,start_date,end_date) {
    var today_date=new Date(year,month,date);
    if(start_date<=today_date&today_date<=end_date){
        var left_content = String(date)+"</div><div class='cal_right_cell'>";
        if(weekday==0||weekday==6){
            var startstr= "<td><div class='cal_cell'><div class='cal_left_cell_weekend'>";
            var right_content="<div class='cal_radio'><input type='radio' class='ui checkbox' value=1 name="+year+'-'+String(month+1)+'-'+date+">"+"<label onclick='easychose(this)'>上班</label>"+"</div><div class='cal_radio'>"+
                "<input type='radio' value=0 class='ui checkbox' checked='checked' name="+year+'-'+String(month+1)+'-'+date+">"+"<label onclick='easychose(this)'>休假</label>"+"</div><div class='cal_radio'>"+
                "<input type='radio' value=2 class='ui checkbox' name="+year+'-'+String(month+1)+'-'+date+">"+"<label onclick=\'easychose(this)\'>法定</label></div>"
        }
        else{
            var startstr= "<td><div class='cal_cell'><div class='cal_left_cell'>";
            var right_content="<div class='cal_radio'><input type='radio' class='ui checkbox' checked='checked' value=1 name="+year+'-'+String(month+1)+'-'+date+">"+"<label onclick='easychose(this)'>上班</label></div><div class='cal_radio'>"+
                "<input type='radio' value=0 class='ui checkbox' name="+year+'-'+String(month+1)+'-'+date+">"+"<label onclick='easychose(this)'>休假</label>"+"</div><div class='cal_radio'>"+
                "<input type='radio' value=2 class='ui checkbox' name="+year+'-'+String(month+1)+'-'+date+">"+"<label onclick='easychose(this)'>法定</label></div>"
        }
        var endstr = "</div></div></td>";
        var content = startstr+left_content+right_content+endstr;
        return content
    }
    else{
        var startstr= "<td><div class='cal_cell_readonly'><div class='cal_left_cell_outrange'>";
        var left_content = String(date)+"</div><div class='cal_right_cell_outrange'>";
        if(weekday==0||weekday==6){
            var right_content="<ul>上班</ul>" +
                "<ul style='text-decoration-line: underline'>休假</ul>" +
                "<ul>法定</ul>"
        }
        else{
            var right_content="<div><ul style='text-decoration-line: underline'>上班</ul>" +
                "<ul>休假</ul><ul>法定</ul></div>"
        }
        var endstr = "</div></div></td>";
        var content = startstr+left_content+right_content+endstr;
        return content
    }

}

function create_month_cal(year,month,place,start_date,end_date) {
    var sumdays = get_sumdays(year,month);
    var days_before_sat = get_days_before_sat(year,month);
    var table_one_month_cal = document.createElement('table');
    table_one_month_cal.width='100%';
    var table_content='<tr><td colspan="7"><div style="font-size: 30px;font-weight: bold;margin-bottom:20px;margin-top:20px;text-align:center">'
        +String(year)+'&nbsp年&nbsp'+String(month+1)+'&nbsp月&nbsp'+'</div></td></tr>';
    table_content+='<tr align="center"><td class="negative head_text">日</td><td class="negative head_text">一</td>' +
        '<td class="negative head_text">二</td><td class="negative head_text">三</td>' +
        '<td class="negative head_text">四</td><td class="negative head_text">五</td>' +
        '<td class="negative head_text">六</td></tr>';
    if(days_before_sat==0){
        var rows=Math.ceil((days_before_sat+sumdays)/7);
        var day_in_month=1;
        for(var i=0;i<rows;i++){
            for(var j=0;j<7;j++){
                if(day_in_month<=sumdays){
                    table_content+=createcell(day_in_month,j,year,month,start_date,end_date);
                    day_in_month++
                }
                else{
                    table_content+="<td></td>";
                    day_in_month++
                }
            }
            table_content="<tr>"+table_content+"</tr>";
        }
    }
    else{
        for(var i=0;i<days_before_sat;i++){
            table_content+="<td></td>";
        }
        var flag = i;
        for(var i=0;i<=6-flag;i++){
            table_content+=createcell(i+1,flag+i,year,month,start_date,end_date);
        }
        var flag1 = i+1;
        table_content="<tr>"+table_content+"</tr>";
        var rows=Math.ceil((days_before_sat+sumdays)/7-1);
        var day_in_month=flag1;
        for(var i=0;i<rows;i++){
            for(var j=0;j<7;j++){
                if(day_in_month<=sumdays){
                    table_content+=createcell(day_in_month,j,year,month,start_date,end_date);
                    day_in_month++
                }
                else{
                    table_content+="<td></td>";
                }
            }
            table_content="<tr>"+table_content+"</tr>";
        }
    }

    table_one_month_cal.innerHTML=table_content;
    place.appendChild(table_one_month_cal)
}

function create_cal(mouth_display,start_date,end_date) {
    var form_workday = document.getElementById('workday');
    form_workday.innerHTML='';
    for(var key in mouth_display){
        for(var i=0;i<mouth_display[key].length;i++){
            create_month_cal(key,mouth_display[key][i],form_workday,start_date,end_date)
        }
    }
    var button_submit=document.createElement("div");
    button_submit.innerHTML="<div style='margin-bottom: 100px;text-align: center;margin-top: 20px'>" +
        "<input type='button' onclick='submit_all()' value='提交' class='ui green large button'></div>";
    form_workday.appendChild(button_submit)
}

function date_selected() {
    var start_date_get = document.getElementById('start_date').value;
    var start_date_number = Date.parse(start_date_get.replace(/-/g,'/'));
    start_date = new Date(start_date_number);
    var end_date_get = document.getElementById('end_date').value;
    var end_date_number = Date.parse(end_date_get.replace(/-/g,'/'));
    end_date = new Date(end_date_number);
    if (end_date_number<start_date_number){
        alert('开始日期必须小于结束日期，请重新选择');
        return;
    }
    var mouth_display = new Array();
    if (start_date.getFullYear()!=end_date.getFullYear()){
        var startyear_mouth=new Array();
        for(var startmouth=start_date.getMonth();startmouth<12;startmouth++){
            startyear_mouth[startyear_mouth.length]=Number(startmouth);
        }
        var endyear_mouth=new Array();
        for(var i=0;i<=end_date.getMonth();i++){
            endyear_mouth[endyear_mouth.length]=i;
        }
        mouth_display[start_date.getFullYear()]=startyear_mouth;
        mouth_display[end_date.getFullYear()]=endyear_mouth;
    }
    else{
        var mouth_this_year=new Array();
        for(var startmouth=start_date.getMonth();startmouth<=end_date.getMonth();startmouth++){
            mouth_this_year[mouth_this_year.length]=Number(startmouth);
        }
        mouth_display[start_date.getFullYear()]=mouth_this_year;
    }

    create_cal(mouth_display,start_date,end_date);
}

function submit_all() {
    start_date = document.getElementById('start_date');
    end_date = document.getElementById('end_date');
    all = document.getElementById('workday');
    all.appendChild(start_date);
    all.appendChild(end_date);
    all.submit()
}

function shortcut(month_selected) {
    var mouth_display = new Array();
    var myDate = new Date();
    var this_year = myDate.getFullYear();
    var month_tobe_show = myDate.getMonth()+Number(month_selected);
    var sumdays=get_sumdays(this_year,month_tobe_show);
    var month_list=new Array();
    month_list[0]=month_tobe_show;
    mouth_display[this_year]=month_list;
    var start_date = new Date(this_year,month_tobe_show,1);
    var end_date = new Date(this_year,month_tobe_show,sumdays);
    if (String(Number(month_tobe_show)+1).length!=2){
        document.getElementById('start_date').value=this_year+'-'+'0'+String(Number(month_tobe_show)+1)+'-'+'01';
        document.getElementById('end_date').value=this_year+'-'+'0'+String(Number(month_tobe_show)+1)+'-'+sumdays;
    }
    else{
        document.getElementById('start_date').value=this_year+'-'+String(Number(month_tobe_show)+1)+'-'+'01';
        document.getElementById('end_date').value=this_year+'-'+String(Number(month_tobe_show)+1)+'-'+sumdays;
    }

    create_cal(mouth_display,start_date,end_date);
}
