var n = 0;
var currentData;
var length;

var currentPage = 1;
var currentPageBox = document.getElementById("pageBox5");
var pageTotal;

var num = 0;
var coursesInCart = [];
var creditTotal = 0;

$.ajax({
    type: "POST",
    url: route,
    data: { "initialized": "1" }
}).done(function (response) {
    if (route == "/catalog") {
        currentData = response; n = 0; currentPage = 1;
        display(JSON.parse(currentData));
    } else if (route == "/student") {
        currentData = response['data']; n = 0; currentPage = 1;
        display(JSON.parse(response['data']))

        try {
            responseCart = JSON.parse(response['cart'])

            var subKeys = Object.keys(responseCart['ID']);

            for (var i = 0; i < subKeys.length; i++) {
                var nameLong = responseCart["longDescription"][subKeys[i]];
                //console.log(nameLong);
                coursesInCart[i] = nameLong;
                splitName = nameLong.split(" ");
                if (splitName[0] == 'HONORS') {
                    splitName.shift()
                } else if (splitName[0] == 'ADVANCED' && splitName[1] == 'PLACEMENT') {
                    splitName.shift()
                    splitName.shift()
                }

                var nameShort = ""
                for (var k = 0; k < splitName.length; k++) {
                    nameShort += splitName[k];
                    if (k != splitName.length - 1) nameShort += " ";
                }

                if (nameShort.length > 13) {
                    nameShort = nameShort.substring(0, 10) + "...";
                }


                var templ = document.getElementById("courseInCart");
                var creditsNum = responseCart['credits'][subKeys[i]];
                var credits = parseInt(creditsNum);

                creditTotal += credits;

                templ.innerHTML = templ.innerHTML.replace("##classID##", "class" + num);
                templ.innerHTML = templ.innerHTML.replace("##classname##", nameShort);
                templ.innerHTML = templ.innerHTML.replace("##removeID##", "remove" + num);
                templ.innerHTML = templ.innerHTML.replace("##classNME##", nameLong);
                templ.innerHTML = templ.innerHTML.replace("##longname##", nameLong);

                templ.innerHTML = templ.innerHTML.replace("##credits##", credits + " credits");
                templ.innerHTML = templ.innerHTML.replace("##creditsNum##", creditsNum);

                document.getElementById("course-list").appendChild(templ.content.cloneNode(true));

                templ.innerHTML = templ.innerHTML.replace("class" + num, "##classID##");
                templ.innerHTML = templ.innerHTML.replace("remove" + num, "##removeID##");
                templ.innerHTML = templ.innerHTML.replace(nameLong, "##classNME##");
                templ.innerHTML = templ.innerHTML.replace(nameLong, "##longname##");
                templ.innerHTML = templ.innerHTML.replace(nameShort, "##classname##");

                templ.innerHTML = templ.innerHTML.replace(credits + " credits", "##credits##");
                templ.innerHTML = templ.innerHTML.replace(creditsNum, "##creditsNum##");
                num++;

            }

        } catch (error) { }
    }
    

});

function pageBoxClick(element) {
    var num = element.innerHTML;
    if (num != "...") {
        //console.log("num: " + num + "   n: " + n + "   currentPage: " + currentPage);
        currentPage = num;
        n = (num * 10) - 10;
        //console.log("APRES - num: " + num + "   n: " + n + "   currentPage: " + currentPage);
        display(JSON.parse(currentData));
    }
}

$("#backward").click(function () {
    if (n >= 10) { n -= 10; currentPage--; }
    display(JSON.parse(currentData));
});

$("#forward").click(function () {
    if ((n + 10) < length) { n += 10; currentPage++; }
    display(JSON.parse(currentData));
});

$("#fullbackward").click(function () {
    n = 0; currentPage = 1;
    display(JSON.parse(currentData));
});

$("#fullforward").click(function () {
    n = (pageTotal * 10) - 10;
    currentPage = pageTotal;
    display(JSON.parse(currentData));
});

$("#search").submit(function (event) {
    event.preventDefault();
    $.ajax({
        type: "POST",
        url: route,
        data: { "searchBar": document.getElementById("searchBar").value, "searchButton": "" }
    }).done(function (response) {
        if (response.redirect) {
            window.location.href = response.redirect;
        } else {
            currentData = response; n = 0; currentPage = 1;
            display(JSON.parse(response));
        }
    });
});

