(function() {
    var app = angular.module('pirriweb', []);
    app.Root = '/';
    app.config(['$interpolateProvider',
        function($interpolateProvider) {
            $interpolateProvider.startSymbol('{[');
            $interpolateProvider.endSymbol(']}');
        }
    ]); 

    app.controller('PirriControl', function ($rootScope, $scope, $http) {
        $scope.currentPage = 'home'; // history / home / settings / add
        $scope.stations = undefined;
        $scope.navTitle = "All Stations"
        $scope.showHome = true;
        $scope.showAdd = false;
        $scope.gpio_pins = undefined;
        $scope.searchResults = {};
        $scope.searchText = "";
        $scope.showSearchResults = false;
        $scope.history = [];
        $scope.historyScope = "All Stations"
        $scope.gpio_add_model = {
            default_message: "Select GPIO",
            GPIO: undefined
        };
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

        // $scope.publishChange = function() {
        //     var queryString = "";
        //     $http.get('/send?' + queryString)
        //     .success(function(data, status, headers, config) {
        //     })
        //     .error(function(data, status, headers, config) {})
        // };
        this.resetAddForm = function() {
            $scope.gpio_add_model = {
                default_message: "Select GPIO", 
                GPIO: undefined
            };
        };

        this.setGPIO = function(gpio) {
            $scope.gpio_add_model.GPIO = gpio;
        };

        this.setPage = function(pageName) {
            $scope.currentPage = pageName;
            if ($scope.currentPage == 'home') {
                $scope.navTitle = "All Stations"
                $scope.showHome = true;
                $scope.showHistory = false;
                $scope.showAdd = false;
                this.resetAddForm();
            }
            else if ($scope.currentPage == 'add') {
                $scope.navTitle = "Add a Station"
                $scope.showAdd = true;
                $scope.showHistory =false;
                $scope.showHome = false;
                this.resetAddForm();
            }
            else if ($scope.currentPage == 'history') {
                this.loadHistory(0);
                $scope.navTitle = "Watering History"
                $scope.showHistory = true;
                $scope.showAdd = false;
                $scope.showHome = false;
                this.resetAddForm();
            }
            console.log($scope.currentPage)
        };

        this.settingsPage = function(sid) {

        };

        this.historyPage = function(sid) {

        }

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
            //console.log(pt);
            return pt
        }
        this.loadStations();
        this.loadGPIO();
    });
})();