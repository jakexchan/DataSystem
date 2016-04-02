(function(){
    // using jQuery, Django post request, code from django documents
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    /*
        Remove charts view 
        div content function
    */
    function removeDivContent(){
        $('#charts-box').html('');
    }


    //Gender ratio charts
    $('#gender-btn').click(function(){
        removeDivContent();
        var ec = echarts.init(document.getElementById('charts-box'));
        ec.showLoading();

        $.ajax({
            url: '/gender_ratio/',
            type: 'post',
            success: function(response){
                var data = JSON.parse(response);
                ec.hideLoading();
                //Gender ratio option
                var option = {
                        title : {
                            text: '用户性别比例',
                            x:'center'
                        },
                        tooltip : {
                            trigger: 'item',
                            formatter: "{a} <br/>{b} : {c} ({d}%)"
                        },
                        toolbox:{
                            show: true,
                            orient: 'vertical',
                            feature: {
                                saveAsImage: {
                                    show: true,
                                    title: '用户性别比例'
                                },
                                restore: {
                                    show: true
                                },
                                dataView: {
                                    show: true
                                }
                            }
                        },
                        legend: {
                            orient: 'vertical',
                            left: 'left',
                            data: function(){
                                var list = [];
                                for ( var i in data ){
                                    list.push(i);
                                }
                                return list;
                            }()
                        },
                        series : [
                            {
                                name: 'Gender',
                                type: 'pie',
                                radius : '70%',
                                data: function(){
                                    var list = [];
                                    $.each(data, function(index, value){
                                        var obj = new Object();
                                        obj.value = parseInt(value);
                                        obj.name = index;
                                        list.push(obj);
                                        obj = null;
                                    });
                                    return list;
                                }(),
                                itemStyle:{ 
                                    normal:{ 
                                        label:{ 
                                            show: true, 
                                            formatter: '{b} : {c} ({d}%)' 
                                        }, 
                                        labelLine :{show:true},
                                        shadowBlur: 10,
                                        shadowOffsetX: 0,
                                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                                    }
                                },
                                roseType:true
                            }
                        ]
                    };  //optin end

                ec.setOption(option);
            }
        });
    });//Gender ratio charts end


    $('#gender-weibo-btn').click(function(){
        removeDivContent();
        var ec = echarts.init(document.getElementById('charts-box'), 'dark');
        ec.showLoading();

        $.ajax({
            url: '/gender_weibo_count/',
            type: 'post',
            success: function(response){
                data = JSON.parse(response);
                ec.hideLoading();
                var labels = ['0-100', '100-1000', '1000-2000', '2000-5000', '5000-10000', '10000以上'];
                var option = {
                    title : {
                        text: '用户性别与其微博数量比较情况',
                        x:'left'
                    },
                    tooltip : {
                        trigger: 'axis',
                        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        }
                    },
                    toolbox:{
                        show: true,
                        orient: 'vertical',
                        feature: {
                            saveAsImage: {
                                show: true,
                                title: '用户性别与其微博数量比较情况'
                            },
                            restore: {
                                show: true
                            },
                            dataView: {
                                show: true
                            },
                            magicType: {
                                type: ['line', 'bar', 'stack', 'tiled']
                            }
                        }
                    },
                    legend: {
                        data:function(){
                            var list = [];
                            for( var i = 0; i < data.length; i++){
                                for(var index in data[i]){
                                    list.push(index)
                                }
                            }
                            return list;
                        }()
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis : [
                        {
                            type : 'category',
                            data : labels
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    series : function(){
                        var list = [];
                        for(var i = 0; i < data.length; i++){
                            var obj = new Object();
                            $.each(data[i], function(index, value){
                                obj.name = index;
                                obj.type = 'bar';
                                obj.data = [];
                                for(var j = 0; j < labels.length; j++){
                                    $.each(value, function(x, y){
                                        if(x === labels[j]){
                                            obj.data.push(y);
                                        }
                                    });
                                }
                            });
                            list.push(obj);
                            obj = null;
                        }
                        return list;
                    }()
                };

                ec.setOption(option);
            }
        });
    });

    $('#gender-follow-btn').click(function(){
        removeDivContent();
        var ec = echarts.init(document.getElementById('charts-box'));
        ec.showLoading();

        $.ajax({
            url: '/gender_follow_count/',
            type: 'post',
            success: function(response){
                data = JSON.parse(response);
                ec.hideLoading();
                var labels = ['0-200', '200-400', '400-600', '600-800', '800-1000', '1000以上'];
                var option = {
                    title : {
                        text: '用户性别与其关注数量比较情况',
                        x:'left'
                    },
                    tooltip : {
                        trigger: 'axis',
                        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        }
                    },
                    toolbox:{
                        show: true,
                        orient: 'vertical',
                        feature: {
                            saveAsImage: {
                                show: true,
                                title: '用户性别与其关注数量比较情况'
                            },
                            restore: {
                                show: true
                            },
                            dataView: {
                                show: true
                            },
                            magicType: {
                                type: ['line', 'bar', 'stack', 'tiled']
                            }
                        }
                    },
                    legend: {
                        data:function(){
                            var list = [];
                            for( var i = 0; i < data.length; i++){
                                for(var index in data[i]){
                                    list.push(index)
                                }
                            }
                            return list;
                        }()
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis : [
                        {
                            type : 'category',
                            data : labels
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    series : function(){
                        var list = [];
                        for(var i = 0; i < data.length; i++){
                            var obj = new Object();
                            $.each(data[i], function(index, value){
                                obj.name = index;
                                obj.type = 'line';
                                obj.data = [];
                                for(var j = 0; j < labels.length; j++){
                                    $.each(value, function(x, y){
                                        if(x === labels[j]){
                                            obj.data.push(y);
                                        }
                                    });
                                }
                            });
                            list.push(obj);
                            obj = null;
                        }
                        return list;
                    }()
                };

                ec.setOption(option);
            }
        });
    });


    $('#gender-fans-btn').click(function(){
        removeDivContent();
        var ec = echarts.init(document.getElementById('charts-box'), 'macarons');
        ec.showLoading();

        $.ajax({
            url: '/gender_fans_count/',
            type: 'post',
            success: function(response){
                data = JSON.parse(response);
                ec.hideLoading();
                var labels = ['0-500', '500-1000', '1000-3000', '3000-5000', '5000-10000', '10000以上'];
                var option = {
                    title : {
                        text: '用户性别与其粉丝数量比较情况',
                        x:'left'
                    },
                    tooltip : {
                        trigger: 'axis',
                        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        }
                    },
                    toolbox:{
                        show: true,
                        orient: 'vertical',
                        feature: {
                            saveAsImage: {
                                show: true,
                                title: '用户性别与其粉丝数量比较情况'
                            },
                            restore: {
                                show: true
                            },
                            dataView: {
                                show: true
                            },
                            magicType: {
                                type: ['line', 'bar', 'stack', 'tiled']
                            }
                        }
                    },
                    legend: {
                        data:function(){
                            var list = [];
                            for( var i = 0; i < data.length; i++){
                                for(var index in data[i]){
                                    list.push(index)
                                }
                            }
                            return list;
                        }()
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis : [
                        {
                            type : 'category',
                            data : labels
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    series : function(){
                        var list = [];
                        for(var i = 0; i < data.length; i++){
                            var obj = new Object();
                            $.each(data[i], function(index, value){
                                obj.name = index;
                                obj.type = 'bar';
                                obj.data = [];
                                for(var j = 0; j < labels.length; j++){
                                    $.each(value, function(x, y){
                                        if(x === labels[j]){
                                            obj.data.push(y);
                                        }
                                    });
                                }
                            });
                            list.push(obj);
                            obj = null;
                        }
                        return list;
                    }()
                };

                ec.setOption(option);
            }
        });
    });

}());