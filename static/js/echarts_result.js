// echarts部分, 横纵坐标传入的data都还不对, 只是测试过可以显示折线图了这样.

// 【1】基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('result_echarts'));

// 【2】指定图表的配置项和数据
var option = {
  tooltip: {
    trigger: 'item',
    formatter: `{d}%`
  },
  legend: {
    show: false,
  },
  series: [
    {
      type: 'pie',
      radius: '50%',
      data: [
        { value: status_count_ls.normal_cnt, name: '正常' },
        { value: status_count_ls.data_lost_cnt, name: '数据丢失' },
        { value: status_count_ls.abnormal_cnt, name: '异常' },
        { value: status_count_ls.disturbed_cnt, name: '干扰中' },
      ],
      label:{
        show: true,
        formatter:function(data){
            return `${data.name} ${data.value}个`
        }
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};

// 【3】使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
