var app = angular.module('MoviesApp', []);


app.controller('mainController', function($scope,$http) {

    $scope.selected = undefined;
    $scope.actors  = [
                        {name:"dan", year:1995},
                        {name:"tomer",year:1990},
                        {name:"dror",year:1780}];




});

