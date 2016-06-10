var MoviesApp = angular.module('MoviesApp', ['ui.bootstrap']);

MoviesApp.controller('mainController',['$scope','$http','$sce','$window', function($scope,$http,$sce,$window) {


    $scope.update = function(){


        $http({
            url: "/update/" ,
            method: "POST",
            data: {'token':'DbMysql03'},
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
           })
            .then(function (response) {
                if (response.data['status'] == "OK") {
                    window.alert("Update Request sent. Updating DB.");
                }
            },  function(response) {
                window.alert("Something went wrong.Update not done.")
            })

    };

    $scope.init = function(){
        var entries = ["actors","directors","language","country","genres"];

        for (var i=0; i<entries.length;i++) {
            $http({
            url: "/init_data/" ,
            method: "POST",
            data: {'entry':entries[i]},
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
           })
           .then(function successCallback(response) {
               var response_data = response.data;
               var entry = Object.keys(response_data[0])[0]
               switch (entry) {
               	   	
                   case "actor" :
                        $scope.actors = response_data;
                       break;
                   case "director" :
                        $scope.directors = response_data;
                       break;
                   case "language" :
                       $scope.languages = response_data;
                       break;
                   case "country" :
                       $scope.countries = response_data;
                       break;
                   case "genre" :
                       $scope.genres = response_data;
                   default:
                       break;
               }
           },
           function errorCallback(response){
               window.alert("Something went wrong");
               var landingUrl = "http://" + $window.location.host;
               $window.location.href = landingUrl;
           })
        }};

    $scope.init();

    $scope.createYouTubePlaylist = function(youtube_id_list){
        //var youtube_id_list = ["JNfRQ4NBjUU", "X2i9Zz_AqTg"];
        var youtube_url_str = "https://www.youtube.com/embed/VIDEO_ID?playlist=";
        for (var i = 0; i < youtube_id_list.length; i++){
            youtube_url_str = youtube_url_str + youtube_id_list[i];
            if (i < youtube_id_list.length - 1) {
                youtube_url_str += ",";
            }
        };
        return $sce.trustAsResourceUrl(youtube_url_str);

    };

    $scope.submit = function(){
    	
    	  console.log($scope.formData)

        $http({
            url: "/fetch_results/",
            method: "POST",
            data: $scope.formData,
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        })
        .then(function(response){
            $scope.results_contents = response.data; 
            $scope.ret_length = $scope.results_contents.length
            console.log(response.data)
            if (response.data.length === 0) {
                $scope.disable_next_button();
                $scope.disable_previous_button();
            	document.getElementById('show_results').innerHTML = "<h1>No corresponding movies found.</h1><h2><a href='/'>Try another search.</a></h2>"
            } 
            else {
                $scope.show_item = 0;

            	var id_list = function(data) {
                                var lst = [];
                                for (var i=0 ; i<data.length;i++){
                                    lst.push(data[i]["youtube_id"]);
                                }
                                return lst;
                            }($scope.results_contents);
            	document.getElementById('youtube_iframe').src = $scope.createYouTubePlaylist(id_list);;
            	
         	}
         	$scope.showResults = true;

        } , function errorCallback(response){
        			window.alert("Something went wrong");
               var landingUrl = "http://" + $window.location.host;
               $window.location.href = landingUrl;
               
           })
    };

    /* Trailer and its description related functions */
    
    
    $scope.showResults = false;
    $scope.results_contents=[];
    $scope.ret_length;


    $scope.click_next = function(){
        $scope.show_item++;
    };

    $scope.click_previous = function() {
        $scope.show_item--;
    };

    $scope.show_item = 0;




}]);

