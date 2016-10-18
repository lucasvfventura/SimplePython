$( document ).ready( function(){
    $("#search").click(function(){
        $.get("crawl", {search: $("#search_term").val()}, function(){
            alert("Crawling for: " + $("#search_term").val());
            $("#search_term").val("");
        });
    });

    $.getJSON("data", {bins: 10}, function( data ) {
        nv.addGraph(function() {
            var chart = nv.models.multiBarChart()
                            .showControls(false)
                            .x(function(d) {
                                return d.label
                            });

            chart.xAxis.axisLabel('10 Price bins');
            chart.yAxis.axisLabel('Items quantity in each price(CDN$) bin').tickFormat(d3.format(',.0f'));

            d3.select('#chart1 svg')
                .datum(data.histogram)
                .transition().duration(500)
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        });

        nv.addGraph(function() {
            var chart = nv.models.lineChart().useInteractiveGuideline(true);

            chart.xAxis
                .axisLabel('Collect order per term')
                .tickFormat(d3.format(',r'));

            chart.yAxis
                .axisLabel('Prices (CDN$)')
                .tickFormat(d3.format('.0f'));

            d3.select('#chart svg')
                .datum(data.data)
                .transition().duration(500)
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        });
    });
});


