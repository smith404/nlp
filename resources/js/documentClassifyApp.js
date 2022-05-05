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
    for (item of probabilities) {
        let prob_element = document.getElementById('P-' + item['secondary']);
        prob = Math.round(item['result'] * 1000) / 1000
        prob_element.value = prob
    }
}

app.controller("documentClassifyCtrl", function ($scope, $http) {
    $scope.lang = '<B>Language: </B><I>UNKNOWN</I>';
    $scope.theInitialText = '';
    $scope.comparisonClause = '';
    $scope.theText = '';
    $scope.theProperties = [];
    $scope.theComparisonClauses = [];
    $scope.theTemplateClauses = [];
    $scope.theComparison = [];
    $scope.matchChart = null
    $scope.guageChart = null

    $scope.redValue = 70;
    $scope.amberValue = 80;
    $scope.greenValue = 90;

    $scope.options = {
        makeAlpha: false,
        removeSpace: false,
        removeStop: false,
        toLemma: false,
        removeDuplicates: false,
        expand: false,
        toLower: false
    }

    $scope.compareParagraph = function () {
        $scope.theTemplateClauses = []
        let clause = {}
        clause['id'] = 'user-clause'
        clause['value'] = $scope.comparisonClause
        $scope.theTemplateClauses.push(clause);
        $scope.doCompare('user-clause')
    }

    $scope.executeCleanUp = function () {
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
        if ($scope.guageChart != null) $scope.guageChart.destroy()

        let theBestProbability = 0
        let theGuageData = []
        let theData = []
        let theLabels = []
        let theColors = []

        let index = 0
        for (result of relevantResults) {
            let actualValue = Math.round((result['result'] * 100))
            // Find the best match
            if (actualValue > theBestProbability) theBestProbability = actualValue
            theData.push((actualValue - 50) * 2)
            theLabels.push('Clause: ' + (++index))
            theColors.push(toColor(actualValue))
        }
        theGuageData.push(theBestProbability-1)
        theGuageData.push(1)
        theGuageData.push(100-theBestProbability-1)

        const bestMatchChart = {
            type: 'bar',
            data: {
                labels: theLabels,
                datasets: [{
                    label: '% Match',
                    data: theData,
                    borderWidth: 1,
                    backgroundColor: theColors
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    },
                        title: {
                        display: true,
                        text: 'Overall Match Statistics',
                        font: {
                            size: 18
                        }
                    }
                },
                scales: {
                    y: {
                        max: 100,
                        min: -100,
                        ticks: {
                            stepSize: 10
                        }
                    }
                }
            }
        }
        const ctx = document.getElementById('best-match-chart').getContext('2d');
        $scope.matchChart = new Chart(ctx, bestMatchChart);

        let guageChart = {
            type: 'doughnut',
            data: {
                labels: ["", "Probability", ""],
                datasets: [{
                    label: 'probability',
                    data: theGuageData,
                    backgroundColor: ["blue", "red", "lightgrey"]
                }]
            },
            options: {
                rotation: 270,
                circumference: 180,
                plugins: {
                    legend: {
                        display: false
                    },
                        title: {
                        display: true,
                        text: 'Estimated Match Likelihood',
                        font: {
                            size: 18
                        }
                    },
                    subtitle: {
                        display: true,
                        text: theBestProbability + '%',
                        font: {
                            size: 36
                        },
                        position: "bottom",
                        padding: {
                            bottom: 150
                        }
                    }
        
                }       
            }
        }

        const ctx2 = document.getElementById('guage-chart').getContext('2d');
        $scope.guageChart = new Chart(ctx2, guageChart);
    }

    $scope.revert = function () {
        $scope.theText = $scope.theInitialText
    }

    $scope.detectLanguage = function () {
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
        for (result of relevantResults) {
            removeClass(result['secondary'], "iris-green-border")
            removeClass(result['secondary'], "iris-amber-border")
            removeClass(result['secondary'], "iris-red-border")

            if (result['result'] * 100 > $scope.greenValue) {
                addClass(result['secondary'], "iris-green-border")
            }
            else if (result['result'] * 100 > $scope.amberValue) {
                addClass(result['secondary'], "iris-amber-border")
            }
            else if (result['result'] * 100 > $scope.redValue) {
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
            $scope.doCompare(null)
        }, function errorCallback(response) {
            showFailure(response);
        });
    }

    $scope.doCompare = function (element) {
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
            if (element != null) $scope.clauseFocus(element)
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