$("#clear").submit(function (event) {
    
    $.ajax({
        type: "POST",
        url: route,
        data: { "clear": "true" }
    }).done(function (response) {
        currentData = response; n = 0; currentPage = 1;
        $('input[type="checkbox"]:checked').prop('checked', false);
        display(JSON.parse(response));
    });
});

$("#pathways").on("change", "input:checkbox", function (event) { 
    AJAX("pathways");
});

$("#departments").on("change", "input:checkbox", function (event) {
    AJAX("departments");
});

$("#courseLevel").on("change", "input:checkbox", function (event) {  
    AJAX("courseLevel");
});

$("#courseLength").on("change", "input:checkbox", function (event) {   
    AJAX("courseLength");
});

function AJAX(elementID) {
    var checked = "";
    var checkboxes = document.getElementById(elementID).querySelectorAll('input[type=checkbox]:checked');
    for (var i = 0; i < checkboxes.length; i++) checked += checkboxes[i].value + "#";
    $.ajax({
        type: "POST",
        url: route,
        data: { "selected": checked, "origin": elementID, "searchBar": document.getElementById("searchBar").value }
    }).done(function (response) {
        currentData = response; n = 0; currentPage = 1;
        display(JSON.parse(response));
    });
}

function display(json) {
    $("#results").html("");
    $("#pageNums").html("");

    var subKeys = Object.keys(json['ID']);

    if (subKeys.length == 0) {
        var temp = document.getElementById("noResult");
        document.getElementById("results").appendChild(temp.content.cloneNode(true));
        pageTotal = 1;
    } else {
        var temp = document.getElementById("cont");

        var start = n;
        var end = n + 10;
        length = subKeys.length;

        if (end > length) { end = length; }

        for (var s = start; s < end; s++) {
            var longDescription = json['longDescription'][subKeys[s]].toUpperCase();
            var description = json['description'][subKeys[s]];
            var dept = json['dept'][subKeys[s]] + ' ';

            var courseLength = json['Length'][subKeys[s]];

            var uniqueId = json['ID'][subKeys[s]];
            var creditsNum = json['credits'][subKeys[s]] + ".0";
            var credits = parseInt(creditsNum);
            var preRec = json['preRequisite'][subKeys[s]];

            temp.innerHTML = temp.innerHTML.replace("##course name##", longDescription);

            temp.innerHTML = temp.innerHTML.replace("##description##", description);
            temp.innerHTML = temp.innerHTML.replace("##preRecs##", preRec);

            temp.innerHTML = temp.innerHTML.replace("##depts##", dept);
            temp.innerHTML = temp.innerHTML.replace("##courseLength##", courseLength);
            temp.innerHTML = temp.innerHTML.replace("##credits##", credits + " credits");
            temp.innerHTML = temp.innerHTML.replace("##creditsNum##", creditsNum);
            temp.innerHTML = temp.innerHTML.replace("##uniqueId##", uniqueId);

            var levelNum = json['level'][subKeys[s]];
            var level = "";
            if (levelNum == "1") level = "Standard/CP";
            if (levelNum == "2") level = "Honors";
            if (levelNum == "3") level = "AP";

            temp.innerHTML = temp.innerHTML.replace("##courseLevel##", level);

            temp.innerHTML = temp.innerHTML.replace("##buttonID##", "button" + s);
            temp.innerHTML = temp.innerHTML.replace("##descID##", "desc" + s);

            temp.innerHTML = temp.innerHTML.replace("##addID##", "add" + s);
            temp.innerHTML = temp.innerHTML.replace("##nameID##", "name" + s);

            document.getElementById("results").appendChild(temp.content.cloneNode(true));

            temp.innerHTML = temp.innerHTML.replace(longDescription, "##course name##");

            temp.innerHTML = temp.innerHTML.replace(description, "##description##");
            temp.innerHTML = temp.innerHTML.replace(preRec, "##preRecs##");
            temp.innerHTML = temp.innerHTML.replace(dept, "##depts##");
            temp.innerHTML = temp.innerHTML.replace(courseLength, "##courseLength##");
            temp.innerHTML = temp.innerHTML.replace(credits + " credits", "##credits##");
            temp.innerHTML = temp.innerHTML.replace(creditsNum, "##creditsNum##");
            temp.innerHTML = temp.innerHTML.replace(uniqueId, "##uniqueId##");

            temp.innerHTML = temp.innerHTML.replace(level, "##courseLevel##");

            temp.innerHTML = temp.innerHTML.replace("button" + s, "##buttonID##");
            temp.innerHTML = temp.innerHTML.replace("desc" + s, "##descID##");

            temp.innerHTML = temp.innerHTML.replace("add" + s, "##addID##");

            temp.innerHTML = temp.innerHTML.replace("name" + s, "##nameID##");
        }
        pageTotal = Math.ceil(subKeys.length / 10);
    }

    //Pages Display
    //console.log("BEFORE - n: " + n + "   currentPage: " + currentPage + "   currentPageBox: " + currentPageBox.id);

    currentPageBox.style.fontWeight = "normal"; //reset text format

    for (var i = 1; i < 6; i++) { //bring back hidden pageBoxes
        document.getElementById("pageBox" + i).style.display = "revert";
    }

    if (currentPage < 4) { currentPageBox = document.getElementById("pageBox" + currentPage); }

    if (pageTotal > 4) { document.getElementById("pageBox5").innerHTML = pageTotal; }
    else if (pageTotal == 4) { document.getElementById("pageBox4").innerHTML = pageTotal; }

    for (var i = 5; i > pageTotal; i--) {
        document.getElementById("pageBox" + i).style.display = "none";
    }

    if (currentPage > 3 && pageTotal > 4) {
        document.getElementById("pageBox2").innerHTML = "...";
        document.getElementById("pageBox3").innerHTML = currentPage;
    }
    else {
        document.getElementById("pageBox2").innerHTML = "2";
        document.getElementById("pageBox3").innerHTML = "3";
    }

    if (document.getElementById("pageBox3").innerHTML >= (pageTotal - 2) && pageTotal > 4) {
        document.getElementById("pageBox4").innerHTML = pageTotal - 1;
    }
    else if (pageTotal > 4) {
        document.getElementById("pageBox4").innerHTML = "...";
    }

    if (currentPage >= (pageTotal - 1) && pageTotal > 4) {
        document.getElementById("pageBox3").innerHTML = pageTotal - 2;
        currentPageBox = document.getElementById("pageBox4");
        if (currentPage == pageTotal) {
            currentPageBox = document.getElementById("pageBox5");
        }
    }
    else if (currentPage > 2 && pageTotal > 4) {
        currentPageBox = document.getElementById("pageBox3");
    }

    if (pageTotal <= 4) {
        currentPageBox = document.getElementById("pageBox" + currentPage);
    }

    currentPageBox.style.fontWeight = "bold";

    //console.log("AFTER - n: " + n + "   currentPage: " + currentPage + "   currentPageBox: " + currentPageBox.id);
}


