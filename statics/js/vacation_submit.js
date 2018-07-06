var all=new Vue({
    el:'#all',
    data:{
        init_info:{
            worker_id:'',
            id_name:{},
            id_group:{},
            ids_to_operate:[],
            groups:[],
            work_type_time:{},
            vacation_types:[]
        },
        group_selected:'',
        date_type_query_info:{
            ids:[],
            start_date:'',
            end_date:''
        },
        date_type_get_info:{},
        vacation_sub_info:{},
        all_date_select_one_vacation:{}
    },
    created:function () {
        this.get_init_info()
    },
    methods:{
        get_init_info:function () {
            let mv=this;
            $.ajax({
                url:'/attendance/vacation_submit',
                type:'get',
                dataType:'JSON',
                success:function (data) {
                    mv.init_info.worker_id=data.worker_id;
                    mv.init_info.id_name=data.id_name;
                    mv.init_info.id_group=data.id_group;
                    mv.init_info.ids_to_operate=data.ids_can_operate;
                    mv.init_info.groups=data.groups;
                    mv.group_selected=data.groups[0];
                    mv.init_info.work_type_time=data.work_type_time;
                    mv.init_info.vacation_types=data.vacation_types
                }
            })
        },
        add_id_to_subinfo:function (e) {
            var worker_id=$(e.target).attr('name');
            this.date_type_query_info.ids.push(worker_id)
        },
        remove_id_from_subinfo:function (e) {
            var worker_id=$(e.target).attr('name');
            var index_of_thisid=this.date_type_query_info.ids.indexOf(worker_id);
            this.date_type_query_info.ids.splice(index_of_thisid, 1);
        },
        sub_date_type_query_info:function () {
            let mv=this;
            if (mv.date_type_query_info.ids.length!==0){
                if(mv.date_type_query_info.start_date&&mv.date_type_query_info.end_date){
                    if(mv.date_type_query_info.start_date>mv.date_type_query_info.end_date){
                        alert('开始日期不能大于结束日期');
                        return
                    }
                }else{
                    alert('请输入完整的日期');
                    return
                }
            }else{
                alert('请至少选择一名员工');
                return
            }
            $.ajax({
                url:'/attendance/vacation_submit',
                dataType:'JSON',
                data:JSON.stringify(mv.date_type_query_info),
                type:'post',
                success:function (data) {
                    mv.date_type_get_info=data;
                    for(var id in data){
                        mv.$set(mv.vacation_sub_info,id,{});
                        mv.$set(mv.all_date_select_one_vacation,id,'事假');
                        for(var date in data[id]){
                            mv.$set(mv.vacation_sub_info[id],date,{});
                            mv.$set(mv.vacation_sub_info[id][date],'start_hour',mv.init_info.work_type_time[data[id][date]][0].slice(0,2));
                            mv.$set(mv.vacation_sub_info[id][date],'start_min',mv.init_info.work_type_time[data[id][date]][0].slice(3));
                            mv.$set(mv.vacation_sub_info[id][date],'end_hour',mv.init_info.work_type_time[data[id][date]][1].slice(0,2));
                            mv.$set(mv.vacation_sub_info[id][date],'end_min',mv.init_info.work_type_time[data[id][date]][1].slice(3));
                            mv.$set(mv.vacation_sub_info[id][date],'vacation_type','事假');
                        }
                    }
                }
            })
        },
        sub_vacation_info:function () {
            sub_data=[];
            for(var id in this.date_type_get_info){
                for(var date in this.date_type_get_info[id]){
                    var work_type=this.date_type_get_info[id][date];
                    var normal_work_start_time=this.init_info.work_type_time[work_type][0];
                    var normal_work_end_time=this.init_info.work_type_time[work_type][1];
                    var vacation_start_time=this.vacation_sub_info[id][date]['start_hour']+':'+this.vacation_sub_info[id][date]['start_min'];
                    var vacation_end_time=this.vacation_sub_info[id][date]['end_hour']+':'+this.vacation_sub_info[id][date]['end_min'];
                    if(normal_work_end_time<normal_work_start_time){
                        var normal_work_end_time_for_compare=this.time_plus_12h(normal_work_end_time);
                        var normal_work_start_time_for_compare=this.time_plus_12h(normal_work_start_time);
                        var vacation_start_time_for_compare=this.time_plus_12h(vacation_start_time);
                        var vacation_end_time_for_compare=this.time_plus_12h(vacation_end_time)
                    }else{
                        var normal_work_end_time_for_compare=normal_work_end_time;
                        var normal_work_start_time_for_compare=normal_work_start_time;
                        var vacation_start_time_for_compare=vacation_start_time;
                        var vacation_end_time_for_compare=vacation_end_time
                    }
                    if(vacation_start_time_for_compare<normal_work_start_time_for_compare||vacation_end_time_for_compare>normal_work_end_time_for_compare
                        ||vacation_start_time_for_compare>vacation_end_time_for_compare||this.vacation_sub_info[id][date]['vacation_type']===''){
                        alert('输入有误，请检查：1）假期时间是否超出正常工作时间的范围；2）假期开始时间大于结束时间；3）假期种类未填写');
                        return
                    }else{
                        var hours=(Number(vacation_end_time_for_compare.slice(0,2))-Number(vacation_start_time_for_compare.slice(0,2))+
                            (Number(vacation_end_time_for_compare.slice(3))-Number(vacation_start_time_for_compare.slice(3)))/60).toFixed(2);
                        if(normal_work_end_time_for_compare!==normal_work_end_time){
                            if(vacation_end_time_for_compare>='12:00'){
                                var sub_vacation_end_datetime=this.date_plus_one(date)+' '+vacation_end_time
                            }else{
                                var sub_vacation_end_datetime=date+' '+vacation_end_time
                            }
                            if(vacation_start_time_for_compare>='12:00'){
                                var sub_vacation_start_datetime=this.date_plus_one(date)+' '+vacation_start_time
                            }else{
                                var sub_vacation_start_datetime=date+' '+vacation_start_time
                            }
                        }else{
                            var sub_vacation_start_datetime=date+' '+vacation_start_time;
                            var sub_vacation_end_datetime=date+' '+vacation_end_time
                        }
                        var temp_list=[id,date,sub_vacation_start_datetime,sub_vacation_end_datetime,hours,this.vacation_sub_info[id][date]['vacation_type'],0,this.init_info.worker_id];
                        sub_data.push(temp_list)
                    }
                }
            }
            var alert_message='注意：如果已经提交过休假，再次提交会覆盖上一次的操作！！！\n请确认休假信息：\n姓名        开始时间              结束时间           小时数     种类\n';
            for(var i=0;i<sub_data.length;i++){
                alert_message=alert_message+this.init_info.id_name[sub_data[i][0]]+'    '+sub_data[i][2].slice(2)+'    '+sub_data[i][3].slice(2)+'    '+sub_data[i][4]+'    '+sub_data[i][5]+'\n'
            }
            var anwser=confirm(alert_message);
            if(anwser){
                $.ajax({
                    url:'/attendance/vacation_submit',
                    data:JSON.stringify(sub_data),
                    dataType:'JSON',
                    type:'post',
                    success:function () {
                        alert('done')
                    }
                })
            }
        },
        time_plus_12h:function (timestr) {
            var hour=timestr.slice(0,2);
            hour=Number(hour)+12;
            if(hour>=24){
                hour=hour-24;
                if(hour<10){
                    hour='0'+String(hour)
                }else{
                    hour=String(hour)
                }
            }
            var time_final=hour+timestr.slice(2);
            return time_final
        },
        date_plus_one:function (datestr) {
            var thisday=new Date(datestr);
            var nextday=new Date(thisday.valueOf()+24*1000*60*60);
            return this.dateToString(nextday)
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
        select_same_vacation_type:function (e) {
            var same_type=$(e.target).val();
            var id=$(e.target).attr('name').slice(-4);
            for(var date in this.vacation_sub_info[id]){
                this.vacation_sub_info[id][date]['vacation_type']=same_type
            }
        }
    }
});