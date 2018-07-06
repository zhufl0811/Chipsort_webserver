var all=new Vue({
    el:'#all',
    data:{
        init_get_info:{
            worker_id:'',
            worker_name:'',
            id_name:{},
            id_group:{},
            overtime_unaudited_info:{}
        },
        date_selected:'',
        group_selected:'',
        sub_audit_info:{
            date:'',
            ids:[],
            pass_or_not:''
        },
    },
    created:function () {
        this.get_info()
    },
    methods:{
        get_info:function () {
            let mv=this;
            $.ajax({
                url:'/attendance/overtime_audit',
                dataType:'JSON',
                type:'get',
                success:function (data) {
                    mv.init_get_info.worker_id=data.worker_id;
                    mv.init_get_info.worker_name=data.worker_name;
                    mv.init_get_info.id_name=data.id_name;
                    mv.init_get_info.id_group=data.id_group;
                    mv.init_get_info.overtime_unaudited_info=data.overtime_unaudited_info
                }
            })
        },
        sub_audit_to_server:function(){
            let mv=this;
            $.ajax({
                url:'/attendance/overtime_audit',
                type:'post',
                data:JSON.stringify(mv.sub_audit_info),
                dataType:'JSON',
                success:function () {
                    delete mv.init_get_info.overtime_unaudited_info[mv.sub_audit_info.date];
                    mv.sub_audit_info.date='';
                    mv.sub_audit_info.ids=[];
                    mv.sub_audit_info.pass_or_not='';
                    alert('OK`');
                    document.location.reload();
                }
            })
        },
        sub_audit_one_day:function (e) {
            let mv=this;
            var tag_name=$(e.target).attr('name');  //取得按钮name值,name格式：pass_2018-09-07 或者 no_pass_2019-09-05
            mv.sub_audit_info.date=tag_name.slice(-10);
            var init_info_thisday=mv.init_get_info.overtime_unaudited_info[mv.sub_audit_info.date];
            for(group in init_info_thisday){
                for(var i=0;i<init_info_thisday[group].length;i++){
                    mv.sub_audit_info.ids.push(init_info_thisday[group][i][0])
                }
            }
            if (tag_name.slice(0,-11)==='pass'){
                mv.sub_audit_info.pass_or_not=1
            }else{
                mv.sub_audit_info.pass_or_not=0
            }
            mv.sub_audit_to_server()
        },
        sub_audit_one_group:function (e) {
            let mv=this;
            var tag_name=$(e.target).attr('name');
            mv.sub_audit_info.date=tag_name.slice(-10);
            var group=tag_name.slice(-16,-11);
            var init_info_thisgroup=mv.init_get_info.overtime_unaudited_info[mv.sub_audit_info.date][group];
            for(var i=0;i<init_info_thisgroup.length;i++){
                mv.sub_audit_info.ids.push(init_info_thisgroup[i][0])
            }
            if (tag_name.slice(0,-17)==='pass'){
                mv.sub_audit_info.pass_or_not=1
            }else{
                mv.sub_audit_info.pass_or_not=0
            }
            mv.sub_audit_to_server()
        },
        sub_audit_one_person:function (e) {
            var tag_name=$(e.target).attr('name');
            this.sub_audit_info.date=tag_name.slice(-10);
            this.sub_audit_info.ids.push(tag_name.slice(-15,-11));
            if (tag_name.slice(0,-16)==='pass'){
                this.sub_audit_info.pass_or_not=1
            }else{
                this.sub_audit_info.pass_or_not=0
            }
            this.sub_audit_to_server()
        }
    }
})