    // this is called a javascript closure. it also wont run the code until the page is finished loading
    // and it protects the scope of your variables from other code you may later add to the page
    $(document).ready (function() {
        console.log("RUNNING FUNCTION")
        var select_table1 = $('#tableselect1'),
            select_table2 = $('#tableselect2'),
            select_variable1 = $('#varselect1'),
            select_variable2 = $('#varselect2'),
            query_variable = $("#queryvarselect")
            query_variable_label = $("#query_variable_label")
            variable_label = $('#varlabel1'),
            queryLabel = $('#queryLabel'),
            queryInput = $('#queryInput'),
            submitButton = $('#submitButton'),
            tableV = $('#resultsTable')
            resultsTable = $("#resultsTable tbody"),
            resultsTableHeader = $("#resultsTable thead")
            resultHeading = $("#resultHeading")
            orderSelect = $("#orderSelect")
            orderSelectLabel = $("#orderSelectLabel")
            hackingGif = $("#hackingGif")
            ohnoGif = $("#ohnoGif")
            groupSelectLabel = $("#groupSelectLabel")
            groupSelect = $("#groupSelect")
            toggleSwitch = false;  
            singleMultiL = $("#singleMultiL")
            singleMultiC = $("#singleMultiC")
            tableselectL1 = $("#tableselectL1")
            tableselectL2 = $("#tableselectL2")
            orderTable = $("#orderSelect")
            groupTable = $("#groupTable")
            orderTableLabel = $("#orderTableLabel")
            groupTableLabel = $("#groupTableLabel")
            isMulti = false
        
        orderTable.change(function(){
            console.log("ORDER TABLE CHANGED")
            console.log(orderTable.val())
            onOrderChange()
        })
        groupTable.change(function(){
            console.log("GROUP TABLE CHANGED")
            console.log(groupTable.val())
            onGroupChange()
        })       

        singleMultiC.change(function(){
            console.log("CHNAGED SINGLE/MULTI")
            console.log(singleMultiC.val())
            onSingleMultiC()
        })

        query_variable.change(function(){
            console.log("CHANGED QVAR")
            console.log(query_variable.val())
        });
        
        select_table1.change(function() {
            // fires when room selection changes
            console.log("CHANGED TABLE")
            console.log(select_table1.val())
            getUpdatedSettings()
        });

        select_variable1.change(function() {
            console.log("CHANGED VARIABLE")
            console.log(select_variable1.val())
            if (select_variable1.val() != "*") { toggleSwitch = false; variableSearch = select_variable1.val(); } else { toggleSwitch = true; };
            onVariableChange()
        });

        queryInput.change(function(){
            console.log("CHANGED QUERY")
            console.log(queryInput.val())
            onQueryChange()
        });

        orderSelect.change(function(){
            console.log("CHANGED ORDER")
            console.log(orderSelect.val())
            onOrderSelect()
        });

        function onGroupChange(){
            val = groupTable.val()

            groupSelect.removeAttr('hidden')
            groupSelect.removeAttr('disabled')
            groupSelectLabel.removeAttr('hidden')
            fetchValues(groupTable.val(), "group")
        }

        function onOrderChange(){
            val = orderTable.val()
            
            orderSelect.removeAttr('hidden')
            orderSelect.removeAttr('disabled')
            orderSelectLabel.removeAttr('hidden')
            fetchValues(orderTable.val(), "order")
        }

        function onSingleMultiC(){
            val = singleMultiC.val()
            console.log(val)
            if (val != "Single"){
                isMulti = true
            }
            else if(val == "Single") {
                isMulti = false
            }
            singleMultiL.attr('hidden', true)
            singleMultiC.attr('hidden', true)
            changeBase()
        };

        function changeBase(){
            if (isMulti){
                select_table2.removeAttr('hidden')
                select_variable2.removeAttr('hidden')
                select_variable1
            }
            
            select_table1.removeAttr('hidden')
            tableselectL1.removeAttr('hidden')
        }
        function onOrderSelect(){
        }
        submitButton.click(sendData)

        function onVariableChange() {
            revealSwitch()

            submitButton.removeAttr('hidden')
            submitButton.removeAttr('disabled')
            queryLabel.removeAttr('disabled')
            queryLabel.removeAttr('hidden')
            queryInput.removeAttr('disabled')
            queryInput.removeAttr('hidden')

        }

        function revealSwitch(){
            console.log(toggleSwitch)
            if (isMulti == false){
                if (toggleSwitch){
                query_variable_label.removeAttr("disabled")
                query_variable_label.removeAttr("hidden")
                query_variable.removeAttr("disabled")
                query_variable.removeAttr("hidden")
                } else  {
                    query_variable_label.attr("disabled", true)
                    query_variable_label.attr("hidden", true)
                    query_variable.attr("disabled", true)
                    query_variable.attr("hidden", true)
                }
                groupSelectLabel.removeAttr('hidden')
                groupSelect.removeAttr('hidden')
                groupSelect.removeAttr('disabled')
                orderSelectLabel.removeAttr('hidden')
                orderSelect.removeAttr('hidden')
                orderSelect.removeAttr('disabled')
            }
                
        }

        function sendData() {
            if (isMulti) {
                if (toggleSwitch) {
                    var send = {
                        table1: select_table1.val(),
                        table2: select_table2.val(),
                        qVar1: select_variable1.val(),
                        qVar2: select_variable2.val(),
                        group: groupSelect.val(),
                        groupTable: groupTable.val(),
                        order: orderSelect.val(),
                        orderTable:orderTable.val(),
                    };
                } else {
                    var send = {
                        table1: select_table1.val(),
                        table2: select_table2.val(),
                        qVar1: select_variable1.val(),
                        qVar2: select_variable2.val(),
                        group: groupSelect.val(),
                        groupTable: groupTable.val(),
                        order: orderSelect.val(),
                        orderTable:orderTable.val(),
                    };
                }
            } else {
                if (toggleSwitch) {
                    var send = {
                        table: select_table1.val(),
                        variable: select_variable1.val(),
                        qVar1: query_variable.val(),
                        query: queryInput.val(),
                        order: orderSelect.val(),
                        group: groupSelect.val(),
                    };
                } else {
                    var send = {
                        table: select_table1.val(),
                        variable: select_variable1.val(),
                        qVar1: select_variable1.val(),
                        query: queryInput.val(),
                        order: orderSelect.val(),
                        group: groupSelect.val(),
                    };
                };
            };
            console.log(isMulti)
            send["multi"] = isMulti
            select_variable1.attr('disabled', true);
            select_variable1.attr('hidden', true);
            select_table1.attr('disabled', true);
            select_table1.attr('hidden', true);
            queryInput.attr("hidden", true);
            queryInput.attr("disabled", true);
            submitButton.attr("disabled", true);
            submitButton.attr("hidden", true);
            

            $.getJSON("/query_sql", send, function(response) {
                console.log(response);
                resultsTable.empty();
                resultsTableHeader.empty()
                resultHeading.text(select_table1.val())
                resultsList = response.results;
                
                resultsTableHeader.append('<tr>');
                if (select_variable1.val() !="*"){
                    resultsTableHeader.append(`<th>${select_variable1.val()}</th>`)
                } else {
                    for (let varible of variableList) {
                        resultsTableHeader.append(`<th>${varible}</th>`);
                    }
                }
                resultsTableHeader.append('</tr>');

                $.each(get_table(resultsList), function(index, value){
                    resultsTable.append(value)
                })
            })


            select_variable1.removeAttr('disabled')
            select_variable1.removeAttr('hidden')
            select_table1.removeAttr('disabled')
            select_table1.removeAttr('hidden')
            queryInput.removeAttr('disabled')
            queryInput.removeAttr('hidden')
            submitButton.removeAttr('disabled')
            submitButton.removeAttr('hidden')
            tableV.removeAttr('hidden')
            tableV.attr('border', '1')
        }

    function get_table(data) {
        let result = []
        for(let row of data) {
            result.push('<tr>');
            for(let cell of row){
                result.push(`<td>${cell}</td>`);
            }
            result.push('</tr>');
        }
        //console.log(result)
        return result;
        }

        function onQueryChange(){
            submitButton.removeAttr('disabled')
            submitButton.removeAttr('hidden')
        }
        function getUpdatedSettings() {
            // data to send back to the server
            var send = {table: select_table1.val(),};
            console.log(send)
            // make the selections disabled while fetching new data
            select_variable1.attr('disabled', true);
            select_table1.attr('disabled', true);
            orderSelect.attr('disabled', true)
            
            $.getJSON("/_get_table_values", send, function(response) {
                // this send the room and the day select vals to the URL specified
                // we will need to add a handler for this in Flask

                // for the purpose of the example I am assuming the response will be
                // a JSON object that has a dictionary of elements ("am_1" and "am_2")
                // each of which is a list of values for the selects....

                //console.log(response); // good for QA!

                // populate 1am
                select_variable1.empty();
                query_variable.empty();
                $.each(response.variables, function (index, value) {
                    select_variable1.append($('<option>', {value: value, text: value}, '</option>'));
                    query_variable.append($('<option>', {value: value, text: value}, '</option>'));
                    if (isMulti == false){
                        groupSelect.empty()
                        orderSelect.empty()
                        groupSelect.append($('<option>', {value:"None", text:"No Grouping"}));
                        orderSelect.append($('<option>', {value:"None", text:"No Grouping"}));
                        groupSelect.append($('<option>', {value: value, text: value}, '</option>'))
                        orderSelect.append($('<option>', {value: value, text: value}, '</option>'))
                    }
                });
                select_variable1.append($('<option>', {value:"*", text:"*"}));
                // remove disabled now
                select_variable1.removeAttr('disabled');
                select_table1.removeAttr('disabled')
                variable_label.removeAttr('hidden')
                select_variable1.removeAttr('hidden')
            });
        }
        
        function fetchValues(tableName, toggle) {
            var send = {table: tableName}
            console.log(send)   
            var returnData;
            if (toggle == "order"){
                orderSelect.empty()
                orderSelect.append($('<option>', {value:"None", text:"No Order"}));
                $.getJSON("/fetchValue", send, function(response){
                    $.each(response.variables, function (index, value) {
                        orderSelect.append($('<option>', {value: value, text: value}, '</option>'));
                    });
                })
            } else {
                    groupSelect.empty()
                    groupSelect.append($('<option>', {value:"None", text:"No Grouping"}));
                    $.getJSON("/fetchValue", send, function(response){
                        groupSelect.append($('<option>', {value: value, text: value}, '</option>'));
                    });
            };
            $.getJSON("/fetchValue", send, function(response){
                returnData = response.variables
            })     
            return returnData
        }
    });