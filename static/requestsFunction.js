//need initializing AJAX call
var cartContents;
var classDepartments = ["lol"];
var requirements = ["English", "Mathematics", "Science", "Social Studies"];
var reqirementPairs = new Map([
    ["English", "EN"],
    ["Mathematics", "MA"],
    ["Science", "SC"],
    ["Social Studies", "SS"],
    ["Health", "HP"],
    ["Physical Education", "HP"]
]);
var gradeReqirements = new Map([]);
//populate gradeRequirements
for (var i = 0; i < requirements.length; i++) {
    gradeReqirements.set(reqirementPairs.get(requirements[i]), false);
}

$.ajax({
    type: "POST",
    url: "/requests",
    data: { "initialized": "1" }
}).done(function (response) {
    cartContents = response;
    try {
        display(JSON.parse(response))
    } catch (error) { }

    //console.log(cartContents);
});

$("#return").submit(function (event) {
    event.preventDefault();
    $.ajax({
        type: "POST",
        url: "/requests",
        data: { "return": '1' }
    }).done(function (response) {
        if (response.redirect) {
            window.location.href = response.redirect;
        }
    });
});

function display(json) {
    $("#results").html("");
    var subKeys = Object.keys(json['ID']);
    var temp = document.getElementById("cont");

    for (var s = 0; s < subKeys.length; s++) {
        var longDescription = json['longDescription'][subKeys[s]];
        var creds = json['credits'][subKeys[s]];

        //Get Departments
        var dept = json['dept'][subKeys[s]];
        classDepartments[s] = dept;

        temp.innerHTML = temp.innerHTML.replace("##name##", longDescription);
        temp.innerHTML = temp.innerHTML.replace("##credits##", creds);

        document.getElementById("results").appendChild(temp.content.cloneNode(true));

        temp.innerHTML = temp.innerHTML.replace(longDescription, "##name##");
        temp.innerHTML = temp.innerHTML.replace(creds, "##credits##");
    }

    //Requirements
    //console.log(classDepartments.toString());
    for (var i = 0; i < requirements.length; i++) {
        checkRequirement(reqirementPairs.get(requirements[i]));
    }
    //console.log([...gradeReqirements]);

    //Display Requirements
    var reqListHTML = document.getElementById("requirementsList");
    for (var i = 0; i < requirements.length; i++) {
        var node = document.createElement('li');
        node.appendChild(document.createTextNode(requirements[i]));
        if (gradeReqirements.get(reqirementPairs.get(requirements[i])) == true) {
            console.log("you have: " + requirements[i]);
            node.style.color = "green";
        }
        reqListHTML.appendChild(node);
    }

}

function checkRequirement(requirement) {
    if (classDepartments.includes(requirement)) {
        gradeReqirements.set(requirement, true);

    }
}
