document.addEventListener("DOMContentLoaded", function() {
  hideAllInputFields();
  document.getElementById("SentimentCheck").style.display = "none";
});

function hideAllInputFields() {
  document.getElementById("url_input").style.display = "none";
  document.getElementById("text_input").style.display = "none";
  document.getElementById("file_input").style.display = "none";
  document.getElementById("container").style.display = "none";
  document.getElementById("Score").style.display = "none";
}

function showInputField(id) {
  hideAllInputFields();
  document.getElementById(id).style.display = "block";
  document.getElementById("SentimentCheck").style.display = "block";
}

function processInput() {
  document.getElementById("container").style.display = "block";
  document.getElementById("Score").style.display = "block";
  document.getElementById("positive_lines").style.display = "none";
  document.getElementById("negative_lines").style.display = "none";

  // Example: Set the sentiment score and lines
  document.getElementById("sentiment").innerText = "Positive";
  document.getElementById("positive_lines").innerHTML = "<p>Example positive line 1</p><p>Example positive line 2</p>";
  document.getElementById("negative_lines").innerHTML = "<p>Example negative line 1</p><p>Example negative line 2</p>";
}

function toggleCollapse(id) {
  const content = document.getElementById(id);
  if (content.style.display === "block") {
    content.style.display = "none";
  } else {
    content.style.display = "block";
  }
}
