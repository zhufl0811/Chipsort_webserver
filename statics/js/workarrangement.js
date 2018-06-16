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
//
// var submit = new Vue({
//     el:'#submit_button',
//     methods:{
//         submit_work_arrangement:function () {
//             for
//         }
//     }
// })
