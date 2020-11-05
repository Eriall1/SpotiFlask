    // this is called a javascript closure. it also wont run the code until the page is finished loading
    // and it protects the scope of your variables from other code you may later add to the page
    $(document).ready (function() {
        console.log("RUNNING FUNCTION")
        var initDB = $("#initDB")
            fillDB = $("#fillDB")
            clearDB = $("#clearDB")
            reportButton = $("#genReportButton")
            loadingGif = $("#loadingGif")
            form = $('#formInput')
            reportTable = $('#reportTable')
            reportTableH = $('#reportTableH')
            reportTableB = $("#reportTableB")
            
            // setup onclick functions
            document.getElementById("initDB").addEventListener("click", function() {
                sendR("init")
            }); 
            document.getElementById("fillDB").addEventListener("click", function() {
                sendR("fill")
            }); 
            document.getElementById("clearDB").addEventListener("click", function() {
                sendR("drop")
            }); 
            document.getElementById("genReportButton").addEventListener("click", function() {
                  genReport()
              }); 
            function sendR(str){
                console.log(str)
                send = {
                    function: str
                }
                sendF(send)
            }
            
            function genReport(){
                reportTableH.empty()
                reportTableB.empty()
                send = {}
                $.getJSON("/genReport", send, function(response){ // retrieve report
                    $.each(response.headers, function(index, value){
                        console.log(value)
                        reportTableH.append(`<th>${value}</th>`)
                    })
                    $.each(response.data, function(index, value){
                        reportTableB.append(`<td>${value}</td>`)
                    })
                })
                reportTable.attr('border', '1')
                reportTable.removeAttr('hidden')
            }
            async function sendF(send){ // send function
                initDB.attr("disabled", true)
                fillDB.attr("disabled", true)
                clearDB.attr("disabled", true)
                reportButton.attr('disabled', true)
                form.attr('hidden', true)
                loadingGif.removeAttr("hidden")

                await $.getJSON("/DBFunc", send, function(response){ // await so that the buttons arent available until the processing is over.
                    console.log(response)
                })
                initDB.removeAttr("disabled")
                fillDB.removeAttr("disabled")
                clearDB.removeAttr("disabled")
                reportButton.removeAttr('disabled')
                form.removeAttr('hidden')
                loadingGif.attr("hidden", true)
            }

    })