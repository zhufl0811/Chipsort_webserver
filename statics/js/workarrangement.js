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

var a;
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
                    a=data.group_info
                    }
                });
        }
    }
    });

function submit_wa(group_name) {
    var sub_info={};
    groups=getgroup.group_info;
    var start_date = $("input[name='start_date_of_"+group_name+"\']").val();
    var end_date = $("input[name='end_date_of_"+group_name+"\']").val();
    if(start_date){
        if(end_date){
            if(start_date>end_date){
                alert('开始日期需要小于结束日期')
            }else{
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
                if(JSON.stringify(sub_info)==='{}'){
                    alert('请至少提供一名员工的排班信息')
                }else{
                    sub_info['start_date']=start_date;
                    sub_info['end_date']=end_date;
                    sub_info=JSON.stringify(sub_info);
                    $.ajax({
                        url:'/attendance/workarrangement',
                        dataType:'json',
                        type:'post',
                        data:sub_info,
                        success: function() {
                            alert(group_name+' 提交成功');
                        }
                    })
                }

            }
        }else{
            alert('请输入**本组**的结束日期')
        }
    }else{
        alert('请输入**本组**的开始日期')
    }

}

function submit_diy(that) {
    var diy_group_info={};
    var ids_divided_into=[];
    var son_group_name = $(that).parent().prev().find('input');
    if(son_group_name[0].value){
        diy_group_info['son_group_name']=son_group_name[0].value
    }else{
        alert('请输入分组名称');
        return
    };
    var ids_not_diyed = $(that).parent().prev().prev().find('input:checked');
    if(ids_not_diyed.length<2){
        alert('请至少选中两名员工');
        return
    }else{
        for(var i=0;i<ids_not_diyed.length;i++){
            ids_divided_into.push(ids_not_diyed[i].value)
        }
    }
    diy_group_info['ids_divided_into']=ids_divided_into;
    diy_group_info=JSON.stringify(diy_group_info);
    $.ajax({
        url:'/attendance/workarrangement',
        dataType:'json',
        type:'post',
        data:diy_group_info,
        success: function() {
            alert('分组成功');
            window.location.reload()
        }
    })
}

function select_group(that) {
    var div_ids_in_this = $(that).parent().parent().find('div');
    var ids_in_this=[];
    for(i=0;i<div_ids_in_this.length;i++){
        ids_in_this.push($.trim(div_ids_in_this[i].textContent))
    }
    if($(that).attr('name')==='select_group_1'){
            for(i in ids_in_this){
                $("input[type='radio'][name="+ids_in_this[i]+"][value=1]").prop('checked','checked')
            }
    }else if($(that).attr('name')==='select_group_2'){
        for(i in ids_in_this){
                $("input[type='radio'][name="+ids_in_this[i]+"][value=2]").prop('checked','checked')
            }
    }else{
        for(i in ids_in_this){
                $("input[type='radio'][name="+ids_in_this[i]+"][value=3]").prop('checked','checked')
            }
    }
}

function delete_group(that) {
    var group_name=$(that).parents('table').attr('name').slice(0,5);
    var diy_group_name = $(that).attr('name');
    var data={};
    data['group_parent']=group_name;
    data['group_son'] = diy_group_name;
    $.ajax({
        url:'/attendance/workarrangement',
        dataType:'json',
        type:'post',
        data:JSON.stringify(data),
        success: function() {
            alert('删除成功');
            window.location.reload()
        }
    })
}
