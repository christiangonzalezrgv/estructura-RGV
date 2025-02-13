
// formato de grafica = "#chart1"
// Generic chart rendering function
// Generic chart rendering function
function generar_grafica(selector, chartType, data_y, data_x, options = {}) {
    if (!selector || !document.querySelector(selector)) {
        console.error("Invalid selector or element not found:", selector);
        return;
    }

    const defaultOptions = {
        series: [
            {
                name: options.seriesName || "",
                data: data_y,
            },
        ],
        chart: {
            height: 280,
            type: chartType || "bar",
            events: options.events || {},
            toolbar: {
                show: false,
            },
            fontFamily: "Inter, sans-serif",
        },
        colors: options.colors || [
            "#267DFF",
            "#7B6AFE",
            "#FF51A4",
            "#FF7C51",
            "#00D085",
            "#FFC41F",
            "#FF3232",
        ],
        plotOptions: {
            bar: {
                columnWidth: "20%",
                distributed: true,
                borderRadius: 5,
                ...options.plotOptions?.bar,
            },
        },
        dataLabels: {
            enabled: false,
            ...options.dataLabels,
        },
        legend: {
            show: false,
            ...options.legend,
        },
        yaxis: {
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false,
            },
            tickAmount: 5,
            labels: {
                formatter: value => value.toLocaleString(),
                offsetX: -10,
                offsetY: 0,
                style: {
                    fontSize: "12px",
                    fontWeight: "600",
                    colors: "#7780A1",
                    cssClass: "apexcharts-xaxis-title",
                },
            },
            opposite: false,
            ...options.yaxis,
        },
        xaxis: {
            tickAmount: 7,
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false,
            },
            categories: data_x,
            labels: {
                style: {
                    fontSize: "12px",
                    fontWeight: "600",
                    colors: "#7780A1",
                    cssClass: "apexcharts-xaxis-title",
                },
            },
            ...options.xaxis,
        },
        grid: {
            borderColor: "#e0e6ed",
            strokeDashArray: 2,
            xaxis: {
                lines: {
                    show: false,
                },
            },
            yaxis: {
                lines: {
                    show: true,
                },
            },
            padding: {
                top: 0,
                right: 0,
                bottom: 0,
                left: 25,
            },
            ...options.grid,
        },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    // Destroy the existing chart if it exists
    const chartKey = selector.replace(/[^a-zA-Z0-9]/g, ""); // Create a safe key for window storage
    if (window[chartKey]) {
        window[chartKey].destroy();
    }

    // Create and render the new chart
    window[chartKey] = new ApexCharts(document.querySelector(selector), mergedOptions);
    window[chartKey].render();
}



// handles option change
function grafica_dinamica(nombre_grafica, tipo_grafica,dataXKey, dataYKey,path) {
    fetch(path)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            // Check if data is an array
            if (!Array.isArray(data)) {
                throw new Error("Fetched data is not an array.");
            }
            const y = data.map(item => item[dataYKey]);
            const x = data.map(item => item[dataXKey]);
            generar_grafica(nombre_grafica, tipo_grafica, y, x);
        })
        .catch(error => {
            console.error("Error fetching or processing data:", error);
        });
}

