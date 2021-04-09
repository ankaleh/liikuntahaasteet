var myFunction = (endpoint) => {
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(data) {
            console.log(data.minutesInDay)
            return data
        }
    })
}

var getMyJsonAndDraw = (type, indexAxis) => {
    $.ajax({
        method: "GET",
        url: '/my-json',
        success: function(data) {
            if (type==='line') {
                draw(data.minutesInDay['dates'], data.minutesInDay['minutes'], type, indexAxis)
            } else if (type==='pie') {
                draw(data.durationPerExercise['exercises'], data.durationPerExercise['durations'], type, indexAxis)
            } else {
                getTable(data.all)
            }
        },
        error: function(error_data) {
            console.log(error_data);
        }
    })
}

var getAllJsonAndDraw = (chartType, indexAxis) => {
    $.ajax({
    method: "GET",
    url: '/all-json',
    success: function(data) {
        draw(data.labels, data.data, chartType, indexAxis);
        },
        error: function(error_data) {
            console.log(error_data);
        }
    })
}

var draw = (labels, data, type, indexAxis) => {
    var div = document.getElementById("container")
    while (div.firstChild) {
        div.removeChild(div.firstChild)
    }
    var ctx = document.createElement("canvas")
    var backButton = document.createElement("button")
    backButton.classList.add("btn")
    backButton.appendChild(document.createTextNode("Palaa takaisin"))
    backButton.addEventListener("click", () => history.back())
    div.appendChild(ctx)
    div.appendChild(backButton)

    var label = 'Lajiin käytetty aika minuutteina'
    if (type==='line') {
        label = 'Liikuntaan käytetty aika minuutteina / päivä'
    }
    var myChart = new Chart(ctx, {
        type,
        data: {
            labels,
            datasets: [{
                label,
                data,
                backgroundColor: [
                    '#FFB6C1',
                    '#20B2AA',
                    '#FFDAB9',
                    '#FFA07A',
                    '#E0FFFF',
                    '#7B68EE',
                    '#FFFACD',
                    '#87CEFA'
                ],
                borderColor: [
                    '#FFB6C1',
                    '#20B2AA',
                    '#FFDAB9',
                    '#FFA07A',
                    '#E0FFFF',
                    '#7B68EE',
                    '#FFFACD',
                    '#87CEFA'

                ],
                borderWidth: 1,
                indexAxis
            }]
        },
        options: {
            /* scales: {
                indexAxis: {
                beginAtZero: true
                }
                
            } */
        }
    })
}

var getTable = (all) => {
    var div = document.getElementById("container")
    while (div.firstChild) {
        div.removeChild(div.firstChild)
    }
    var backButton = document.createElement("button")
    backButton.classList.add("btn")
    backButton.appendChild(document.createTextNode("Palaa takaisin"))
    backButton.addEventListener("click", () => history.back())
    var table = document.createElement("table")
    table.classList.add("table")
    div.appendChild(table)
    div.appendChild(backButton)

    var headingRow = document.createElement("tr")
    headingRow.classList.add("table-heading")
        
    var heading1 = document.createElement("th")
    heading1.classList.add("table")
    heading1.appendChild(document.createTextNode("Laji"))

    var heading2 = document.createElement("th")
    heading2.classList.add("table")
    heading2.appendChild(document.createTextNode("Kesto"))

    var heading3 = document.createElement("th")
    heading3.classList.add("table")
    heading3.appendChild(document.createTextNode("Ajankohta"))

    headingRow.appendChild(heading1)
    headingRow.appendChild(heading2)
    headingRow.appendChild(heading3)

    table.appendChild(headingRow)
        
    for (i=0; i<all['exercises'].length; i++) {
        var dataRow = document.createElement("tr")
        dataRow.classList.add("table-data")
        var td1 = document.createElement("td")
        td1.classList.add("table")
        td1.appendChild(document.createTextNode(all['exercises'][i]))

        var td2 = document.createElement("td")
        td2.classList.add("table")
        td2.appendChild(document.createTextNode(all['durations'][i]))

        var td3 = document.createElement("td")
        td3.classList.add("table")
        td3.appendChild(document.createTextNode(all['dates'][i]))
        
        dataRow.appendChild(td1)
        dataRow.appendChild(td2)
        dataRow.appendChild(td3)
        table.appendChild(dataRow)  
    
    }
}
