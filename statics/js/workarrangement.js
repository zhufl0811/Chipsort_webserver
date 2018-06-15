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
                    mv.worker_id=data.worker_id}
                })
        }
    }
});


var getgroup = new Vue({
    el:'#group',
    data:{
        groupmembers:Object,
        ids:[],
        rows:''
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
                    mv.groupmembers=data.groupmembers;
                    mv.ids=Object.keys(data.groupmembers);
                    mv.rows=Math.ceil(mv.ids.length/7)
                    }
                });
                }
    }
    });