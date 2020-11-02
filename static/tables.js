    // this is called a javascript closure. it also wont run the code until the page is finished loading
    // and it protects the scope of your variables from other code you may later add to the page
    $(document).ready (function() {
        console.log("RUNNING FUNCTION")
        var initDB = $("#initDB")
            fillDB = $("#fillDB")
            clearDB = $("#clearDB")
            loadingGif = $("#loadingGif")
            
            document.getElementById("initDB").addEventListener("click", function() {
                sendR("init")
            }); 
            document.getElementById("fillDB").addEventListener("click", function() {
                sendR("fill")
            }); 
            document.getElementById("clearDB").addEventListener("click", function() {
                sendR("drop")
            }); 

            function sendR(str){
                console.log(str)
                send = {
                    function: str
                }
                sendF(send)
            }
            
            async function sendF(send){
                initDB.attr("disabled", true)
                fillDB.attr("disabled", true)
                clearDB.attr("disabled", true)
                loadingGif.removeAttr("hidden")

                await $.getJSON("/DBFunc", send, function(response){
                    console.log(response)
                })
                initDB.removeAttr("disabled")
                fillDB.removeAttr("disabled")
                clearDB.removeAttr("disabled")
                loadingGif.attr("hidden", true)
            }
    })