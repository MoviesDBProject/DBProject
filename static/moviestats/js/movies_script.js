var MoviesApp = angular.module('MoviesApp', ['ui.bootstrap']);

MoviesApp.controller('mainController', function($scope,$http,$window,$sce) {

    $scope.actors  = [
                        {name:"dan", year:1995, country: "Israel"},
                        {name:"tomer",year:1990, country: "USA"},
                        {name:"dror",year:1780, country: "UK"}
    ];

    $scope.countries = ["Afghanistan", "Albania", "Algeria",
        "American Samoa", "Angola", "Anguilla", "Antartica",
        "Antigua and Barbuda", "Argentina",
        "Armenia", "Aruba", "Ashmore and Cartier Island",
        "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
        "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia",
        "Bosnia and Herzegovina", "Botswana", "Brazil", "British Virgin Islands", "Brunei", "Bulgaria",
        "Burkina Faso", "Burma", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands",
        "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Clipperton Island", "Cocos (Keeling) Islands",
        "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire",
        "Croatia", "Cuba", "Cyprus", "Czeck Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt",
        "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Europa Island", "Falkland Islands (Islas Malvinas)",
        "Faroe Islands", "Fiji", "Finland", "France", "French Guiana", "French Polynesia", "French Southern and Antarctic Lands", "Gabon",
        "Gambia, The", "Gaza Strip", "Georgia", "Germany", "Ghana", "Gibraltar", "Glorioso Islands", "Greece", "Greenland", "Grenada",
        "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard Island and McDonald Islands",
        "Holy See (Vatican City)", "Honduras", "Hong Kong", "Howland Island", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
        "Ireland", "Ireland, Northern", "Israel", "Italy", "Jamaica", "Jan Mayen", "Japan", "Jarvis Island", "Jersey", "Johnston Atoll",
        "Jordan", "Juan de Nova Island", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos",
        "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia," +
        "Former Yugoslav Republic", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Man, Isle of", "Marshall Islands",
        "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia, Federated States of", "Midway Islands", "Moldova",
        "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles",
        "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway",
        "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcaim Islands", "Poland",
        "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romainia", "Russia", "Rwanda", "Saint Helena", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
        "Saudi Arabia", "Scotland", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
        "Somalia", "South Africa", "South Georgia and South Sandwich Islands", "Spain", "Spratly Islands", "Sri Lanka", "Sudan", "Suriname",
        "Svalbard", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Tobago", "Toga",
        "Tokelau", "Tonga", "Trinidad", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
        "United Kingdom", "Uruguay", "USA", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands", "Wales", "Wallis and Futuna",
        "West Bank", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"];


    $scope.languages = ["Hebrew","English","Arabic","French"];




    var results_element = document.getElementById("show_results");
    results_table.setAttribute("border", "1");

    $scope.results_cols = ["Actor", "Year", "Language"];
    $scope.results_contents = [{ actor: "Dror", year: "1990", language: "Hebrew"},
        { actor: "Tomer", year: "1990", language: "Hebrew"}];


    // Create YouTube playlist
    var youtube_id_list = ["JNfRQ4NBjUU", "X2i9Zz_AqTg"];
    var youtube_url_str = "https://www.youtube.com/embed/VIDEO_ID?playlist=";
    for (i = 0; i < youtube_id_list.length; i++){
        youtube_url_str = youtube_url_str + youtube_id_list[i];
        if (i < youtube_id_list.length - 1)
            youtube_url_str = youtube_url_str + ",";
    };
    $scope.youtube_url = $sce.trustAsResourceUrl(youtube_url_str);

    //document.getElementById("debug").innerHTML = $scope.results_cols.indexOf("Actor").toString();


    $scope.submit = function(){

        $http({
            url: "/fetch_results/",
            method: "POST",
            data: $scope.formData,
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        })
        .success(function(response){
            console.log(response);
            results_element.removeChild(document.getElementById("results_table"));
            var results_table = document.createElement("table");
            results_table.setAttribute("id", "results_table");
            results_element.appendChild(results_table);
        })
    };



});

