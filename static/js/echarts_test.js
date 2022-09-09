// echarts部分, 横纵坐标传入的data都还不对, 只是测试过可以显示折线图了这样.

// 【1】基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));

// 【2】指定图表的配置项和数据
var option = {
  xAxis: {
    type: 'category',
//    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    boundaryGap: false,
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
//      data: [150, 230, 224, 218, 135, 147, 260, 135, 147, 260],
      type: 'line',
      data: arrayObj,
    }
  ]
};
// 【3】使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
