var all=new Vue({
  el:'#all',
  data:{
      worker_id:'',
      worker_name:'',
      group_info:'',
      group_selected_to_show:'',
      workarrangement_types:'',
      sub_info:{
          'start_date':'',
          'end_date':'',
          'wa_info':{}
      }

  },
  created:function () {
        this.get_info()
    },
  methods:{
      get_info:function () {
          let mv=this;
            $.ajax({
                url:'/attendance/workarrangement_new',
                dataType:'json',
                type:'get',
                success:function (data) {
                    mv.worker_id=data.worker_id;
                    mv.worker_name=data.worker_name;
                    mv.group_info=data.group_info;
                    mv.group_selected_to_show=mv.group_info[0].group_name;
                    mv.workarrangement_types=data.workarrangement_types
                }
                })
      },
      easy_operator:function (e) {
          let mv=this;
          var tooday=new Date();
          var thisyear=tooday.getFullYear();
          var thismonth = tooday.getMonth();
          if($(e.target).context.textContent==='上月'){
              var start_date=new Date(thisyear,thismonth-1,1);
              mv.sub_info.start_date=mv.dateToString(start_date);
              var end_date=new Date(thisyear,thismonth,0);
              mv.sub_info.end_date=mv.dateToString(end_date);
          }else if($(e.target).context.textContent==='本月'){
              var start_date=new Date(thisyear,thismonth,1);
              mv.sub_info.start_date=mv.dateToString(start_date);
              var end_date=new Date(thisyear,thismonth+1,0);
              mv.sub_info.end_date=mv.dateToString(end_date);
          }else{
              var start_date=new Date(thisyear,thismonth+1,1);
              mv.sub_info.start_date=mv.dateToString(start_date);
              var end_date=new Date(thisyear,thismonth+2,0);
              mv.sub_info.end_date=mv.dateToString(end_date);
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
      select_son_group:function (e) {
          let mv=this;
          var type=$(e.target).context.textContent.replace(/\s/g,'').slice(2);
          a=$(e.target).parent().parent().parent().find("input[value=\'"+type+"\']");
          for(var i=0;i<a.length;i++){
              $(a[i]).click()
          }
      },
      sub_info_to_server:function () {
          let mv=this;
          var sd=this.sub_info.start_date;
          var ed=this.sub_info.end_date;
          if(!(sd&&ed)){
              alert('开始和结束日期均要填写')
          }else if(new Date(ed.substr(0,4),ed.substr(5,2),ed.substr(8,2))<new Date(sd.substr(0,4),sd.substr(5,2),sd.substr(8,2))){
              alert('结束日期不得小于开始日期')
          }else{
              $.ajax({
                url:'/attendance/workarrangement_new',
                type:'post',
                dataType:'JSON',
                data:JSON.stringify(mv.sub_info),
                success:function(){
                  alert('ok')
                }
              })
          }
      }
  }
})
