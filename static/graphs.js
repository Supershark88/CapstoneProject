$(document).ready(function() {
    $(chart_id).highcharts({
        chart: chart,
        title: title,
        xAxis: xAxis,
        yAxis: yAxis,
        //yAxis1A: yAxis1A,
        //yAxis1B: yAxis1B,
        //yAxis1C: yAxis1C,
        //yAxis1D: yAxis1D,
        series: series
        });
});