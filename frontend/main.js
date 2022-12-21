

const icon = document.querySelector('i.fa.fa-microphone');
function voiceSearch() {
    var SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.start();
    recognition.onresult = (event) => {
        const speechToText = event.results[0][0].transcript;
        console.log(speechToText);
        document.getElementById("searchbar").value = speechToText;
        searchImage();
      }
}

function searchImage() {
  var searchTerm = document.getElementById("searchbar").value;
  var apigClient = apigClientFactory.newClient({ apiKey: "goMghRsRvP2F2Tx8gmfRG7WC1WON580b8geKbfkA" });

  var params = {
    "q": searchTerm
  };

  console.log(searchTerm);
  apigClient.searchGet(params, {}, {})
    .then(function (result) {
      console.log('success found');
      var newDiv = document.getElementById("images");
      if(typeof(newDiv) != 'undefined' && newDiv != null){
          while (newDiv.firstChild) {
              newDiv.removeChild(newDiv.firstChild);
          }
      }

      if(result.data.length == 0){
          $(images).append('<h1>Search not found</h1>')
          return
      }
      for (var i = 0; i < result.data.length; i++) {
        console.log(result.data[i]);
        var newDiv = document.getElementById("images");
        newDiv.style.display = 'inline'
        var newimg = document.createElement("img");
        newimg.classList.add();
        url =  'https://photoss3000001.s3.amazonaws.com/'+ result.data[i]['objectKey'];
        newimg.src = url
        console.log(url)
        newDiv.appendChild(newimg);
      }

    }).catch(function (result) {
      console.log("Search not found");
    });

}


function uploadPhoto() {
    var file = document.getElementById('myFile').files[0];
    file.constructor = () => file;
    var labels = document.getElementById('labels').value
    var apigClient = apigClientFactory.newClient({ apiKey: "goMghRsRvP2F2Tx8gmfRG7WC1WON580b8geKbfkA" });

    var params = {
      "img": file.name,
      "photos": "photoss3000001",
      "Content-Type": file.type,
      "x-amz-meta-customLabels": labels
    };
    console.log(file.type)

    var additionalParams = {
      // headers: {
      //   "x-amz-meta-customLabels": ""
      // }
    };

    apigClient.uploadPhotosImgPut(params, file, additionalParams)
        .then(function (result) {
          console.log('success OK');
        }).catch(function (result) {
      console.log(result);
    });

}
