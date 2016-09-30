(function() {
    var app = angular.module('pirriweb', ['chart.js']);
    app.Root = '/';
    app.config(['$interpolateProvider',
        function($interpolateProvider) {
            $interpolateProvider.startSymbol('{[');
            $interpolateProvider.endSymbol(']}');
        }
    ]); 

    app.controller('PirriControl', function ($rootScope, $scope, $http) {
        $scope.chartData1 = {};
        $scope.chartData2 = {};

        $scope.currentPage = 'home'; // history / home / settings / add
        $scope.stations = undefined;
        $scope.navTitle = "All Stations";
        $scope.showHome = true;
        $scope.showAdd = false;
        $scope.showEditStation = false;
        $scope.gpio_pins = undefined;
        $scope.searchResults = {};
        $scope.searchText = "";
        $scope.showSearchResults = false;
        $scope.history = [];
        $scope.historyScope = "All Stations";
        $scope.schedule = undefined;
        $scope.gpio_add_model = {
            default_message: "Select GPIO",
            GPIO: undefined
        };
        $scope.edit_station_model = {
            SID: undefined,
            GPIO: undefined,
            notes: undefined
        };
        $scope.durationIntervals = [1,5,10,15,20,25,30,35,40,45,50,55,60];
        $scope.show_gpio_diagram = false;

        this.filterForKeys = function(searchText) {
            $scope.searchResults = [];
            $scope.stations.forEach(function(k) {
                var n = k.search(searchText);
                if (n >= 0) {
                    $scope.searchResults[k] = true;
                }
            });
            if (Object.keys($scope.searchResults).length > 0) {
                $scope.showSearchResults = true;
            } else {
                $scope.showSearchResults = false;
            }
            if (searchText === "") {
                $scope.searchResults = [];
                $scope.showSearchResults = false;
            }
        };

        this.resetAddForm = function() {
            $scope.gpio_add_model = {
                default_message: "Select GPIO", 
                GPIO: undefined
            };
        };

        this.setGPIO = function(gpio) {
            $scope.gpio_add_model.GPIO = gpio;
        };

        this.setEditingStationInfo = function(id, gpio, notes) {
            $scope.edit_station_model.SID = id;
            $scope.edit_station_model.GPIO = gpio;
            $scope.edit_station_model.notes = notes;
            console.log($scope.edit_station_model);
        };

        this.setPage = function(pageName) {
            $scope.currentPage = pageName;
            if ($scope.currentPage == 'home') {
                $scope.navTitle = "All Stations"
                $scope.stats = false;
                $scope.showEditStation = false;
                $scope.showEditSchedule = false;
                $scope.showHome = true;
                $scope.showHistory = false;
                $scope.showAdd = false;
                this.resetAddForm();
            }
            else if ($scope.currentPage == 'add') {
                $scope.stats = false;
                $scope.showEditSchedule = false;
                $scope.showEditStation = false;
                $scope.navTitle = "Add a Station"
                $scope.showAdd = true;
                $scope.showHistory =false;
                $scope.showHome = false;
                this.resetAddForm();
            }
            else if ($scope.currentPage == 'calendar') {
                $scope.stats = false;
                $scope.showEditSchedule = true;
                $scope.showEditStation = false;
                $scope.navTitle = "Schedule"
                $scope.showAdd = false;
                $scope.showHistory =false;
                $scope.showHome = false;
                this.resetAddForm();
            }
            else if ($scope.currentPage == 'editstation') {
                $scope.stats = false;
                $scope.navTitle = "Editing Station " + $scope.edit_station_model.SID + " - (" + $scope.edit_station_model.notes + ")";
                $scope.showEditSchedule = false;
                $scope.showEditStation = true;
                $scope.showAdd = false;
                $scope.showHistory =false;
                $scope.showHome = false;
                this.resetAddForm();
            }
            else if ($scope.currentPage == 'history') {
                this.loadHistory(0);
                $scope.stats = false;
                $scope.showEditSchedule = false;
                $scope.navTitle = "Watering History"
                $scope.showEditStation = false;
                $scope.showHistory = true;
                $scope.showAdd = false;
                $scope.showHome = false;
                this.resetAddForm();
            }
            else if ($scope.currentPage == 'stats') {
                this.loadStatsData();
                $scope.stats = true;
                $scope.showEditSchedule = false;
                $scope.navTitle = "Usage Stats"
                $scope.showEditStation = false;
                $scope.showHistory = false;
                $scope.showAdd = false;
                $scope.showHome = false;
                this.resetAddForm();
            }
            //console.log($scope.currentPage)
        };

        
        this.getUsageDataForChart1 = function() {
            $http.get('/stats?id=1')
            .success(function(data, status, headers, config) {
                $scope.chartData1.labels = data.chartData.labels;
                $scope.chartData1.series = data.chartData.series;
                $scope.chartData1.data = data.chartData.data;
            })
            .error(function(data, status, headers, config) {})

            console.log($scope.chartData1)
            $scope.chartData1.options = {
                
            };
        };

        this.loadStatsData = function() {
            //Chart.defaults.global.colors = [ '#803690', '#00ADF9', '#DCDCDC', '#46BFBD', '#FDB45C', '#949FB1', '#4D5360'];
            this.getUsageDataForChart1();
        };
        


        this.submitEditStation = function() {
        };
        this.submitDeleteStation = function() {
        };
        this.submitAddStation = function() {
        };

        $scope.scheduleModel = {};
        this.submitAddSchedule = function() {
        };
        this.submitEditSchedule = function() {
            //stuff
            $http.post('/schedule', $scope.scheduleModel)
            .success(function(data, status, headers, config) {
                console.log($scope.scheduleModel, data)
            })
            .error(function(data, status, headers, config) {})
            // cleanup
            $scope.scheduleModel = {};
            $scope.scheduleModel = undefined;
            this.getSchedule();
        };
        this.mapModelForSchedEdit = function(currentModel) {
            $scope.scheduleModel = currentModel;
            console.log($scope.scheduleModel)
        };


        this.submitDeleteSchedule = function() {
        };

        $scope.singleRunModel = {};
        this.submitSingleRun = function() {
            //stuff
            $http.post('/station/run', $scope.singleRunModel)
            .success(function(data, status, headers, config) {
                console.log($scope.singleRunModel, data)
            })
            .error(function(data, status, headers, config) {})
            // cleanup
            $scope.singleRunModel = {};
            $scope.singleRunMinField = undefined;
        };


        this.loadStations = function() {
            $http.get('/station/list')
            .success(function(data, status, headers, config) {
                $scope.stations = data.stations;
            })
            .error(function(data, status, headers, config) {})
        };

        this.loadGPIO = function() {
            $http.get('/gpio/list')
            .success(function(data, status, headers, config) {
                $scope.gpio_pins = data.gpio_pins;
            })
            .error(function(data, status, headers, config) {})
        };

        this.loadHistory = function(station) {
            var query = '?station=' + station + '&earliest=-168';
            $http.get('/history' + query)
            .success(function(data, status, headers, config) {
                $scope.history = data.history;
            })
            .error(function(data, status, headers, config) {})
        };

        this.prettyTime = function(uglyTime) {
            var pt = moment(uglyTime).calendar();
            return pt
        }
        this.getSchedule = function() {
            $http.get('/schedule')
            .success(function(data, status, headers, config) {
                $scope.schedule = data.schedule;
            })
            .error(function(data, status, headers, config) {})
        };

        this.getSchedule();
        this.loadStations();
        this.loadGPIO();
    });
})();