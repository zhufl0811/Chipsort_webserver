var all=new Vue({
    el:'#all',
    data:{
        tooday:'',
        init_get_info:'',
        query_info:{
            group_selected:'',
            date:''
        },
        group_type_info:'',
        overtime_query_info:{'unaudited':[],'audited':[]},
        overtime_sub_info:{}
    },
    created:function () {
        this.get_info();
        this.tooday=this.dateToString(new Date())
    },
    methods:{
        get_info:function () {
            let mv=this;
            $.ajax({
                url:'/attendance/overtime_submit',
                type:'get',
                dataType:'JSON',
                success:function (data) {
                    mv.init_get_info=data;
                    mv.query_info.group_selected=data.group[0];
                }
            })
        },
        dateToString: function(date){
          var year = date.getFullYear();
          var month =(date.getMonth() + 1).toString();
          var day = (date.getDate()).toString();
          if (month.length === 1) {
              month = "0" + month;
          }
          if (day.length === 1) {
              day = "0" + day;
          }
          var dateTime = year + "-" + month + "-" + day;
          return dateTime;
        },
        sub_query:function () {
            let mv=this;
            if(mv.query_info.date){
                $.ajax({
                url:'/attendance/overtime_submit',
                type:'post',
                dataType:'JSON',
                data:JSON.stringify(mv.query_info),
                success:function (data) {
                    mv.group_type_info=data.group_type_info;
                    mv.overtime_query_info.unaudited=data.overtime_info.unaudited;
                    mv.overtime_query_info.audited=data.overtime_info.audited;
                    for(group in mv.group_type_info){
                        for(type in mv.group_type_info[group]){
                            mv.overtime_sub_info[group+'_'+type]={'start_time_hour':'','start_time_min':'','end_time_hour':'',
                                'end_time_min':'','ids':[],kind:'kind1','date':mv.query_info.date}
                        }
                    }
                }
            })
            }else{
                alert('请输入日期');
                return
            }
        },
        easy_query:function (e) {
            let mv=this;
            var tooday=new Date();
            var thisyear=tooday.getFullYear();
            var thismonth = tooday.getMonth();
            var thisdate = tooday.getDate();
            if($(e.target).context.textContent==='选定昨天'){
                var set_date=new Date(thisyear,thismonth,thisdate-1);
                mv.query_info.date=mv.dateToString(set_date);
            }else if($(e.target).context.textContent==='选定今天'){
                var set_date=tooday;
                mv.query_info.date=mv.dateToString(set_date);
            }else{
                var set_date=new Date(thisyear,thismonth,thisdate-2);
                mv.query_info.date=mv.dateToString(set_date);
            }
            mv.sub_query()
        },
        select_group_type:function (e) {
            var group=$(e.target).attr('name').substr(0,5);
            var type=$(e.target).attr('name').substr(6,2);
            for(var i=0;i<this.group_type_info[group][type].length;i++){
                $(e.target).parent().parent().next().find("input[id="+this.group_type_info[group][type][i]+']').click()
            }
        },
        sub_overtime_info:function (e) {
            var group_type=$(e.target).attr('name');
            var sub_data=this.overtime_sub_info[group_type];
            if(sub_data['start_time_hour']&&sub_data['end_time_min']&&sub_data['end_time_hour']&&sub_data['end_time_min']){
                if(sub_data['kind']){
                    if(sub_data['ids'].length!=0){
                        var work_min=60*(Number(sub_data['end_time_hour'])-Number(sub_data['start_time_hour']))+
                            Number(sub_data['end_time_min'])-Number(sub_data['start_time_min']);
                        if(work_min===0){
                            alert('开始时间不能等于结束时间')
                        }else if(work_min<0){
                            if(sub_data['kind']!=='kind2'){
                                alert('kind1的开始时间不能大于结束时间');
                                return
                            }
                        }
                    }else{
                        alert('请至少选择一名员工');
                        return
                    }
                }else{
                    alert('请选择加班种类');
                    return
                }
            }else{
                alert('请填写完整的时间');
                return
            }
            var confirm_info="您本次提报的人员：";
            for (var i=0;i<sub_data['ids'].length;i++){
                confirm_info=confirm_info+this.init_get_info.id_name[sub_data['ids'][i]]+';'
            }
            confirm_info=confirm_info+"\n提报的小时数为:";
            if(((sub_data['end_time_hour']-sub_data['start_time_hour'])*60+sub_data['end_time_min']-sub_data['start_time_min'])>0){
                var hours=sub_data['end_time_hour']-sub_data['start_time_hour']+(sub_data['end_time_min']-sub_data['start_time_min'])/60
            }else{
                var hours=sub_data['end_time_hour']-sub_data['start_time_hour']+(sub_data['end_time_min']-sub_data['start_time_min'])/60+24
            }
            confirm_info=confirm_info+String(hours)+"\n是否确认";
            if(!confirm(confirm_info)){
                return
            }
            sub_data['group_type']=group_type;
            let mv=this;
            $.ajax({
                url:'/attendance/overtime_submit',
                type:'post',
                dataType:'JSON',
                data:JSON.stringify(mv.overtime_sub_info[group_type]),
                success:function (data) {
                    alert('提报成功');
                    mv.sub_query()
                }
            })
        }
    }
})