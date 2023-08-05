/*

const copyFrom = document.getElementById('copy-from');
const copyTo = document.getElementById('copy-to');
const copyButton = document.getElementById('copy-button');

copyButton.addEventListener('click', () => {
  var linkElements = document.querySelectorAll("#youtube_link");

  var hrefValues = Array.from(linkElements).map(function(link) {
      return link.href; // Get the href value of each <a> tag
    });

  var tempTextarea = document.createElement("textarea");
  tempTextarea.value = hrefValues.join("\n");

  document.body.appendChild(tempTextarea);

  tempTextarea.select();
  tempTextarea.setSelectionRange(0, 99999); // For mobile devices

  document.execCommand("copy");

  document.body.removeChild(tempTextarea);

  alert("Infringing Urls copied to clipboard: \n" + hrefValues.join("\n"));

});

*/

const copyFrom = document.getElementById('copy-from');
const copyTo = document.getElementById('copy-to');
const copyButton = document.getElementById('copy-button');

copyButton.addEventListener('click', () => {
  var linkElements = document.querySelectorAll("#youtube_link");
  var row = document.querySelectorAll("#youtube_result");

  function extractDataFromRows(rows) {
    var extractedData = [];

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        var channelTitle = cells[1].getElementsByTagName("a")[0].textContent;
        var channelUrl = cells[1].getElementsByTagName("a")[0].getAttribute("href");
        var vidTitle = cells[2].textContent;
        var videoPublishedAt = cells[3].textContent;
        var videoViewCount = cells[4].textContent;
        var channelSubscriberCount = cells[5].textContent;
        var video_url = cells[7].getElementsByTagName("a")[0].getAttribute("href");
        //var video_url = "dummy";

        var rowData = channelTitle + "\t" + channelUrl + "\t" + vidTitle + "\t" + videoPublishedAt + "\t" + videoViewCount + "\t" + channelSubscriberCount + "\t" + video_url;
        extractedData.push(rowData);
    }

    return extractedData;
}
    var data = extractDataFromRows(row);
    console.log("--!");
    console.log(data);
    console.log("--2");

  var tempTextarea = document.createElement("textarea");

  tempTextarea.value = data.join("\n");

  document.body.appendChild(tempTextarea);

  tempTextarea.select();
  tempTextarea.setSelectionRange(0, 99999); // For mobile devices

  document.execCommand("copy");

  document.body.removeChild(tempTextarea);

  //alert("Infringing Urls copied to clipboard: \n" + data.join("\n"));
  alert("URL's Copied ...!!")

});