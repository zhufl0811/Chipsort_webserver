var all=new Vue({
    el:'#all',
    data:{
        init_info:{
            worker_id:'',
            id_name:''
        },
        query_condition:{
            start_date:'',
            end_date:''
        },
        return_info:[],
        info_for_filter:{},
        filter_condition:{
            group_selected:'',
            name_selected:'',
            ratio_selected:'',
            state_selected:'',
            submit_id_selected:'',
            audit_id_selected:''
        }
    },
    created:function () {
        this.get_init_info()
    },
    methods:{
        get_init_info:function () {
            let mv=this;
            $.ajax({
                url:'/attendance/overtime_query',
                type:'get',
                dataType:'JSON',
                success:function (data) {
                    mv.init_info.worker_id=data.worker_id;
                    mv.init_info.id_name=data.id_name
                }
            })
        },
        sub_query:function () {
            let mv=this;
            if(mv.query_condition.start_date>mv.query_condition.end_date){
                alert('开始日期要小于结束日期');
                return
            }
            $.ajax({
                url:'/attendance/overtime_query',
                type:'post',
                dataType:'JSON',
                data:JSON.stringify(mv.query_condition),
                success:function (data) {
                    mv.return_info=data.return_info;
                    mv.info_for_filter=data.info_for_filter
                }
            })
        }
    }
})