var greeting = new Vue({
    el:'#greeting',
    data:{
        worker_name:''
    },
    created:function () {
        this.get_info()
    },
    methods:{
        get_info:function () {
            let mv=this;
            $.ajax({
                url:'/attendance/workarrangement_type',
                dataType:'json',
                type:'get',
                success:function (data) {
                    mv.worker_name=data.worker_name;

                }
                })
        }
    }
});

var add_type=new Vue({
    el:'#add_type',
    data:{
        start_hour:'',
        start_min:'',
        end_hour:'',
        end_min:'',
        wa_type_name:'',
        inuse:1,
        type_info:'',
        name_list:[]
    },
    created:function(){
        this.get_info()
    },
    methods:{
        sub_add:function () {
            let mv=this;
            if(mv.name_list.indexOf(mv.wa_type_name)>=0||mv.wa_type_name==''){
                alert('名称重复或为空，请重新输入');
                return
            }else{
                if(mv.start_hour===''||mv.start_min===''||mv.end_hour===''||mv.end_min===''){
                    alert('请输入完整的时间');
                    return
                }else{
                    var sepmin=(Number(mv.end_hour)-Number(mv.start_hour))*60+Number(mv.end_min)-Number(mv.start_min);
                    sepmin = sepmin>0?sepmin:1440+sepmin;
                    if(sepmin>660||sepmin<540){
                        alert('排班时长要在9-11小时之间');
                        return
                    }else{
                        var sub_data={};
                        sub_data['typename']=mv.wa_type_name;
                        sub_data['start_time']=mv.start_hour+':'+mv.start_min;
                        sub_data['end_time']=mv.end_hour+':'+mv.end_min;
                        sub_data['inuse']=mv.inuse;
                        $.ajax({
                        dataType:'JSON',
                        data:JSON.stringify(sub_data),
                        type:'post',
                        url:'/attendance/workarrangement_type',
                        success:function () {
                            sub_data['readonly']=true
                            mv.type_info.push(sub_data);
                            mv.name_list.push(sub_data['typename']);
                        }    
                        })
                    }
                }
            }
        },
        
        get_info:function() {
            let mv = this;
            $.ajax({
                type: 'get',
                url: '/attendance/workarrangement_type',
                dataType: 'JSON',
                success: function (data) {
                    mv.type_info = data.type_info;
                    for (var i = 0; i < mv.type_info.length; i++) {
                        mv.name_list.push(mv.type_info[i]['typename']);
                    }
                }
            })
        },
        
        sub_edit:function (e) {
            let mv=this;
            var typename=$(e.target).attr('name')
            typename=typename.replace(/(^\s*)|(\s*$)/g, "");
            var edited_type={};
            for(var i=0;i<mv.type_info.length;i++){
                if(String(typename)===mv.type_info[i].typename){
                    mv.type_info[i].readonly=true;
                    edited_type=mv.type_info[i];
                    break
                }
            }
            if(edited_type.start_time.search(/^[0-2]\d\:[0-5]\d$/)!=-1&&edited_type.end_time.search(/^[0-2]\d\:[0-5]\d$/)!=-1){
                var sepmin=(Number(edited_type.end_time.slice(0,2))-Number(edited_type.start_time.slice(0,2)))*60
                    +Number(edited_type.end_time.slice(3,2))-Number(edited_type.start_time.slice(3,2));
                sepmin = sepmin>0?sepmin:1440+sepmin;
                if(sepmin>660||sepmin<540){
                    alert(sepmin+'排班时长要在9-11小时之间');
                    return
                }else{
                    $.ajax({
                    dataType:'JSON',
                    data:JSON.stringify(edited_type),
                    type:'post',
                    url:'/attendance/workarrangement_type',
                    success:function () {
                        alert(sepmin+'修改成功')
                    }
                    })
                }
            }else{
                alert('请输入正确的时间');
                return
            }

        },

        sub_del:function (e) {
            let mv=this;
            var typename = $(e.target).attr('name');
            if(confirm('确认删除班别‘'+typename+'‘吗？')){
                var del_type={};
                del_type['typename']=typename;
                $.ajax({
                    dataType:'JSON',
                    data:JSON.stringify(del_type),
                    type:'post',
                    url:'/attendance/workarrangement_type',
                    success:function () {
                        for(var i=0;i<mv.type_info.length;i++){
                            if(String(typename)===mv.type_info[i].typename){
                                delete mv.type_info[i];
                                alert('删除成功');
                                location.reload();
                                return
                            }
                        }
                    }
                })
            }
        }
    }
});