//VARIABLES
var theseContainers = document.getElementsByClassName("dropdown-container");
var dropdownBttns = document.getElementsByClassName("dropdown");
const dropdownmMap = new Map();
var filterTypes = document.getElementsByClassName("filterType");

//CLICKING ON DROPDOWNS
var onButtonClick = function (event) {
    var thisBttn = event.currentTarget;
    var container = dropdownmMap.get(thisBttn);
    $(container).toggle();
};

//CLICKING ON CHECKBOXES
const filterTypeBox = new Map([
    ["pathways", ""],
    ["departments", ""],
    ["courseLevel", ""],
    ["courseLength", ""]
]);
var checkboxClick = function (element) {
    var filterType = element.parentElement.parentElement.parentElement.id;
    //console.log(filterType);
    //console.log("ID: " + element.id + "      checked: " + element.checked);
    if (filterTypeBox.get(filterType) != "") {
        filterTypeBox.get(filterType).checked = false;
    }
    if (filterTypeBox.get(filterType) == element) {
        filterTypeBox.set(filterType, "");
    }
    else {
        filterTypeBox.set(filterType, element);
    }
    //console.log(filterTypeBox);
}

//View Description Button
var lastDescript;
var descriptionBttn = function (element) {
    var elementName = element.id;
    var elNum = elementName.substring(6);
    var descript = document.getElementById("desc" + elNum);
    $(descript).toggle();
    if (lastDescript != null) {
        if (descript != lastDescript && lastDescript.style.display != "none") {
            $(lastDescript).toggle();
        }
    }
    lastDescript = descript;

}

//Add event listeners to all dropdowns
for (var i = 0; i < dropdownBttns.length; i++) {
    dropdownmMap.set(dropdownBttns[i], theseContainers[i]);
    dropdownBttns[i].addEventListener("click", onButtonClick);
}
