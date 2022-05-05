function addClass(item, clazz) {
    let text_element = document.getElementById(item);
    let prob_element = document.getElementById('P-' + item);
    text_element.classList.add(clazz);
    prob_element.classList.add(clazz);
}

function removeClass(item, clazz) {
    let text_element = document.getElementById(item);
    let prob_element = document.getElementById('P-' + item);
    text_element.classList.remove(clazz);
    prob_element.classList.remove(clazz);
}

function setProbabilities(probabilities) {
    for (item of probabilities)
    {
        let prob_element = document.getElementById('P-' + item['secondary']);
        prob = Math.round(item['result'] * 1000) / 1000
        prob_element.value = prob
    }
}

app.controller("documentClassifyCtrl", function ($scope, $http) {
    $scope.lang = '<B>Language: </B><I>UNKNOWN</I>';
    $scope.theInitialText = '';
    $scope.theText = '';
    $scope.theProperties = [];
    $scope.theComparisonClauses = [];
    $scope.theTemplateClauses = [];
    $scope.theComparison = [];
    $scope.matchChart = null

    $scope.redValue = 70;
    $scope.amberValue = 80;
    $scope.greenValue = 90;

    $scope.options = {
        makeAlpha : false,
        removeSpace : false,
        removeStop : false,
        toLemma : false,
        removeDuplicates : false,
        expand : false,
        toLower : false
    }

    $scope.executeCleanUp = function() {
        if ($scope.options.makeAlpha) $scope.makeAlphaNumeric()
        if ($scope.options.removeSpace) $scope.removeWhite()
        if ($scope.options.toLower) $scope.toLower()
    }

    $scope.removeWhite = function () {
        $scope.theText = $scope.theText.replace(/  +/g, ' ')
    }

    $scope.makeAlphaNumeric = function () {
        $scope.theText = $scope.theText.replace(/[^\n0-9a-zA-Z?!. ,;:-]/g, '')
    }

    $scope.toLower = function () {
        $scope.theText = $scope.theText.toLowerCase()
    }

    $scope.getBestMatch = function (relevantResults) {
        // Delete any existing chart
        if ($scope.matchChart != null) $scope.matchChart.destroy()
        theData = []
        theLabels = []
        for (result of relevantResults)
        {
            theData.push(result['result'] * 100)
            theLabels.push(result['secondary'])
        }
        const ctx = document.getElementById('best-match').getContext('2d');
        $scope.matchChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: theLabels,
                datasets: [{
                    label: '% Match',
                    data: theData,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    $scope.revert = function() {
        $scope.theText = $scope.theInitialText
    }

    $scope.detectLanguage = function() {
        const target_url = "/api/v1.0/data/language";
        const method = "POST";
        $http({
            method: method,
            url: target_url,
            data: $scope.theText,
            headers: {
                'Content-Type': undefined
            }
        }).then(function successCallback(response) {
            $scope.lang = '<B>Language: </B><I>' + response.data.longname + '</I>';
        }, function errorCallback(response) {
            showFailure(response);
        });
    }

    $scope.deleteClause = function (id) {
        $scope.theComparisonClauses = $scope.theComparisonClauses.filter(function (value, index, arr) {
            return value.id != id;
        })
    }

    $scope.addClause = function (id) {
        let i = 0
        const newClause = {
            "id": uuidv4(),
            "value": ""
        }
        for (i = 0; i < $scope.theComparisonClauses.length; ++i) {
            if ($scope.theComparisonClauses[i].id == id) {
                break
            }
        }
        $scope.theComparisonClauses.splice(i, 0, newClause);
    }

    $scope.combineWithClauseAbove = function (id) {
        let i = 0
        for (i = 0; i < $scope.theComparisonClauses.length; ++i) {
            if ($scope.theComparisonClauses[i].id == id) {
                break
            }
        }
        if (i == 0) return
        $scope.theComparisonClauses[i - 1].value = $scope.theComparisonClauses[i - 1].value + " " + $scope.theComparisonClauses[i].value
        $scope.deleteClause(id)
    }

    $scope.combineWithClauseBelow = function (id) {
        let i = 0
        for (i = 0; i < $scope.theComparisonClauses.length; ++i) {
            if ($scope.theComparisonClauses[i].id == id) {
                break
            }
        }
        if (i > $scope.theComparisonClauses.length - 1) return
        $scope.theComparisonClauses[i + 1].value = $scope.theComparisonClauses[i + 1].value + " " + $scope.theComparisonClauses[i].value
        $scope.deleteClause(id)
    }

    $scope.clauseFocus = function (id) {
        relevantResults = $scope.theComparison.filter(function (value, index, arr) {
            return value['primary'] == id;
        })
       
        setProbabilities(relevantResults)
        $scope.getBestMatch(relevantResults)
        for (result of relevantResults)
        {
            removeClass(result['secondary'], "iris-green-border")
            removeClass(result['secondary'], "iris-amber-border")
            removeClass(result['secondary'], "iris-red-border")

            if (result['result'] * 100 > $scope.greenValue)
            {
                addClass(result['secondary'], "iris-green-border")
            }
            else if (result['result'] * 100 > $scope.amberValue)
            {
                addClass(result['secondary'], "iris-amber-border")
            }
            else if (result['result'] * 100 > $scope.redValue)
            {
                addClass(result['secondary'], "iris-red-border")
            }
        }
    }

    $scope.uploadComparisonData = function () {
        if (document.getElementById("comparisonFileUploadInput").files.length == 0) {
            return;
        }
        let theFile = document.getElementById("comparisonFileUploadInput").files[0];
        const file_url = tika_base + "/tika/gettext?type=content";
        if (theFile != null) $scope.uploadComparisonFileToUrl(theFile, file_url);
    }

    $scope.uploadComparisonFileToUrl = function (file, target_url) {
        let form_data = new FormData();
        form_data.append("file", file);

        const method = "POST";
        $http({
            method: method,
            url: target_url,
            data: form_data,
            headers: {
                'Content-Type': undefined
            }
        }).then(function successCallback(response) {
            $scope.readComparisonClauses(response.data.result);
        }, function errorCallback(response) {
            showFailure(response);
        });
    }

    $scope.readComparisonClauses = function (theText) {
        const target_url = tika_base + "/nlp/clauses";
        const method = "POST";
        $http({
            method: method,
            url: target_url,
            data: theText,
            headers: {
                'Content-Type': undefined
            }
        }).then(function successCallback(response) {
            $scope.theTemplateClauses = response.data;
            $scope.doCompare()
        }, function errorCallback(response) {
            showFailure(response);
        });
    }

    $scope.doCompare = function () {
        const target_url = "/api/v1.0/comparelist";
        const method = "POST";
        let body = {}
        body['primary'] = $scope.theTemplateClauses
        body['secondary'] = $scope.theComparisonClauses
        $http({
            method: method,
            url: target_url,
            data: body,
            headers: {
                'Content-Type': "application/json"
            }
        }).then(function successCallback(response) {
            $scope.theComparison = response.data
        }, function errorCallback(response) {
            showFailure(response);
        });
    }


    $scope.dumpClausesToDocument = function () {
        let paragraphs = []
        for (clause of $scope.theComparisonClauses) {
            paragraphs.push(clause.value)
        }

        let element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(paragraphs.join("\n\n")));
        element.setAttribute('download', 'document.txt');

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    }

    $scope.readClauses = function () {
        const target_url = tika_base + "/nlp/clauses";
        const method = "POST";
        $http({
            method: method,
            url: target_url,
            data: $scope.theText,
            headers: {
                'Content-Type': undefined
            }
        }).then(function successCallback(response) {
            $scope.theComparisonClauses = response.data;
        }, function errorCallback(response) {
            showFailure(response);
        });
    }

    $scope.uploadOCRData = function () {
        if (document.getElementById("singleFileUploadInput").files.length == 0) {
            return;
        }
        let theFile = document.getElementById("singleFileUploadInput").files[0];
        const file_url = tika_base + "/tika/gettext?type=content";
        if (theFile != null) $scope.uploadFileToUrl(theFile, file_url);
    };

    $scope.uploadFileToUrl = function (file, target_url) {
        let form_data = new FormData();
        form_data.append("file", file);

        const method = "POST";
        $http({
            method: method,
            url: target_url,
            data: form_data,
            headers: {
                'Content-Type': undefined
            }
        }).then(function successCallback(response) {
            $scope.theInitialText = response.data.result;
            $scope.theText = response.data.result;
            $scope.detectLanguage()
            $scope.setProperties(response.data.properties)
        }, function errorCallback(response) {
            showFailure(response);
        });
    }

    $scope.setProperties = function (properties) {
        $('#theproperties').DataTable().destroy();
        $('#theproperties')
            .DataTable({
                "data": properties,
                "columns": [
                    { "data": "key" },
                    { "data": "value" }]
            })
    };

});
