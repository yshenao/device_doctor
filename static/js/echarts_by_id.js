// echarts部分, 横纵坐标传入的data都还不对, 只是测试过可以显示折线图了这样.

// 【1】基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main_by_id'));

// 【2】指定图表的配置项和数据
var option = {
  // Make gradient line here
  visualMap: {
      show: false,
      type: 'continuous',
      seriesIndex: 0,
      min: -1.2,
      max: -0.85
    },
  title: {
      left: 'center',
      text: testpoint_id
    },
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
//      data: dateList
    type: 'category',
    boundaryGap: false,
    data: date_ls
    },
  yAxis: {
        type: 'value',
        scale: true,
        min: (value) => {
            return value.min
        },
        max: (value) => {
            return value.max
        },
        name: '断电电位'
    },
  grid: {
//      bottom: '10%'
    },
  series: {
      type: 'line',
      showSymbol: false,
      data: data_ls
    },
};

// 【3】使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
