const submitBtn1 = document.getElementById("submit-btn-1");
const firstFour = document.querySelector(".first-four");

const submitBtn2 = document.getElementById("submit-btn-2");
const secFour = document.querySelector(".sec-four");

const submitBtn3 = document.getElementById("submit-btn-3");
const thirdFour = document.querySelector(".third-four");

const submitBtn4 = document.getElementById("submit-btn-4");
const fourthFour = document.querySelector(".fourth-four");


submitBtn1.addEventListener("click", ()=> {
    const inputText1 = document.getElementById("input1").value.trim();

    if (inputText1.toLowerCase() === "enigma m3") {
        firstFour.classList.remove("centered-align");
        firstFour.classList.add("hidden");
    }
    else{
        alert("Incorrect deciphering! Try again!")
    }
});

submitBtn2.addEventListener("click", ()=> {
    const inputText2 = document.getElementById("input2").value.trim();

    if (inputText2.toLowerCase() === "ukw c") {
        secFour.classList.remove("centered-align");
        secFour.classList.add("hidden");
    }
    else{
        alert("Incorrect deciphering! Try again!")
    }
});

submitBtn3.addEventListener("click", ()=> {
    const inputText3 = document.getElementById("input3").value.trim();

    if (inputText3.toLowerCase() === "rotor1 i p m rotor2 iv a o rotor3 vi i n") {
        thirdFour.classList.remove("centered-align");
        thirdFour.classList.add("hidden");
    }
    else{
        alert("Incorrect deciphering! Try again!")
    }
});

submitBtn4.addEventListener("click", ()=> {
    const inputText4 = document.getElementById("input4").value.trim();

    if (inputText4.toLowerCase() === "vi sh wa ct fx") {
        fourthFour.classList.remove("centered-align");
        fourthFour.classList.add("hidden");        
    }
    else{
        alert("Incorrect deciphering! Try again!")
    }
});