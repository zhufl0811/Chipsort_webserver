var greeting = new Vue({
    el:'#greeting',
    data:{
        worker_id:''

    },
    created:function () {
        this.get_info()
    },
    methods:{
        get_info:function () {
            let mv=this;
            $.ajax({
                url:'/attendance/workarrangement',
                dataType:'json',
                type:'get',
                success:function (data) {
                    mv.worker_id=data.worker_id;

                }
                })
        }
    }
});


var getgroup = new Vue({
    el:'#form_wa',
    data:{
        group_info:''
    },
    created:function () {
        this.get_info()
    },
    methods:{
        get_info:function () {
            let mv=this;
            $.ajax({
                url:'/attendance/workarrangement',
                dataType:'json',
                type:'get',
                success:function (data) {
                    mv.group_info = data.group_info;
                    }
                });
        }
    }
    });

function submit(group_name) {
    var sub_info={};
    groups=getgroup.group_info;
    var start_date = $("input[name='start_date_of_"+group_name+"\']").val();
    var end_date = $("input[name='end_date_of_"+group_name+"\']").val();
    if(start_date){
        if(end_date){
            if(start_date>end_date){
                alert('开始日期需要小于结束日期')
            }else{
                sub_info['start_date']=start_date;
                sub_info['end_date']=end_date;
                for(var i=0;i<groups.length;i++) {
                    if (group_name === groups[i].group_name) {
                        var sub_group = groups[i].group_members;
                    }
                }
                for(var j=0;j<sub_group.length;j++){
                    id = sub_group[j].id;
                    type = $('input[name='+id+']:checked').val();
                    sub_info[id]=type
                }
                sub_info=JSON.stringify(sub_info);
                $.ajax({
                    url:'/attendance/workarrangement',
                    dataType:'json',
                    type:'post',
                    data:sub_info,
                    success: function(ret) {
                        alert('OK');
                    }
                })
            }
        }else{
            alert('请输入结束日期')
        }
    }else{
        alert('请输入开始日期')
    }

}


