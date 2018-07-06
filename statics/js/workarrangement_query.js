var all = new Vue({
    el:'#all',
    data:{
        group_names:['生产|点测','生产|包装','生产|分选','生产|全体','工程|点测','工程|分选','工程|全体','职员|职员',''],
        types:{},
        worker_name:'',
        id_name:'',
        id_group:'',
        query_condition:{
            start_date:'',
            end_date:'',
            group:'',
            worker_id:'',
            type:''
        },
        show_data:{
            worker_id:[],
            date:[],
            type:[],
            operator_id:[]
        }
    },
    created:function(){
        this.get_type()
    },
    methods:{
        get_type:function () {
            let mv=this;
            $.ajax({
                url:'/attendance/workarrangement_query',
                type:'get',
                dataType:'JSON',
                success:function (data) {
                    mv.worker_name=data.worker_name;
                    delete data.worker_name;
                    mv.id_name=data.id_name;
                    delete data.id_name;
                    mv.id_group=data.id_group;
                    delete data.id_group;
                    mv.types=data;
                    mv.types['']='';
                }
            })
        },
        sub_query:function () {
            let mv=this;
            if(mv.query_condition.start_date&&mv.query_condition.end_date){
                if(mv.query_condition.group||mv.query_condition.worker_id||mv.query_condition.type){
                    if(mv.query_condition.worker_id&&(mv.query_condition.worker_id.search(/^s|S\d{3,4}$/)===-1)){
                        alert('请输入正确的工号：字母s(S)加3位数字');
                        return
                    }
                    $.ajax({
                        url:'/attendance/workarrangement_query',
                        type:'post',
                        dataType:'JSON',
                        data:JSON.stringify(mv.query_condition),
                        success:function (data) {
                            mv.show_data=data;
                        }
                    })
                }else{
                    alert('请至少输入一种查询条件！');
                    return
                }
            }else{
                alert('请输入起始日期！');
                return
            }

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

        easy_operator:function (e) {
          let mv=this;
          var tooday=new Date();
          var thisyear=tooday.getFullYear();
          var thismonth = tooday.getMonth();
          if($(e.target).context.textContent==='上月'){
              var start_date=new Date(thisyear,thismonth-1,1);
              mv.query_condition.start_date=mv.dateToString(start_date);
              var end_date=new Date(thisyear,thismonth,0);
              mv.query_condition.end_date=mv.dateToString(end_date);
          }else if($(e.target).context.textContent==='本月'){
              var start_date=new Date(thisyear,thismonth,1);
              mv.query_condition.start_date=mv.dateToString(start_date);
              var end_date=new Date(thisyear,thismonth+1,0);
              mv.query_condition.end_date=mv.dateToString(end_date);
          }else{
              var start_date=new Date(thisyear,thismonth+1,1);
              mv.query_condition.start_date=mv.dateToString(start_date);
              var end_date=new Date(thisyear,thismonth+2,0);
              mv.query_condition.end_date=mv.dateToString(end_date);
          }
      },
    }
})