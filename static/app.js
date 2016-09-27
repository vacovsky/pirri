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
        $scope.stations = undefined;

        // $scope.publishChange = function() {
        //     var queryString = "";
        //     $http.get('/send?' + queryString)
        //     .success(function(data, status, headers, config) {
        //     })
        //     .error(function(data, status, headers, config) {})
        // };

        $scope.loadStations = function() {
            $http.get('/station/list')
            .success(function(data, status, headers, config) {
                $scope.stations = data.stations;
            })
            .error(function(data, status, headers, config) {})
        };

        $scope.loadStations();
    });
})();