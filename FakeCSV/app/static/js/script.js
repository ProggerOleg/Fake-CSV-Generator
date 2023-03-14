function toggleFromTo() {
  var select = document.getElementById("inputType");
  var selectedValue = select.value;
  console.log(selectedValue);
  var elements = document.getElementsByClassName("FromTo");
  if (selectedValue === "number") {
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.display = "block";
    }
  } else {
    for (var i = 0; i < elements.length; i++) {
      elements[i].style.display = "none";
    }
  }
}