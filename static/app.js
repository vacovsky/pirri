(function() {
    var app = angular.module('pirriweb', ['chart.js']);
    app.Root = '/';
    app.config(['$interpolateProvider',
        function($interpolateProvider) {
            $interpolateProvider.startSymbol('{[');
            $interpolateProvider.endSymbol(']}');
        }
    ]);

    app.controller('PirriControl', function($rootScope, $scope, $http, $timeout, $filter) {
        $rootScope.updateInterval = 6000;
        $scope.chartData1 = {};
        $scope.chartData2 = {
            options: {}
        };

        $scope.randomColor = function() {
            var letters = '0123456789ABCDEF';
            var color = '#';
            for (var i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        };

        $scope.calEvents = []
        this.getCalEvents = function() {
            $http.get('/schedule/cal')
                .success(function(data, status, headers, config) {
                   $scope.calEvents = data.schedule;
                   //$scope.$apply();
                })
                .error(function(data, status, headers, config) {})
                console.log($scope.calEvents)
                //loadCalendar();
        };

        $scope.currentPage = 'home'; // history / home / settings / add
        $scope.stations = undefined;
        $scope.navTitle = "All Stations";
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
        $scope.durationIntervals = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60];
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

        this.setEditingStationInfo = function(station) {
            $scope.stationModel = station;
            // console.log($scope.stationModel);
        };


        $scope.currentPage = 0;
        this.setPage = function(pageName) {
            $scope.currentPage = pagename
        };


        $scope.dripnodes = {};
        $scope.watercost = 0.0021;
        this.getWaterUsageStats = function() {
            $http.get('/stats/gallons')
                .success(function(data, status, headers, config) {
                    $scope.dripnodes = data.water_usage;
                })
                .error(function(data, status, headers, config) {})
            this.getWaterNodeEntries();
        };

        this.getUsageDataForChart1 = function() {
            $http.get('/stats?id=1')
                .success(function(data, status, headers, config) {
                    $scope.chartData1.labels = data.chartData.labels;
                    $scope.chartData1.series = data.chartData.series;
                    $scope.chartData1.data = data.chartData.data;
                })
                .error(function(data, status, headers, config) {})

            // console.log($scope.chartData1)
            $scope.chartData1.options = {
                title: {
                    display: true,
                    text: 'Total Usage in Minutes (last 30 days)'
                },
                scaleStartValue: 0,
                legend: {
                    display: true,
                    labels: {
                        //fontColor: 'rgb(255, 99, 132)'
                    }
                },
            };
        };

        $scope.monthly_cost = 0;
        this.calcMonthlyCost = function() {
            $scope.monthly_cost = 0;
            angular.forEach($scope.dripnodes, function(value, key) {
                $scope.monthly_cost += value['usage_last_30'] * $scope.watercost
            })
        };

        this.getUsageDataForChart2 = function() {
            $http.get('/stats?id=2')
                .success(function(data, status, headers, config) {
                    $scope.chartData2.labels = data.chartData.labels;
                    $scope.chartData2.series = data.chartData.series;
                    $scope.chartData2.data = data.chartData.data;
                })
                .error(function(data, status, headers, config) {})
                // console.log($scope.chartData2);
            $scope.chartData2.options = {
                scaleStartValue: 0,
                title: {
                    display: true,
                    text: 'Usage in Minutes by Day of Week (last 7 days)'
                },
                scaleStartValue: 0,
                legend: {
                    display: true,
                    labels: {
                        //fontColor: 'rgb(255, 99, 132)'
                    }
                },
            };
        };

        this.loadStatsData = function() {
            Chart.defaults.global.defaultFontColor = "#fff";
            this.getUsageDataForChart1();
            this.getUsageDataForChart2();

        };


        $scope.stationModel = {}
        this.submitEditStation = function() {
            $http.post('/station/edit', $scope.stationModel)
                .success(function(data, status, headers, config) {
                    // console.log($scope.singleRunModel, data)
                })
                .error(function(data, status, headers, config) {})
                // cleanup
            $scope.stationModel = {};
            $scope.stationModel = undefined;
        };
        this.submitDeleteStation = function() {};
        this.submitAddStation = function() {};

        $scope.scheduleModel = {};

        this.addScheduleButton = function() {
            $scope.scheduleModel = undefined;
            $scope.scheduleModel = {
                id: 0,
                sunday: false,
                monday: false,
                tuesday: false,
                wednesday: false,
                thursday: false,
                friday: false,
                saturday: false,
                repeat: false,
                station: undefined,
                starttime: undefined,
                startdate: undefined,
                enddate: 30000000,
                duration: 0,
                new: true
            };
            // console.log($scope.scheduleModel)
            $scope.schedule.unshift($scope.scheduleModel)
        };

        this.addScheduleButtonFromCalendar = function(startTime) {
            $scope.scheduleModel = undefined;
            $scope.scheduleModel = {
                id: 0,
                sunday: false,
                monday: false,
                tuesday: false,
                wednesday: false,
                thursday: false,
                friday: false,
                saturday: false,
                repeat: false,
                station: undefined,
                starttime: undefined,
                startdate: undefined,
                enddate: 30000000,
                duration: 0,
                new: true
            };
            $scope.currentPage = 'calendar';

            // console.log($scope.scheduleModel)
            $scope.schedule.unshift($scope.scheduleModel)
        };

        this.convertScheduleBoolToInt = function() {
            if ($scope.scheduleModel.sunday) {
                $scope.scheduleModel.sunday = 1;
            } else {
                $scope.scheduleModel.sunday = 0;
            }
            if ($scope.scheduleModel.monday) {
                $scope.scheduleModel.monday = 1;
            } else {
                $scope.scheduleModel.monday = 0;
            }
            if ($scope.scheduleModel.tuesday) {
                $scope.scheduleModel.tuesday = 1;
            } else {
                $scope.scheduleModel.tuesday = 0;
            }
            if ($scope.scheduleModel.wednesday) {
                $scope.scheduleModel.wednesday = 1;
            } else {
                $scope.scheduleModel.wednesday = 0;
            }
            if ($scope.scheduleModel.thursday) {
                $scope.scheduleModel.thursday = 1;
            } else {
                $scope.scheduleModel.thursday = 0;
            }
            if ($scope.scheduleModel.friday) {
                $scope.scheduleModel.friday = 1;
            } else {
                $scope.scheduleModel.friday = 0;
            }
            if ($scope.scheduleModel.saturday) {
                $scope.scheduleModel.saturday = 1;
            } else {
                $scope.scheduleModel.saturday = 0;
            }
            if ($scope.scheduleModel.repeat) {
                $scope.scheduleModel.repeat = 1;
            } else {
                $scope.scheduleModel.repeat = 0;
            }
        };
        this.submitEditSchedule = function() {
            this.convertScheduleBoolToInt();
            $http.post('/schedule/edit', $scope.scheduleModel)
                .success(function(data, status, headers, config) {
                    // console.log($scope.scheduleModel, data)
                })
                .error(function(data, status, headers, config) {})
                // cleanup
            $scope.scheduleModel = {};
            $scope.scheduleModel = undefined;
            this.refresh();
        };

        this.submitAddSchedule = function() {
            this.convertScheduleBoolToInt();
            $http.post('/schedule/add', $scope.scheduleModel)
                .success(function(data, status, headers, config) {
                    // console.log($scope.scheduleModel, data)
                })
                .error(function(data, status, headers, config) {})
                // cleanup
            $scope.scheduleModel = {};
            $scope.scheduleModel = undefined;
            this.refresh();
        };

        this.mapModelForSchedEdit = function(currentModel) {
            $scope.scheduleModel = currentModel;
            // console.log($scope.scheduleModel)
        };

        this.mapModelForSchedEditFromCalClick = function(id) {
            $scope.currentPage = 'calendar';
            console.log($scope.currentPage);
            var sch = $filter('filter')($scope.schedule, {id: id })[0];
            $scope.scheduleModel = sch;
            // console.log($scope.scheduleModel)
        };

        this.submitDeleteSchedule = function(schedule_id) {
            $http.post('/schedule/delete', {
                    schedule_id: schedule_id
                })
                .success(function(data, status, headers, config) {
                    // console.log('deleted schedule id: ', schedule_id)
                })
                .error(function(data, status, headers, config) {})
                // cleanup
            $scope.scheduleModel = {};
            $scope.scheduleModel = undefined;
            this.refresh();
        };

        $scope.singleRunModel = {};
        this.submitSingleRun = function() {
            //stuff
            $http.post('/station/run', $scope.singleRunModel)
                .success(function(data, status, headers, config) {
                    // console.log($scope.singleRunModel, data)
                })
                .error(function(data, status, headers, config) {})
                // cleanup
            $scope.singleRunModel = {};
            $scope.singleRunMinField = undefined;
        };

        this.refresh = function() {
            this.getSchedule();
            this.loadStations();
            this.getLastStationRun();
            this.getNextStationRun();
            this.loadGPIO();
            this.loadStatsData();
            this.getWaterUsageStats();
        };
        this.loadStations = function() {
            $http.get('/station/list')
                .success(function(data, status, headers, config) {
                    $scope.stations = data.stations;
                    angular.forEach($scope.stations, function(value, key) {
                        value['cal_color'] = $scope.randomColor();
                    })
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
            if (uglyTime !== undefined && uglyTime !== null) {
                // console.log(uglyTime)
                var pt = moment(uglyTime).calendar();
                return pt
            } else {
                return "Never"
            }
        }
        this.getSchedule = function() {
            $http.get('/schedule')
                .success(function(data, status, headers, config) {
                    $scope.schedule = data.schedule;
                })
                .error(function(data, status, headers, config) {})
        };

        $scope.lastStationRunHash = {}
        this.getLastStationRun = function() {
            $http.get('/station/lastruns')
                .success(function(data, status, headers, config) {
                    $scope.lastStationRunHash = data.lastrunlist;
                })
                .error(function(data, status, headers, config) {})
                // console.log($scope.lastStationRunHash);
        };

        $scope.nextStationRunHash = {}
        this.getNextStationRun = function() {
            $http.get('/station/nextruns')
                .success(function(data, status, headers, config) {
                    $scope.nextStationRunHash = data.nextrunlist;
                })
                .error(function(data, status, headers, config) {})
                // console.log($scope.nextStationRunHash);
        };

        $scope.waterNodeEntries = [];
        $scope.waterNodeModel = {};
        this.getWaterNodeEntries = function() {
            $http.get('/station/nodes')
                .success(function(data, status, headers, config) {
                    $scope.waterNodeEntries = data.dripnodes;
                })
                .error(function(data, status, headers, config) {})
                // console.log($scope.nextStationRunHash);
        }
        this.submitEditNodeEntry = function() {
            $http.post('/station/nodes', $scope.waterNodeModel)
                .success(function(data, status, headers, config) {
                    // console.log($scope.singleRunModel, data)
                })
                .error(function(data, status, headers, config) {})
                // cleanup
            $scope.waterNodeModel = undefined;
            $scope.waterNodeModel = {};
        };

        this.submitAddNodeEntry = function() {
            $scope.waterNodeModel.new = true;
            $http.post('/station/nodes', $scope.waterNodeModel)
                .success(function(data, status, headers, config) {
                    // console.log($scope.singleRunModel, data)
                })
                .error(function(data, status, headers, config) {})
                // cleanup
            $scope.waterNodeModel = undefined;
            $scope.waterNodeModel = {};
        };

        this.submitDeleteNodeEntry = function(nodeid) {
            $scope.waterNodeModel.id = nodeid;
            $http.post('/station/nodes/delete', $scope.waterNodeModel)
                .success(function(data, status, headers, config) {
                    // console.log($scope.singleRunModel, data)
                })
                .error(function(data, status, headers, config) {})
                // cleanup
            $scope.waterNodeModel = undefined;
            $scope.waterNodeModel = {};
        };

        this.mapModelForWaterNodeEdit = function(currentModel) {
            $scope.waterNodeModel = currentModel;
            // console.log($scope.scheduleModel)
        };

        this.addWaterNodeButton = function() {
            $scope.waterNodeModel = undefined;
            $scope.waterNodeModel = {
                id: '-',
                sid: 'Select Station ID',
                gph: '',
                count: 0,
                new: true
            };
            // console.log($scope.scheduleModel)
            $scope.waterNodeEntries.unshift($scope.waterNodeModel)
        };

        this.autoLoader = function() {
            this.getCalEvents();
            this.getSchedule();
            this.loadStations();
            this.getLastStationRun();
            this.getNextStationRun();
            this.loadGPIO();
            this.loadStatsData();
            this.loadHistory();
            this.calcMonthlyCost();
        };
        $scope.loader = this.autoLoader;
        $scope.currentPage = 'home';
        // $scope.intervalFunction = function() {
        //     $timeout(function() {
        //         $scope.loader();
        //         $scope.intervalFunction();
        //     }, $rootScope.updateInterval)
        // };
        //$scope.intervalFunction();

        this.autoLoader();

    });
})();